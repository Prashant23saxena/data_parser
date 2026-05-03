from __future__ import annotations

import os
import sqlite3
import time
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import HTTPException

from app.core.config import SUPPORTED_LLM_PROVIDERS, default_llm_provider, env_value, provider_default
from app.llm.providers.anthropic import AnthropicProvider
from app.llm.providers.base import BaseLLMProvider
from app.llm.providers.openai import OpenAICompatibleProvider
from app.llm.schemas import ChatCompletionRequest, LLMProfileCreate, LLMTestRequest, Message
from app.llm.secrets import clear_vault as clear_secret_vault
from app.llm.secrets import get_provider_secret, mask_secret, save_provider_secret
from app.services.workspace import ensure_workspace, workspace_paths


TENANT_ID = "default"


def get_config(provider: str | None = None) -> dict[str, Any]:
    selected = _coerce_provider(provider or default_llm_provider())
    defaults = provider_default(selected)
    env_key = env_value(defaults.api_key_env)
    env_model = env_value(defaults.model_env)
    env_base_url = env_value(defaults.base_url_env)
    secret, secret_source = get_provider_secret(selected)
    api_key = env_key or (secret or {}).get("api_key")
    source = "env" if env_key else secret_source or "missing"
    return {
        "provider": selected,
        "model": env_model or (secret or {}).get("model") or defaults.model,
        "base_url": env_base_url or (secret or {}).get("base_url") or defaults.base_url,
        "masked_key_status": mask_secret(api_key),
        "source": source,
    }


def save_vault_key(provider: str, *, api_key: str, model: str | None = None, base_url: str | None = None) -> dict[str, Any]:
    selected = _coerce_provider(provider)
    defaults = provider_default(selected)
    result = save_provider_secret(
        selected,
        api_key=api_key,
        model=model or defaults.model,
        base_url=base_url or defaults.base_url,
    )
    return {**get_config(selected), **result}


def list_profiles() -> list[dict[str, Any]]:
    _ensure_db()
    with _connect() as conn:
        rows = conn.execute(
            "select id, tenant_id, label, provider, model, base_url, is_default, is_enabled, created_at, updated_at "
            "from llm_profile where tenant_id = ? order by is_default desc, updated_at desc",
            (TENANT_ID,),
        ).fetchall()
    return [_profile_row(row) for row in rows]


def create_profile(payload: LLMProfileCreate) -> dict[str, Any]:
    _ensure_db()
    defaults = provider_default(payload.provider)
    now = _now()
    profile_id = uuid4().hex
    with _connect() as conn:
        conn.execute(
            "insert into llm_profile (id, tenant_id, label, provider, model, base_url, is_default, is_enabled, created_at, updated_at) "
            "values (?, ?, ?, ?, ?, ?, 0, ?, ?, ?)",
            (
                profile_id,
                TENANT_ID,
                payload.label,
                payload.provider,
                payload.model or defaults.model,
                payload.base_url or defaults.base_url,
                1 if payload.is_enabled else 0,
                now,
                now,
            ),
        )
    return get_profile(profile_id)


def get_profile(profile_id: str) -> dict[str, Any]:
    _ensure_db()
    with _connect() as conn:
        row = conn.execute(
            "select id, tenant_id, label, provider, model, base_url, is_default, is_enabled, created_at, updated_at "
            "from llm_profile where id = ? and tenant_id = ?",
            (profile_id, TENANT_ID),
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="LLM profile not found.")
    return _profile_row(row)


def set_default_profile(profile_id: str) -> dict[str, Any]:
    profile = get_profile(profile_id)
    now = _now()
    with _connect() as conn:
        conn.execute("update llm_profile set is_default = 0 where tenant_id = ?", (TENANT_ID,))
        conn.execute(
            "update llm_profile set is_default = 1, updated_at = ? where id = ? and tenant_id = ?",
            (now, profile_id, TENANT_ID),
        )
    return get_profile(profile_id)


def delete_profile(profile_id: str) -> dict[str, bool]:
    _ensure_db()
    with _connect() as conn:
        cursor = conn.execute("delete from llm_profile where id = ? and tenant_id = ?", (profile_id, TENANT_ID))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="LLM profile not found.")
    return {"deleted": True}


def list_audit(limit: int = 50) -> dict[str, list[dict[str, Any]]]:
    _ensure_db()
    with _connect() as conn:
        rows = conn.execute(
            "select id, provider, model, latency_ms, success, error_message, request_preview, response_preview, created_at "
            "from llm_audit_log where tenant_id = ? order by created_at desc limit ?",
            (TENANT_ID, limit),
        ).fetchall()
    return {"items": [_audit_row(row) for row in rows]}


def clear_vault() -> dict[str, bool]:
    clear_secret_vault()
    return {"cleared": True}


def test_llm(payload: LLMTestRequest) -> dict[str, Any]:
    selected = _coerce_provider(payload.provider or _default_profile_provider() or default_llm_provider())
    config = _resolved_provider_config(selected, model_override=payload.model)
    request = ChatCompletionRequest(
        provider=selected,
        model=config["model"],
        messages=[Message(role="user", content=payload.message)],
    )
    return execute_chat(request, config=config, request_preview=payload.message)


def playground(payload: LLMTestRequest) -> dict[str, Any]:
    return test_llm(payload)


def complete_chat(request: ChatCompletionRequest) -> str:
    selected = _coerce_provider(request.provider or _default_profile_provider() or default_llm_provider())
    config = _resolved_provider_config(selected, model_override=request.model)
    adapter = _build_provider(selected, config)
    return adapter.chat_completion(request.model_copy(update={"provider": selected, "model": config["model"]}))


def complete_text(prompt: str, provider: str | None = None) -> str:
    selected = _coerce_provider(provider or _default_profile_provider() or default_llm_provider())
    config = _resolved_provider_config(selected)
    request = ChatCompletionRequest(
        provider=selected,
        model=config["model"],
        messages=[
            Message(role="system", content="You are a concise Python data-workspace assistant."),
            Message(role="user", content=prompt),
        ],
    )
    result = execute_chat(request, config=config, request_preview=prompt)
    if not result["success"]:
        raise RuntimeError(result["error"] or "Provider request failed.")
    return str(result["response"] or "")


def runtime_status(provider: str | None = None) -> dict[str, Any]:
    config = get_config(provider or _default_profile_provider() or default_llm_provider())
    return {
        "provider": config["provider"],
        "label": provider_default(config["provider"]).label,
        "model": config["model"],
        "hasApiKey": config["masked_key_status"] != "missing",
        "status": "ready" if config["masked_key_status"] != "missing" else "missing_key",
        "message": "Provider key is configured." if config["masked_key_status"] != "missing" else "Configure an API key before running LLM tests.",
    }


def execute_chat(request: ChatCompletionRequest, *, config: dict[str, str], request_preview: str) -> dict[str, Any]:
    started = time.perf_counter()
    provider = _coerce_provider(config["provider"])
    try:
        response_text = complete_chat(request)
        latency_ms = round((time.perf_counter() - started) * 1000, 2)
        _write_audit(provider, config["model"], latency_ms, True, None, request_preview, response_text)
        return {
            "provider": provider,
            "model": config["model"],
            "response": response_text,
            "latency_ms": latency_ms,
            "success": True,
            "error": None,
        }
    except HTTPException:
        raise
    except Exception as exc:
        latency_ms = round((time.perf_counter() - started) * 1000, 2)
        _write_audit(provider, config["model"], latency_ms, False, str(exc), request_preview, None)
        return {
            "provider": provider,
            "model": config["model"],
            "response": None,
            "latency_ms": latency_ms,
            "success": False,
            "error": str(exc),
        }


def _resolved_provider_config(provider: str, *, model_override: str | None = None) -> dict[str, str]:
    selected = _coerce_provider(provider)
    defaults = provider_default(selected)
    secret, source = get_provider_secret(selected)
    env_key = env_value(defaults.api_key_env)
    api_key = env_key or (secret or {}).get("api_key")
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail={"code": "LLM_KEY_MISSING", "message": "Configure an API key before running LLM tests."},
        )
    profile = _default_profile_for_provider(selected)
    return {
        "provider": selected,
        "api_key": api_key,
        "model": model_override
        or env_value(defaults.model_env)
        or (profile or {}).get("model")
        or (secret or {}).get("model")
        or defaults.model,
        "base_url": env_value(defaults.base_url_env)
        or (profile or {}).get("base_url")
        or (secret or {}).get("base_url")
        or defaults.base_url,
        "source": "env" if env_key else source or "missing",
    }


def _build_provider(provider: str, config: dict[str, str]) -> BaseLLMProvider:
    if provider in {"openai", "kimi", "azure-openai"}:
        return OpenAICompatibleProvider(api_key=config["api_key"], model=config["model"], base_url=config["base_url"])
    if provider == "anthropic":
        return AnthropicProvider(api_key=config["api_key"], model=config["model"], base_url=config["base_url"])
    raise ValueError("Unsupported LLM provider.")


def _default_profile_provider() -> str | None:
    _ensure_db()
    with _connect() as conn:
        row = conn.execute(
            "select provider from llm_profile where tenant_id = ? and is_default = 1 and is_enabled = 1 limit 1",
            (TENANT_ID,),
        ).fetchone()
    return row[0] if row else None


def _default_profile_for_provider(provider: str) -> dict[str, str] | None:
    _ensure_db()
    with _connect() as conn:
        row = conn.execute(
            "select model, base_url from llm_profile where tenant_id = ? and provider = ? and is_default = 1 and is_enabled = 1 limit 1",
            (TENANT_ID, provider),
        ).fetchone()
    return {"model": row[0], "base_url": row[1]} if row else None


def _write_audit(provider: str, model: str, latency_ms: float, success: bool, error: str | None, request_preview: str, response_preview: str | None) -> None:
    _ensure_db()
    with _connect() as conn:
        conn.execute(
            "insert into llm_audit_log (id, tenant_id, provider, model, latency_ms, success, error_message, request_preview, response_preview, created_at) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                uuid4().hex,
                TENANT_ID,
                provider,
                model,
                latency_ms,
                1 if success else 0,
                error,
                _redact(request_preview),
                _redact(response_preview or ""),
                _now(),
            ),
        )


def _connect() -> sqlite3.Connection:
    ensure_workspace()
    conn = sqlite3.connect(str(workspace_paths()["metadata"] / "llm-control-plane.sqlite"))
    return conn


def _ensure_db() -> None:
    ensure_workspace()
    with _connect() as conn:
        conn.execute(
            "create table if not exists llm_profile ("
            "id text primary key, tenant_id text not null, label text not null, provider text not null, "
            "model text not null, base_url text not null, is_default integer not null default 0, "
            "is_enabled integer not null default 1, created_at text not null, updated_at text not null)"
        )
        conn.execute(
            "create table if not exists llm_audit_log ("
            "id text primary key, tenant_id text not null, provider text not null, model text not null, "
            "latency_ms real not null, success integer not null, error_message text, request_preview text, "
            "response_preview text, created_at text not null)"
        )


def _profile_row(row: sqlite3.Row | tuple[Any, ...]) -> dict[str, Any]:
    return {
        "id": row[0],
        "tenant_id": row[1],
        "label": row[2],
        "provider": row[3],
        "model": row[4],
        "base_url": row[5],
        "is_default": bool(row[6]),
        "is_enabled": bool(row[7]),
        "created_at": row[8],
        "updated_at": row[9],
    }


def _audit_row(row: sqlite3.Row | tuple[Any, ...]) -> dict[str, Any]:
    return {
        "id": row[0],
        "provider": row[1],
        "model": row[2],
        "latency_ms": row[3],
        "success": bool(row[4]),
        "error_message": row[5],
        "request_preview": row[6],
        "response_preview": row[7],
        "created_at": row[8],
    }


def _coerce_provider(provider: str) -> str:
    if provider not in SUPPORTED_LLM_PROVIDERS:
        raise HTTPException(status_code=400, detail="Unsupported LLM provider.")
    return provider


def _redact(value: str) -> str:
    if not value:
        return ""
    redacted = value[:500]
    for name in ["OPENAI_API_KEY", "KIMI_API_KEY", "ANTHROPIC_API_KEY", "AZURE_OPENAI_API_KEY"]:
        secret = os.environ.get(name)
        if secret:
            redacted = redacted.replace(secret, "[redacted]")
    return redacted


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
