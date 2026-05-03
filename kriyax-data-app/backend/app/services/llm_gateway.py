from typing import Any

from app.llm.schemas import LLMTestRequest
from app.services import developer_llm
from app.services.llm_settings import settings_summary
from app.services.llm_settings import Provider


def runtime_status(provider: Provider | None = None) -> dict[str, Any]:
    selected = provider
    if not selected:
        legacy_settings = settings_summary()
        selected = legacy_settings.get("activeProvider") or legacy_settings.get("defaultProvider")
    return developer_llm.runtime_status(selected)


def playground(prompt: str, provider: Provider | None = None, model: str | None = None) -> dict[str, Any]:
    result = developer_llm.playground(LLMTestRequest(provider=provider, model=model, message=prompt))
    return {
        "provider": result["provider"],
        "model": result["model"],
        "latencyMs": result["latency_ms"],
        "status": "success" if result["success"] else "error",
        "responseText": result["response"] or result["error"] or "",
    }


def complete_text(prompt: str, provider: Provider | None = None) -> str | None:
    try:
        return developer_llm.complete_text(prompt, provider=provider)
    except Exception:
        return None
