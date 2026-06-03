import json

from openai import OpenAI

from app.core.config import OPENAI_API_KEY
from app.prompts.judge_prompt import SYSTEM_PROMPT


class LLMEvaluator:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)


    def evaluate(
        self,
        question: str,
        reference_answer: str,
        model_answer: str
    ):
        user_prompt = f'''
        Question:
        {question}

        Reference Answer:
        {reference_answer}

        Candidate Answer:
        {model_answer}
        '''

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0
        )

        content = response.choices[0].message.content

        try:
            parsed = json.loads(content)
        except Exception:
            parsed = {
                "raw_response": content
            }

        return parsed
