from typing import Any

from fastapi import HTTPException

from app.llm.schemas import LLMTestRequest
from app.services import developer_llm
from app.llm.schemas import LlmProvider


def runtime_status(provider: LlmProvider | None = None) -> dict[str, Any]:
    return developer_llm.runtime_status(provider)


def playground(prompt: str, provider: LlmProvider | None = None, model: str | None = None) -> dict[str, Any]:
    result = developer_llm.playground(LLMTestRequest(provider=provider, model=model, message=prompt))
    return {
        "provider": result["provider"],
        "model": result["model"],
        "latencyMs": result["latency_ms"],
        "status": "success" if result["success"] else "error",
        "responseText": result["response"] or result["error"] or "",
    }


def complete_text(prompt: str, provider: LlmProvider | None = None) -> str | None:
    try:
        return developer_llm.complete_text(prompt, provider=provider)
    except HTTPException as exc:
        if isinstance(exc.detail, dict) and exc.detail.get("code") == "LLM_KEY_MISSING":
            return None
        raise
    except ValueError as exc:
        if "LLM_KEY_MISSING" in str(exc):
            return None
        raise
    except RuntimeError:
        raise
        return None
