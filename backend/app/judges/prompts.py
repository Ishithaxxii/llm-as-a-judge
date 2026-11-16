
import json

JSON_INSTRUCTIONS = """
Return ONLY a valid JSON object. Do not include markdown fences or extra text.

Use this exact structure:
{
  "criterion_scores": {
    "answer_correctness": 0,
    "relevance": 0,
    "query_alignment": 0,
    "semantic_similarity": null,
    "tone": 0,
    "tool_calling": null
  },
  "reasoning": "Brief evidence-based explanation of the scores.",
  "overall_score": 0,
  "confidence": 0.0
}

Rules:
- Scores must be numbers between 0 and 10, or null when not applicable.
- Do not invent missing queries, reference answers, or tool traces.
- If the original query is missing, query_alignment must be null.
- If the reference answer is missing, semantic_similarity must be null.
- If the tool trace is missing, tool_calling must be null.
- Calculate overall_score as the weighted average of applicable criteria only.
- Exclude null criteria from the weighted average.
- If a criterion is not applicable, do not give it a score of zero.
- Keep reasoning concise and evidence-based. Do not reveal hidden chain-of-thought.
"""


def build_scoring_prompt(
    content: str,
    content_type: str,
    criteria: list[dict],
    query: str | None = None,
    reference_answer: str | None = None,
    tool_trace: list | None = None,
) -> str:

    criteria_block = "\n".join(
        f"- {c['name']} (weight {c['weight']}, scale 0-{c['scale']}): "
        f"{c['description']}"
        for c in criteria
    )

    query_text = query if query else "NOT PROVIDED"
    reference_text = reference_answer if reference_answer else "NOT PROVIDED"
    tool_trace_text = (
        json.dumps(tool_trace, indent=2, ensure_ascii=False)
        if tool_trace
        else "NOT PROVIDED"
    )

    return f"""
You are an independent evaluator assessing an AI-generated response.

EVALUATION CRITERIA:
{criteria_block}

ORIGINAL USER QUERY:
{query_text}

REFERENCE ANSWER:
{reference_text}

TOOL EXECUTION TRACE:
{tool_trace_text}

SUBMISSION TYPE:
{content_type}

AI-GENERATED RESPONSE:
---
{content}
---

EVALUATION GUIDELINES:

1. Answer Correctness:
Assess factual accuracy and whether claims are supported.

2. Relevance:
Assess whether the response stays focused on the subject.

3. Query Alignment:
Assess whether the response answers the original user query.
If no query was provided, return null.

4. Semantic Similarity:
Compare the response's meaning with the supplied reference answer.
Assess meaning, not just matching words.
If no reference answer was provided, return null.

5. Tone:
Assess clarity, professionalism, and suitability for the context.

6. Tool Calling:
Assess the supplied tool execution trace, including whether tool
selection and execution appear appropriate and whether outputs support
the response. Do not assume a tool was needed without evidence.
If no tool trace was provided, return null.

Do not penalize a concise response merely for being short.
Do not reward verbosity without substance.
Evaluate only the evidence available.

{JSON_INSTRUCTIONS}
"""
