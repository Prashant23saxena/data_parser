from typing import Literal

from pydantic import BaseModel, Field


LlmProvider = Literal["openai", "kimi", "anthropic", "azure-openai"]


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatCompletionRequest(BaseModel):
    provider: LlmProvider | None = None
    model: str | None = None
    messages: list[Message]
    temperature: float | None = 0.2
    max_tokens: int | None = 800
    timeout_ms: int | None = 30000


class LLMTestRequest(BaseModel):
    provider: LlmProvider | None = None
    model: str | None = None
    message: str = Field(default="Say OK for the LLM test runner.", min_length=1)


class VaultKeyRequest(BaseModel):
    provider: LlmProvider
    api_key: str = Field(min_length=1)
    model: str | None = None
    base_url: str | None = None


class LLMProfileCreate(BaseModel):
    label: str = Field(min_length=1)
    provider: LlmProvider
    model: str | None = None
    base_url: str | None = None
    is_enabled: bool = True
