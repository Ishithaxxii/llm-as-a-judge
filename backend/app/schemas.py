from pydantic import BaseModel

class Criterion(BaseModel):
    name: str
    description: str
    weight: float = 1.0
    scale: int = 10

class RubricCreate(BaseModel):
    name: str
    domain: str
    criteria: list[Criterion]

class RubricOut(RubricCreate):
    id: str
    model_config = {"from_attributes": True}

class SubmissionCreate(BaseModel):
    content: str
    content_type: str = "text"
    rubric_id: str | None = None

class SubmissionOut(BaseModel):
    id: str
    content: str
    content_type: str
    rubric_id: str | None
    model_config = {"from_attributes": True}

class JudgeRequest(BaseModel):
    submission_id: str
    judges: list[str] | None = None

class JudgeResultOut(BaseModel):
    model_name: str
    score: float
    reasoning: str
    criterion_scores: dict[str, float]
    confidence: float | None
    latency_ms: int | None
    model_config = {"from_attributes": True}

class JudgeResponse(BaseModel):
    submission_id: str
    results: list[JudgeResultOut]
    aggregate_score: float
    agreement: float
    flagged_disagreement: bool = False