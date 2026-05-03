from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.core.config import SUPPORTED_LLM_PROVIDERS, default_llm_provider
from app.llm.schemas import LLMProfileCreate, LLMTestRequest, LlmProvider
from app.services import developer_llm


class LlmProfilePayload(BaseModel):
    provider: LlmProvider
    label: str | None = None
    model: str | None = None
    baseUrl: str | None = None
    apiKey: str | None = Field(default=None, min_length=1)
    setDefault: bool = True
    setActive: bool = True
    removeApiKey: bool = False


class LlmTestPayload(BaseModel):
    provider: LlmProvider


class LlmPlaygroundPayload(BaseModel):
    prompt: str = Field(min_length=1)
    provider: LlmProvider | None = None
    model: str | None = None


router = APIRouter()


@router.get("/settings")
def get_llm_settings() -> dict[str, object]:
    return _settings_summary()


@router.post("/settings")
def save_llm_settings(payload: LlmProfilePayload) -> dict[str, object]:
    try:
        if payload.apiKey and not payload.removeApiKey:
            developer_llm.save_vault_key(
                payload.provider,
                api_key=payload.apiKey,
                model=payload.model,
                base_url=payload.baseUrl,
            )
        profile = developer_llm.create_profile(
            LLMProfileCreate(
                label=payload.label or SUPPORTED_LLM_PROVIDERS[payload.provider].label,
                provider=payload.provider,
                model=payload.model,
                base_url=payload.baseUrl,
                is_enabled=True,
            )
        )
        if payload.setDefault or payload.setActive:
            profile = developer_llm.set_default_profile(profile["id"])
        config = developer_llm.get_config(payload.provider)
        return {
            "profile": _legacy_profile_summary(profile, config),
            "settings": _settings_summary(),
        }
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/test")
def test_llm_settings(payload: LlmTestPayload) -> dict[str, object]:
    config = developer_llm.get_config(payload.provider)
    if config["masked_key_status"] == "missing":
        return {
            "provider": payload.provider,
            "status": "missing_key",
            "message": "Configure an API key before running LLM tests.",
        }
    return {
        "provider": payload.provider,
        "status": "ready",
        "message": "Provider key is configured.",
        "model": config["model"],
        "baseUrl": config["base_url"],
    }


@router.get("/status")
def get_llm_status() -> dict[str, object]:
    return developer_llm.runtime_status()


@router.post("/playground")
def run_llm_playground(payload: LlmPlaygroundPayload) -> dict[str, object]:
    try:
        result = developer_llm.playground(
            LLMTestRequest(provider=payload.provider, model=payload.model, message=payload.prompt)
        )
        return {
            "provider": result["provider"],
            "model": result["model"],
            "latencyMs": result["latency_ms"],
            "status": "success" if result["success"] else "error",
            "responseText": result["response"] or result["error"] or "",
        }
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Provider request failed: {exc}") from exc


def _settings_summary() -> dict[str, Any]:
    sql_profiles = developer_llm.list_profiles()
    default_profile = next((profile for profile in sql_profiles if profile["is_default"]), None)
    default_provider = (default_profile or {}).get("provider") or default_llm_provider()
    provider_rows = []
    for provider, defaults in SUPPORTED_LLM_PROVIDERS.items():
        config = developer_llm.get_config(provider)
        matching_profile = next((profile for profile in sql_profiles if profile["provider"] == provider and profile["is_default"]), None)
        matching_profile = matching_profile or next((profile for profile in sql_profiles if profile["provider"] == provider), None)
        provider_rows.append(
            {
                "provider": provider,
                "label": (matching_profile or {}).get("label") or defaults.label,
                "model": config["model"],
                "baseUrl": config["base_url"],
                "hasApiKey": config["masked_key_status"] != "missing",
                "updatedAt": (matching_profile or {}).get("updated_at"),
                "isDefault": default_provider == provider,
                "isActive": default_provider == provider,
            }
        )
    return {
        "supportedProviders": [
            {
                "provider": provider,
                "label": defaults.label,
                "defaultModel": defaults.model,
                "defaultBaseUrl": defaults.base_url,
            }
            for provider, defaults in SUPPORTED_LLM_PROVIDERS.items()
        ],
        "profiles": provider_rows,
        "savedProfiles": sql_profiles,
        "defaultProvider": default_provider,
        "activeProvider": default_provider,
        "encryption": "fernet-v1",
        "storage": "developer-control-plane",
    }


def _legacy_profile_summary(profile: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": profile["id"],
        "provider": profile["provider"],
        "label": profile["label"],
        "model": profile["model"],
        "baseUrl": profile["base_url"],
        "hasApiKey": config["masked_key_status"] != "missing",
        "updatedAt": profile["updated_at"],
        "isDefault": profile["is_default"],
        "isActive": profile["is_default"],
    }
