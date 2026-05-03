from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet, InvalidToken


def runtime_status() -> dict[str, Any]:
    provider = os.environ.get("KRIYAX_LLM_PROVIDER") or _default_provider()
    legacy = _legacy_profile(provider)
    if provider == "anthropic":
        has_key = bool(os.environ.get("ANTHROPIC_API_KEY") or (legacy or {}).get("api_key"))
        model = os.environ.get("ANTHROPIC_MODEL") or (legacy or {}).get("model") or "claude-sonnet-4-5"
    elif provider == "kimi":
        has_key = bool(os.environ.get("KIMI_API_KEY") or (legacy or {}).get("api_key"))
        model = os.environ.get("KIMI_MODEL") or (legacy or {}).get("model") or "kimi-for-coding"
    else:
        has_key = bool(os.environ.get("OPENAI_API_KEY") or (legacy or {}).get("api_key"))
        model = os.environ.get("OPENAI_MODEL") or (legacy or {}).get("model") or "gpt-5.1"
    return {"provider": provider, "model": model, "hasApiKey": has_key, "status": "ready" if has_key else "missing_key"}


def complete_text(prompt: str) -> str:
    status = runtime_status()
    if not status["hasApiKey"]:
        raise RuntimeError("LLM key missing. Set OPENAI_API_KEY or ANTHROPIC_API_KEY.")
    if status["provider"] == "anthropic":
        return _anthropic(prompt, str(status["model"]))
    if status["provider"] == "kimi":
        return _openai_chat_compatible(prompt, str(status["model"]), provider="kimi")
    return _openai(prompt, str(status["model"]))


def _openai(prompt: str, model: str) -> str:
    from openai import OpenAI

    legacy = _legacy_profile("openai")
    api_key = os.environ.get("OPENAI_API_KEY") or (legacy or {}).get("api_key")
    base_url = os.environ.get("OPENAI_BASE_URL") or (legacy or {}).get("base_url") or None
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": "Return concise, executable Python/pandas code when code is requested."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.output_text


def _openai_chat_compatible(prompt: str, model: str, provider: str) -> str:
    from openai import OpenAI

    legacy = _legacy_profile(provider)
    api_key = os.environ.get("KIMI_API_KEY") or (legacy or {}).get("api_key")
    base_url = os.environ.get("KIMI_BASE_URL") or (legacy or {}).get("base_url") or "https://api.kimi.com/coding/"
    client = OpenAI(api_key=api_key, base_url=_openai_base_url(base_url))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Return concise, executable Python/pandas code when code is requested."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=800,
    )
    return response.choices[0].message.content or ""


def _anthropic(prompt: str, model: str) -> str:
    from anthropic import Anthropic

    legacy = _legacy_profile("anthropic")
    api_key = os.environ.get("ANTHROPIC_API_KEY") or (legacy or {}).get("api_key")
    base_url = os.environ.get("ANTHROPIC_BASE_URL") or (legacy or {}).get("base_url") or None
    client = Anthropic(api_key=api_key, base_url=_anthropic_base_url(base_url) if base_url else None)
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system="Return concise, executable Python/pandas code when code is requested.",
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in response.content if getattr(block, "type", "") == "text")


def _default_provider() -> str:
    if _legacy_profile("anthropic"):
        return "anthropic"
    if _legacy_profile("kimi"):
        return "kimi"
    return "openai"


def _legacy_profile(provider: str) -> dict[str, str] | None:
    vault_path, key_path = _legacy_paths()
    if not vault_path.exists() or not key_path.exists():
        return None
    try:
        payload = json.loads(vault_path.read_text(encoding="utf-8"))
        profile = payload.get("profiles", {}).get(provider)
        if not profile and provider == "kimi":
            profile = payload.get("profiles", {}).get("anthropic")
        if not profile and provider == "anthropic":
            profile = payload.get("profiles", {}).get("kimi")
        encrypted = profile.get("apiKey") if profile else None
        if not encrypted:
            return None
        key = key_path.read_text(encoding="utf-8").strip().encode("ascii")
        api_key = Fernet(key).decrypt(encrypted["ciphertext"].encode("ascii")).decode("utf-8")
    except (OSError, json.JSONDecodeError, InvalidToken, KeyError, AttributeError, ValueError):
        return None
    return {"api_key": api_key, "model": profile.get("model") or "", "base_url": profile.get("baseUrl") or ""}


def _legacy_paths() -> tuple[Path, Path]:
    configured = os.environ.get("KRIYAX_LEGACY_LLM_METADATA")
    if configured:
        root = Path(configured).expanduser().resolve()
    else:
        root = Path(__file__).resolve().parents[3] / "kriyax-data-app" / "workspace" / "metadata"
    return root / "llm-settings.vault", root / "llm-master.key"


def _anthropic_base_url(base_url: str) -> str:
    cleaned = base_url.rstrip("/")
    for suffix in ["/v1/messages", "/messages", "/v1"]:
        if cleaned.endswith(suffix):
            return cleaned[: -len(suffix)]
    return cleaned


def _openai_base_url(base_url: str) -> str:
    cleaned = base_url.rstrip("/")
    suffix = "/chat/completions"
    if cleaned.endswith(suffix):
        return cleaned[: -len(suffix)]
    return cleaned
