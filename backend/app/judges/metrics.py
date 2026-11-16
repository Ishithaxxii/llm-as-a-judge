
from __future__ import annotations

import re
import math
from statistics import mean, pstdev
from typing import Sequence


# Default weights used by the six-metric evaluator.
DEFAULT_WEIGHTS = {
    "answer_correctness": 0.25,
    "relevance": 0.15,
    "query_alignment": 0.20,
    "semantic_similarity": 0.15,
    "tone": 0.10,
    "tool_calling": 0.15,
}


def calculate_weighted_score(
    criterion_scores: dict,
    criterion_weights: dict[str, float] | None = None,
    fallback_score: float = 0.0,
) -> float:
    """Calculate a weighted score, excluding criteria with null values."""

    weights = criterion_weights or DEFAULT_WEIGHTS

    applicable = [
        (float(criterion_scores[name]), float(weight))
        for name, weight in weights.items()
        if (
            name in criterion_scores
            and criterion_scores[name] is not None
            and weight > 0
        )
    ]

    if not applicable:
        return round(float(fallback_score), 2)

    total_weight = sum(weight for _, weight in applicable)

    weighted_total = sum(
        score * weight for score, weight in applicable
    )

    return round(weighted_total / total_weight, 2)


def _tokenize(text: str) -> set[str]:
    text = text.lower()
    return set(re.findall(r"[a-z0-9_]+", text))


def jaccard_similarity(text1: str, text2: str) -> float:
    if not text1 or not text2:
        return 0.0

    set1, set2 = _tokenize(text1), _tokenize(text2)

    if not set1 and not set2:
        return 1.0

    intersection = len(set1 & set2)
    union = len(set1 | set2)

    return round(intersection / union, 4) if union else 0.0


def cosine_similarity_simple(text1: str, text2: str) -> float:
    """Lightweight bag-of-words cosine similarity."""

    if not text1 or not text2:
        return 0.0

    tokens1 = _tokenize(text1)
    tokens2 = _tokenize(text2)
    all_tokens = list(tokens1 | tokens2)

    if not all_tokens:
        return 1.0

    vec1 = [1 if t in tokens1 else 0 for t in all_tokens]
    vec2 = [1 if t in tokens2 else 0 for t in all_tokens]

    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return round(dot / (norm1 * norm2), 4)


def z_score(score: float, history: Sequence[float]) -> float | None:
    if len(history) < 5:
        return None

    mu = mean(history)
    sigma = pstdev(history)

    if sigma == 0:
        return 0.0

    return round((score - mu) / sigma, 3)


def compute_metrics(
    outcomes: list,
    historical_scores: list[float] | None = None,
    criterion_weights: dict[str, float] | None = None,
) -> dict:

    valid = [
        outcome
        for outcome in outcomes
        if getattr(outcome, "error", None) is None
    ]

    if not valid:
        return {
            "aggregate_score": 0.0,
            "agreement": 0.0,
            "flagged_disagreement": True,
            "jaccard": 0.0,
            "cosine": 0.0,
            "z_score": None,
            "score_std": 0.0,
            "num_valid_judges": 0,
        }

    # Recalculate each judge's score from its criterion scores.
    scores = [
        calculate_weighted_score(
            outcome.criterion_scores,
            criterion_weights,
            fallback_score=outcome.score,
        )
        for outcome in valid
    ]

    avg = mean(scores)
    std = pstdev(scores) if len(scores) > 1 else 0.0

    cv = (std / avg) if avg else 0.0
    agreement = max(0.0, min(1.0, 1 - cv))

    jaccards, cosines = [], []

    for i in range(len(valid)):
        for j in range(i + 1, len(valid)):
            jaccards.append(
                jaccard_similarity(
                    valid[i].reasoning,
                    valid[j].reasoning,
                )
            )

            cosines.append(
                cosine_similarity_simple(
                    valid[i].reasoning,
                    valid[j].reasoning,
                )
            )

    avg_jaccard = round(mean(jaccards), 4) if jaccards else 1.0
    avg_cosine = round(mean(cosines), 4) if cosines else 1.0

    z = z_score(avg, historical_scores or [])

    return {
        "aggregate_score": round(avg, 2),
        "agreement": round(agreement, 3),
        "flagged_disagreement": agreement < 0.70,
        "jaccard": avg_jaccard,
        "cosine": avg_cosine,
        "z_score": z,
        "score_std": round(std, 3),
        "num_valid_judges": len(valid),
    }
