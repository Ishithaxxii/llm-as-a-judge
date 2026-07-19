from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import get_settings
from app.database import get_db
from app.judges.orchestrator import JudgeOutcome, aggregate, run_judges
from app.models import JudgeResult, Rubric, Submission
from app.schemas import JudgeRequest, JudgeResponse, JudgeResultOut

router = APIRouter(prefix="/judge", tags=["judge"])
settings = get_settings()

@router.post("", response_model=JudgeResponse)
async def judge_submission(payload: JudgeRequest, db: AsyncSession = Depends(get_db)):
    submission = await db.get(Submission, payload.submission_id)
    if not submission:
        raise HTTPException(404, "Submission not found")

    criteria = [{"name": "overall_quality", "description": "General quality", "weight": 1.0, "scale": 10}]
    if submission.rubric_id:
        rubric = await db.get(Rubric, submission.rubric_id)
        if rubric:
            criteria = rubric.criteria

    judges = payload.judges or settings.default_judges

    existing = await db.execute(
        select(JudgeResult).where(JudgeResult.submission_id == submission.id, JudgeResult.model_name.in_(judges))
    )
    cached = {r.model_name: r for r in existing.scalars().all()}
    to_run = [j for j in judges if j not in cached]

    new_results = []
    if to_run:
        outcomes = await run_judges(submission.content, submission.content_type, criteria, to_run)
        for o in outcomes:
            if o.error:
                continue
            rec = JudgeResult(
                submission_id=submission.id, model_name=o.model_name, score=o.score,
                reasoning=o.reasoning, criterion_scores=o.criterion_scores,
                confidence=o.confidence, latency_ms=o.latency_ms,
            )
            db.add(rec)
            new_results.append(rec)
        await db.commit()
        for r in new_results:
            await db.refresh(r)

    all_results = list(cached.values()) + new_results
    if not all_results:
        raise HTTPException(502, "All judges failed — check API keys")

    agg = aggregate([JudgeOutcome(r.model_name, r.score, r.reasoning, r.criterion_scores, r.confidence, r.latency_ms or 0) for r in all_results])

    return JudgeResponse(
        submission_id=submission.id,
        results=[JudgeResultOut.model_validate(r) for r in all_results],
        aggregate_score=agg["aggregate_score"],
        agreement=agg["agreement"],
        flagged_disagreement=agg["flagged_disagreement"],
    )