from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services import llm_gateway
from app.services.llm_settings import save_profile, settings_summary, validate_profile


Provider = Literal["openai", "anthropic"]


class LlmProfilePayload(BaseModel):
    provider: Provider
    label: str | None = None
    model: str | None = None
    baseUrl: str | None = None
    apiKey: str | None = Field(default=None, min_length=1)
    setDefault: bool = True
    setActive: bool = True
    removeApiKey: bool = False


class LlmTestPayload(BaseModel):
    provider: Provider


class LlmPlaygroundPayload(BaseModel):
    prompt: str = Field(min_length=1)
    provider: Provider | None = None
    model: str | None = None


router = APIRouter()


@router.get("/settings")
def get_llm_settings() -> dict[str, object]:
    return settings_summary()


@router.post("/settings")
def save_llm_settings(payload: LlmProfilePayload) -> dict[str, object]:
    try:
        profile = save_profile(
            payload.provider,
            label=payload.label,
            model=payload.model,
            base_url=payload.baseUrl,
            api_key=payload.apiKey,
            set_default=payload.setDefault,
            set_active=payload.setActive,
            remove_api_key=payload.removeApiKey,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"profile": profile, "settings": settings_summary()}


@router.post("/test")
def test_llm_settings(payload: LlmTestPayload) -> dict[str, object]:
    return validate_profile(payload.provider)


@router.get("/status")
def get_llm_status() -> dict[str, object]:
    return llm_gateway.runtime_status()


@router.post("/playground")
def run_llm_playground(payload: LlmPlaygroundPayload) -> dict[str, object]:
    try:
        return llm_gateway.playground(payload.prompt, provider=payload.provider, model=payload.model)
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Provider request failed: {exc}") from exc
