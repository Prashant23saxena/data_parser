import json
import os
from datetime import datetime, timezone
from typing import Any, Literal

from cryptography.fernet import Fernet, InvalidToken

from app.services.workspace import ensure_workspace, workspace_paths


Provider = Literal["openai", "anthropic"]

SUPPORTED_PROVIDERS: dict[Provider, dict[str, str]] = {
    "openai": {
        "label": "OpenAI",
        "defaultModel": "gpt-4.1-mini",
        "defaultBaseUrl": "https://api.openai.com/v1",
    },
    "anthropic": {
        "label": "Anthropic",
        "defaultModel": "claude-3-5-sonnet-latest",
        "defaultBaseUrl": "https://api.anthropic.com/v1",
    },
}


def settings_summary() -> dict[str, Any]:
    vault = _read_vault()
    profiles = []
    for provider, defaults in SUPPORTED_PROVIDERS.items():
        profile = vault["profiles"].get(provider, {})
        profiles.append(
            {
                "provider": provider,
                "label": profile.get("label") or defaults["label"],
                "model": profile.get("model") or defaults["defaultModel"],
                "baseUrl": profile.get("baseUrl") or defaults["defaultBaseUrl"],
                "hasApiKey": bool(profile.get("apiKey")),
                "updatedAt": profile.get("updatedAt"),
                "isDefault": vault.get("defaultProvider") == provider,
                "isActive": vault.get("activeProvider") == provider,
            }
        )

    paths = workspace_paths()
    return {
        "supportedProviders": [
            {"provider": provider, **defaults} for provider, defaults in SUPPORTED_PROVIDERS.items()
        ],
        "profiles": profiles,
        "defaultProvider": vault.get("defaultProvider"),
        "activeProvider": vault.get("activeProvider"),
        "vaultPath": str(paths["llm_settings"]),
        "masterKeyPath": str(paths["llm_master_key"]),
        "encryption": "fernet-v1",
    }


def save_profile(
    provider: Provider,
    *,
    label: str | None = None,
    model: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    set_default: bool = True,
    set_active: bool = True,
    remove_api_key: bool = False,
) -> dict[str, Any]:
    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError("Unsupported LLM provider.")

    vault = _read_vault()
    defaults = SUPPORTED_PROVIDERS[provider]
    existing = vault["profiles"].get(provider, {})
    encrypted_key = existing.get("apiKey")
    if remove_api_key:
        encrypted_key = None
    elif api_key and api_key.strip():
        encrypted_key = _encrypt(api_key.strip())

    vault["profiles"][provider] = {
        "provider": provider,
        "label": label.strip() if label and label.strip() else defaults["label"],
        "model": model.strip() if model and model.strip() else defaults["defaultModel"],
        "baseUrl": base_url.strip() if base_url and base_url.strip() else defaults["defaultBaseUrl"],
        "apiKey": encrypted_key,
        "updatedAt": _now(),
    }
    if set_default:
        vault["defaultProvider"] = provider
    if set_active:
        vault["activeProvider"] = provider
    _write_vault(vault)
    return _profile_summary(provider, vault)


def validate_profile(provider: Provider) -> dict[str, Any]:
    vault = _read_vault()
    profile = vault["profiles"].get(provider)
    if not profile:
        return {
            "provider": provider,
            "status": "missing",
            "message": f"{SUPPORTED_PROVIDERS[provider]['label']} is not configured yet.",
        }

    if not profile.get("apiKey"):
        return {
            "provider": provider,
            "status": "missing_key",
            "message": f"{profile['label']} is saved, but no API key is stored.",
        }

    return {
        "provider": provider,
        "status": "ready",
        "message": f"{profile['label']} key is encrypted locally and ready for runtime use.",
        "model": profile["model"],
        "baseUrl": profile["baseUrl"],
    }


def get_runtime_profile(provider: Provider | None = None) -> dict[str, str] | None:
    vault = _read_vault()
    selected = provider or vault.get("activeProvider") or vault.get("defaultProvider")
    if not selected:
        return None
    profile = vault["profiles"].get(selected)
    if not profile or not profile.get("apiKey"):
        return None
    return {
        "provider": selected,
        "label": profile["label"],
        "model": profile["model"],
        "baseUrl": profile["baseUrl"],
        "apiKey": _decrypt(profile["apiKey"]),
    }


def _profile_summary(provider: Provider, vault: dict[str, Any]) -> dict[str, Any]:
    profile = vault["profiles"][provider]
    return {
        "provider": provider,
        "label": profile["label"],
        "model": profile["model"],
        "baseUrl": profile["baseUrl"],
        "hasApiKey": bool(profile.get("apiKey")),
        "updatedAt": profile["updatedAt"],
        "isDefault": vault.get("defaultProvider") == provider,
        "isActive": vault.get("activeProvider") == provider,
    }


def _empty_vault() -> dict[str, Any]:
    return {
        "version": 1,
        "defaultProvider": None,
        "activeProvider": None,
        "profiles": {},
    }


def _read_vault() -> dict[str, Any]:
    ensure_workspace()
    path = workspace_paths()["llm_settings"]
    if not path.exists():
        return _empty_vault()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return _empty_vault()
    if not isinstance(payload.get("profiles"), dict):
        payload["profiles"] = {}
    return {**_empty_vault(), **payload}


def _write_vault(vault: dict[str, Any]) -> None:
    ensure_workspace()
    path = workspace_paths()["llm_settings"]
    path.write_text(json.dumps(vault, indent=2) + "\n", encoding="utf-8")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def _master_key() -> bytes:
    ensure_workspace()
    path = workspace_paths()["llm_master_key"]
    if path.exists():
        return path.read_text(encoding="utf-8").strip().encode("ascii")
    key = Fernet.generate_key()
    path.write_text(key.decode("ascii"), encoding="utf-8")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return key


def _encrypt(secret: str) -> dict[str, str]:
    return {
        "version": "fernet-v1",
        "ciphertext": Fernet(_master_key()).encrypt(secret.encode("utf-8")).decode("ascii"),
    }


def _decrypt(payload: dict[str, str]) -> str:
    try:
        plaintext = Fernet(_master_key()).decrypt(payload["ciphertext"].encode("ascii"))
    except InvalidToken as exc:
        raise ValueError("Encrypted LLM key failed integrity validation.")
    except KeyError as exc:
        raise ValueError("Encrypted LLM key payload is incomplete.") from exc
    return plaintext.decode("utf-8")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
