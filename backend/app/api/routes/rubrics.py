from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Rubric
from app.schemas import RubricCreate, RubricOut

router = APIRouter(prefix="/rubrics", tags=["rubrics"])

TEMPLATES = {
    "code_review": [
        {"name": "correctness", "description": "Does it work correctly?", "weight": 2.0, "scale": 10},
        {"name": "readability", "description": "Clear and well-named?", "weight": 1.0, "scale": 10},
    ],
    "essay": [
        {"name": "thesis_clarity", "description": "Clear central claim?", "weight": 1.5, "scale": 10},
        {"name": "evidence", "description": "Claims backed with evidence?", "weight": 1.5, "scale": 10},
    ],
}

@router.post("", response_model=RubricOut)
async def create_rubric(payload: RubricCreate, db: AsyncSession = Depends(get_db)):
    r = Rubric(name=payload.name, domain=payload.domain, criteria=[c.model_dump() for c in payload.criteria])
    db.add(r)
    await db.commit()
    await db.refresh(r)
    return r

@router.get("/templates")
async def list_templates():
    return TEMPLATES

@router.get("/{rubric_id}", response_model=RubricOut)
async def get_rubric(rubric_id: str, db: AsyncSession = Depends(get_db)):
    r = await db.get(Rubric, rubric_id)
    if not r:
        raise HTTPException(404, "Not found")
    return r