from .base import BaseProvider, LLMResponse
import os
from google import genai


class GeminiProvider(BaseProvider):
    def __init__(self, model="gemini-3.8-flash"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is required to use Gemini")
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def complete(self, question: str) -> LLMResponse:
        resp = self.client.models.generate_content(model=self.model, contents=question)
        usage = resp.usage_metadata
        return LLMResponse(
            text=resp.text or "",
            input_tokens=getattr(usage, "prompt_token_count", 0) or 0,
            output_tokens=getattr(usage, "candidates_token_count", 0) or 0,
        )
