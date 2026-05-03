from anthropic import Anthropic

from app.llm.providers.base import BaseLLMProvider
from app.llm.schemas import ChatCompletionRequest


class AnthropicProvider(BaseLLMProvider):
    def __init__(self, *, api_key: str, model: str, base_url: str, timeout_ms: int = 30000) -> None:
        self.api_key = api_key
        self.model = model
        self.base_url = _sdk_base_url(base_url)
        self.timeout = timeout_ms / 1000

    def chat_completion(self, request: ChatCompletionRequest) -> str:
        system_messages = [message.content for message in request.messages if message.role == "system"]
        chat_messages = [
            {"role": message.role, "content": message.content}
            for message in request.messages
            if message.role in {"user", "assistant"}
        ]
        client = Anthropic(api_key=self.api_key, base_url=self.base_url, timeout=request.timeout_ms / 1000 if request.timeout_ms else self.timeout)
        response = client.messages.create(
            model=request.model or self.model,
            max_tokens=request.max_tokens or 800,
            temperature=request.temperature,
            system="\n".join(system_messages) if system_messages else None,
            messages=chat_messages,
        )
        return "\n".join(block.text for block in response.content if getattr(block, "type", None) == "text").strip()


def _sdk_base_url(base_url: str) -> str:
    cleaned = base_url.rstrip("/")
    if cleaned.endswith("/v1/messages"):
        return cleaned[: -len("/v1/messages")]
    if cleaned.endswith("/messages"):
        return cleaned[: -len("/messages")]
    if cleaned.endswith("/v1"):
        return cleaned[: -len("/v1")]
    return cleaned
