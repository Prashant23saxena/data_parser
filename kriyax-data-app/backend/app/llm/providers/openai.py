from urllib.parse import urlparse, urlunparse

from openai import OpenAI

from app.llm.providers.base import BaseLLMProvider
from app.llm.schemas import ChatCompletionRequest


class OpenAICompatibleProvider(BaseLLMProvider):
    def __init__(self, *, api_key: str, model: str, base_url: str, timeout_ms: int = 30000) -> None:
        self.api_key = api_key
        self.model = model
        self.base_url = _sdk_base_url(base_url)
        self.timeout = timeout_ms / 1000

    def chat_completion(self, request: ChatCompletionRequest) -> str:
        client = OpenAI(api_key=self.api_key, base_url=self.base_url, timeout=request.timeout_ms / 1000 if request.timeout_ms else self.timeout)
        completion = client.chat.completions.create(
            model=request.model or self.model,
            messages=[{"role": message.role, "content": message.content} for message in request.messages],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return completion.choices[0].message.content or ""


def _sdk_base_url(base_url: str) -> str:
    cleaned = base_url.rstrip("/")
    suffix = "/chat/completions"
    if cleaned.endswith(suffix):
        return cleaned[: -len(suffix)]
    parsed = urlparse(cleaned)
    if parsed.netloc.endswith(".openai.azure.com") and not parsed.path.rstrip("/").endswith("/openai/v1"):
        return urlunparse(parsed._replace(path=parsed.path.rstrip("/") + "/openai/v1"))
    return cleaned
