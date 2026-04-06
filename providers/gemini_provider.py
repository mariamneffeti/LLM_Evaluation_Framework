from .base import BaseProvider, LLMResponse
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
genai.api_key = os.getenv("GOOGLE_API_KEY")


class GeminiProvider(BaseProvider):
    def __init__(self, model="gemini-2.0-flash"):
        genai.configure(api_key=genai.api_key)
        self.model = genai.GenerativeModel(model)
        self.model_name = model
    def complete(self, question: str) -> LLMResponse:
        resp = self.model.generate_content(question)
        return LLMResponse(
            text=resp.text,
            input_tokens=resp.usage_metadata.prompt_token_count,
            output_tokens=resp.usage_metadata.candidates_token_count
        )