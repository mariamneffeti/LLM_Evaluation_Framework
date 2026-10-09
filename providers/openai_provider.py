import os

from openai import OpenAI

from .base import BaseProvider, LLMResponse


class OpenAIProvider(BaseProvider):
    def __init__(self, model: str = "gpt-4o-mini"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required to use gpt-4o-mini")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def complete(self, question: str) -> LLMResponse:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": question}],
            max_tokens=512,
        )
        usage = response.usage
        return LLMResponse(
            text=response.choices[0].message.content or "",
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0,
        )
