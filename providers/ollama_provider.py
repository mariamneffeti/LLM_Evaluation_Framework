from .base import BaseProvider, LLMResponse
import requests
import os


class OllamaProvider(BaseProvider):
    def __init__(self, model="llama3.1:8b", base_url=None):
        self.model = model
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    def complete(self, question: str) -> LLMResponse:
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "stream": False,
                "messages": [
                    {"role": "user", "content": question}
                ]
            }
        )
        response_data = response.json()
        return LLMResponse(
            input_tokens=response_data.get("prompt_eval_count", 0),
            output_tokens=response_data.get("eval_count", 0),
            text=response_data["message"]["content"]
        )
