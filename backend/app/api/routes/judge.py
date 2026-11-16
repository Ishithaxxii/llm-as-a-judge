from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import get_settings
from app.database import get_db
from app.judges.orchestrator import JudgeOutcome, aggregate, run_judges
from app.judges.metrics import calculate_weighted_score
from app.models import JudgeResult, Rubric, Submission
from app.schemas import JudgeRequest, JudgeResponse, JudgeResultOut

router = APIRouter(prefix="/judge", tags=["judge"])
settings = get_settings()


@router.post("", response_model=JudgeResponse)
async def judge_submission(payload: JudgeRequest, db: AsyncSession = Depends(get_db)):
    submission = await db.get(Submission, payload.submission_id)
    if not submission:
        raise HTTPException(404, "Submission not found")

    # Default criteria
    criteria = [
        {
            "name": "answer_correctness",
            "description": "Factual accuracy and correctness of the response.",
            "weight": 0.25,
            "scale": 10,
        },
        {
            "name": "relevance",
            "description": "How relevant and focused the response is to the subject.",
            "weight": 0.15,
            "scale": 10,
        },
        {
            "name": "query_alignment",
            "description": "How accurately the response addresses the original user query.",
            "weight": 0.20,
            "scale": 10,
        },
        {
            "name": "semantic_similarity",
            "description": "How closely the response matches the meaning of the reference answer.",
            "weight": 0.15,
            "scale": 10,
        },
        {
            "name": "tone",
            "description": "Clarity, professionalism, and suitability of communication.",
            "weight": 0.10,
            "scale": 10,
        },
        {
            "name": "tool_calling",
            "description": "Appropriateness and successful execution of tool calls.",
            "weight": 0.15,
            "scale": 10,
        },
    ]
    criterion_weights = {
        c["name"]: c["weight"]
        for c in criteria
    }
    if submission.rubric_id:
        rubric = await db.get(Rubric, submission.rubric_id)
        if rubric:
            criteria = rubric.criteria

    judges = payload.judges or settings.default_judges

    # Caching
    existing = await db.execute(
        select(JudgeResult).where(
            JudgeResult.submission_id == submission.id,
            JudgeResult.model_name.in_(judges)
        )
    )
    cached = {r.model_name: r for r in existing.scalars().all()}
    to_run = [j for j in judges if j not in cached]

    new_results = []
    if to_run:
        outcomes = await run_judges(
            content=submission.content,
            content_type=submission.content_type,
            criteria=criteria,
            judges=to_run,
            query=submission.query,
            reference_answer=submission.reference_answer,
            tool_trace=submission.tool_trace,
        )
        for o in outcomes:
            if o.error:
                continue
            rec = JudgeResult(
                submission_id=submission.id,
                model_name=o.model_name,
                score=o.score,
                reasoning=o.reasoning,
                criterion_scores=o.criterion_scores,
                confidence=o.confidence,
                latency_ms=o.latency_ms,
            )
            o.score = calculate_weighted_score(
                o.criterion_scores,
                criterion_weights,
                fallback_score=o.score,
            )
            db.add(rec)
            new_results.append(rec)
        await db.commit()
        for r in new_results:
            await db.refresh(r)

    all_results = list(cached.values()) + new_results
    if not all_results:
        raise HTTPException(502, "All judges failed — check API keys")

    # Build outcomes for metrics
    outcomes_for_metrics = [
        JudgeOutcome(
            r.model_name,
            r.score,
            r.reasoning,
            r.criterion_scores,
            r.confidence,
            r.latency_ms or 0
        )
        for r in all_results
    ]

    # --- Historical scores for Z-score (simple global for now) ---
    hist_query = await db.execute(select(JudgeResult.score).limit(200))
    historical_scores = [row[0] for row in hist_query.all()]

    agg = aggregate(
        outcomes_for_metrics,
        historical_scores,
        criterion_weights,
    )
    
    return JudgeResponse(
        submission_id=submission.id,
        results=[JudgeResultOut.model_validate(r) for r in all_results],
        aggregate_score=agg["aggregate_score"],
        agreement=agg["agreement"],
        flagged_disagreement=agg["flagged_disagreement"],
        jaccard=agg["jaccard"],
        cosine=agg["cosine"],
        z_score=agg["z_score"],
        score_std=agg["score_std"],
        num_valid_judges=agg["num_valid_judges"],
    )