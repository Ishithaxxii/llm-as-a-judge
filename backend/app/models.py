from app.database import Base
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import relationship

def _uuid() -> str:
    return str(uuid.uuid4())

class Rubric(Base):
    __tablename__ = "rubrics"
    id: Mapped[str] = mapped_column(primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(nullable=False)
    domain: Mapped[str] = mapped_column(nullable=False)
    criteria: Mapped[list] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    submissions: Mapped[list["Submission"]] = relationship(back_populates="rubric")


class Submission(Base):
    __tablename__ = "submissions"
    id: Mapped[str] = mapped_column(primary_key=True, default=_uuid)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_type: Mapped[str] = mapped_column(String, default="text")
    rubric_id: Mapped[str | None] = mapped_column(ForeignKey("rubrics.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    rubric: Mapped["Rubric | None"] = relationship(back_populates="submissions")
    results: Mapped[list["JudgeResult"]] = relationship(back_populates="submission")


class JudgeResult(Base):
    __tablename__ = "judge_results"
    id: Mapped[str] = mapped_column(primary_key=True, default=_uuid)
    submission_id: Mapped[str] = mapped_column(ForeignKey("submissions.id"))
    model_name: Mapped[str] = mapped_column(nullable=False)
    score: Mapped[float] = mapped_column(nullable=False)
    reasoning: Mapped[str] = mapped_column(Text, nullable=False)
    criterion_scores: Mapped[dict] = mapped_column(JSON, default=dict)
    confidence: Mapped[float | None] = mapped_column(nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    submission: Mapped["Submission"] = relationship(back_populates="results")