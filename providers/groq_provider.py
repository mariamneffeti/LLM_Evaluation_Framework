from groq import Groq
from .base import BaseProvider, LLMResponse
import os
from dotenv import load_dotenv

load_dotenv()

class GroqProvider(BaseProvider):
    def __init__(self, api_key: str = None, model: str = "openai/gpt-oss-20b"):
        # Ensure API key is set as environment variable for Groq
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
        self.client = Groq()  # Groq will use GROQ_API_KEY from env
        self.model = model

    def complete(self, question: str) -> LLMResponse:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": question}
            ],
            max_completion_tokens=512
        )
        return LLMResponse(
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
            text=response.choices[0].message.content
        )
