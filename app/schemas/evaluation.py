from pydantic import BaseModel


class EvaluationRequest(BaseModel):
    question: str
    reference_answer: str
    model_answer: str
