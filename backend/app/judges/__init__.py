JSON_INSTRUCTIONS = """
Respond with ONLY a JSON object, no markdown fences, no extra text:
{
  "criterion_scores": {"<criterion_name>": <score 0-scale>, ...},
  "reasoning": "<2-4 sentence justification>",
  "overall_score": <weighted average>,
  "confidence": <0.0-1.0>
}
"""

def build_scoring_prompt(content: str, content_type: str, criteria: list[dict]) -> str:
    criteria_block = "\n".join(
        f"- {c['name']} (weight {c['weight']}, scale 0-{c['scale']}): {c['description']}"
        for c in criteria
    )
    return f"""You are an expert evaluator judging a piece of {content_type} against a rubric.

RUBRIC:
{criteria_block}

SUBMISSION:
---
{content}
---

Reason step by step per criterion BEFORE scoring. Do not let length alone
influence the score — a concise correct answer should not be penalized
relative to a verbose one saying the same thing.

{JSON_INSTRUCTIONS}
"""