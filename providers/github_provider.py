from .base import BaseProvider, LLMResponse

class GithubModelsProvider(BaseProvider):
    def __init__(self, model="gpt-4o-mini"):
        self.model = model

    def complete(self, question: str) -> LLMResponse:
        raise RuntimeError(
            "GitHub Models inference was retired on July 30, 2026; "
            "this provider cannot return benchmark results or token usage."
        )
