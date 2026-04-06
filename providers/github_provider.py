from .base import BaseProvider, LLMResponse
import os
import requests
from dotenv import load_dotenv
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

class GithubModelsProvider(BaseProvider):
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        self.base_url = "https://models.inference.ai.azure.com"
        self.api_key = GITHUB_TOKEN
    def complete(self, question: str) -> LLMResponse:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "messages": [
                {"role": "user", "content": question}
            ],
            "model": self.model,
            "max_tokens": 512,
            "temperature": 1
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            usage = data.get("usage", {})
            choice = data.get("choices", [{}])[0]
            message = choice.get("message", {})
            
            return LLMResponse(
                input_tokens=usage.get("prompt_tokens", 0),
                output_tokens=usage.get("completion_tokens", 0),
                text=message.get("content", "")
            )
        except Exception as e:
            print(f"GitHub Models API error: {e}")
            return LLMResponse(
                input_tokens=0,
                output_tokens=0,
                text=f"Error: {str(e)}"
            )