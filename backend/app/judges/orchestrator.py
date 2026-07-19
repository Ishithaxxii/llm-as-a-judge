import asyncio, json, time
from dataclasses import dataclass
from statistics import mean, pstdev
import httpx
from app.config import get_settings
from app.judges.prompts import build_scoring_prompt
import random

settings = get_settings()

@dataclass
class JudgeOutcome:
    model_name: str
    score: float
    reasoning: str
    criterion_scores: dict
    confidence: float | None
    latency_ms: int
    error: str | None = None

async def _call_groq(client, model, prompt, api_key):
    resp = await client.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
            "response_format": {"type": "json_object"},
        },
        timeout=settings.judge_timeout_seconds,
    )
    resp.raise_for_status()
    return json.loads(resp.json()["choices"][0]["message"]["content"])

async def _call_gemini(client, model, prompt, api_key):
    resp = await client.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}",
        json={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.0, "responseMimeType": "application/json"},
        },
        timeout=settings.judge_timeout_seconds,
    )
    resp.raise_for_status()
    text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text)

async def _mock_judge(model_name: str, prompt: str) -> JudgeOutcome:
    """Simulates a judge response instantly, no network call, no API cost.
    Used for testing the request/response flow, aggregation, and caching
    logic in isolation from the actual LLM providers."""
    await asyncio.sleep(0.3)  # simulate a bit of latency so loading states are visible
    score = round(random.uniform(5.0, 9.5), 1)
    return JudgeOutcome(
        model_name=model_name,
        score=score,
        reasoning=f"[MOCK] This is a simulated evaluation from {model_name}, standing in for a real API call during testing.",
        criterion_scores={"overall_quality": score},
        confidence=round(random.uniform(0.6, 0.95), 2),
        latency_ms=300,
    )

async def _run_single_judge(client, model_name, prompt):
    provider, _, model = model_name.partition(":")
    api_key = {"groq": settings.groq_api_key, "gemini": settings.gemini_api_key}.get(provider)
    if not api_key:
        return JudgeOutcome(model_name, 0, "", {}, None, 0, error=f"no API key for {provider}")

    start = time.monotonic()
    try:
        if provider == "groq":
            parsed = await _call_groq(client, model, prompt, api_key)
        elif provider == "gemini":
            parsed = await _call_gemini(client, model, prompt, api_key)
        else:
            return JudgeOutcome(model_name, 0, "", {}, None, 0, error=f"unknown provider {provider}")

        latency_ms = int((time.monotonic() - start) * 1000)
        return JudgeOutcome(
            model_name=model_name,
            score=float(parsed["overall_score"]),
            reasoning=parsed.get("reasoning", ""),
            criterion_scores={k: float(v) for k, v in parsed.get("criterion_scores", {}).items()},
            confidence=parsed.get("confidence"),
            latency_ms=latency_ms,
        )
    except (httpx.HTTPError, KeyError, ValueError, json.JSONDecodeError) as exc:
        return JudgeOutcome(model_name, 0, "", {}, None, int((time.monotonic() - start) * 1000), error=str(exc))

# async def run_judges(content, content_type, criteria, judges):
#     judges = judges[: settings.max_judges_per_request]
#     prompt = build_scoring_prompt(content, content_type, criteria)
#     async with httpx.AsyncClient() as client:
#         return await asyncio.gather(*[_run_single_judge(client, j, prompt) for j in judges])

# TEST RUN_JUDGES
async def run_judges(content, content_type, criteria, judges):
    judges = judges[: settings.max_judges_per_request]

    if settings.mock_judges:
        return await asyncio.gather(*[_mock_judge(j, "") for j in judges])

    prompt = build_scoring_prompt(content, content_type, criteria)
    async with httpx.AsyncClient() as client:
        return await asyncio.gather(*[_run_single_judge(client, j, prompt) for j in judges])

def aggregate(outcomes):
    valid = [o for o in outcomes if o.error is None]
    if not valid:
        return {"aggregate_score": 0.0, "agreement": 0.0, "flagged_disagreement": True}
    scores = [o.score for o in valid]
    avg = mean(scores)
    std = pstdev(scores) if len(scores) > 1 else 0.0
    cv = (std / avg) if avg else 0.0
    agreement = max(0.0, min(1.0, 1 - cv))
    return {"aggregate_score": round(avg, 2), "agreement": round(agreement, 2), "flagged_disagreement": agreement < 0.7}