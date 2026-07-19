from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Submission
from app.schemas import SubmissionCreate, SubmissionOut

router = APIRouter(prefix="/submissions", tags=["submissions"])

@router.post("", response_model=SubmissionOut)
async def create_submission(payload: SubmissionCreate, db: AsyncSession = Depends(get_db)):
    s = Submission(content=payload.content, content_type=payload.content_type, rubric_id=payload.rubric_id)
    db.add(s)
    await db.commit()
    await db.refresh(s)
    return s

@router.get("/{submission_id}", response_model=SubmissionOut)
async def get_submission(submission_id: str, db: AsyncSession = Depends(get_db)):
    s = await db.get(Submission, submission_id)
    if not s:
        raise HTTPException(404, "Not found")
    return s