from fastapi import APIRouter

from app.schemas.evaluation import EvaluationRequest
from app.services.evaluator import LLMEvaluator

router = APIRouter()

evaluator = LLMEvaluator()


@router.post("/evaluate")
async def evaluate_response(payload: EvaluationRequest):
    result = evaluator.evaluate(
        question=payload.question,
        reference_answer=payload.reference_answer,
        model_answer=payload.model_answer
    )

    return result
