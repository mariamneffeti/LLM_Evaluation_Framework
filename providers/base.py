from abc import ABC, abstractmethod
from dataclasses import dataclass



@dataclass
class LLMResponse:
    input_tokens: int
    output_tokens: int
    text : str
class BaseProvider(ABC):
    @abstractmethod
    def complete(self, question: str) -> LLMResponse:
        pass