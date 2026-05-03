from abc import ABC, abstractmethod

from app.llm.schemas import ChatCompletionRequest


class BaseLLMProvider(ABC):
    @abstractmethod
    def chat_completion(self, request: ChatCompletionRequest) -> str:
        raise NotImplementedError
