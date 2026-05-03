import json
import os
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet, InvalidToken

from app.core.config import local_secret_master_key_path, local_secret_vault_path
from app.services.workspace import ensure_workspace, workspace_paths


def save_provider_secret(provider: str, *, api_key: str, model: str | None = None, base_url: str | None = None) -> dict[str, str]:
    vault = _read_vault()
    vault[provider] = {
        "api_key": api_key,
        "model": model or vault.get(provider, {}).get("model") or "",
        "base_url": base_url or vault.get(provider, {}).get("base_url") or "",
    }
    _write_vault(vault)
    return {"provider": provider, "source": "vault", "masked_key_status": mask_secret(api_key)}


def get_provider_secret(provider: str) -> tuple[dict[str, str] | None, str | None]:
    vault = _read_vault()
    if provider in vault and vault[provider].get("api_key"):
        return vault[provider], "vault"
    legacy = _read_legacy_provider_secret(provider)
    if legacy:
        return legacy, "vault"
    return None, None


def clear_vault() -> None:
    path = local_secret_vault_path()
    if path.exists():
        path.unlink()


def mask_secret(secret: str | None) -> str:
    if not secret:
        return "missing"
    if len(secret) <= 8:
        return "set"
    return f"{secret[:3]}...{secret[-4:]}"


def _read_vault() -> dict[str, dict[str, str]]:
    path = local_secret_vault_path()
    if not path.exists():
        return {}
    try:
        raw = Fernet(_master_key()).decrypt(path.read_bytes())
        payload = json.loads(raw.decode("utf-8"))
    except (InvalidToken, json.JSONDecodeError, OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _write_vault(payload: dict[str, dict[str, str]]) -> None:
    path = local_secret_vault_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(Fernet(_master_key()).encrypt(json.dumps(payload).encode("utf-8")))
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def _master_key() -> bytes:
    path = local_secret_master_key_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return path.read_text(encoding="utf-8").strip().encode("ascii")
    key = Fernet.generate_key()
    path.write_text(key.decode("ascii"), encoding="utf-8")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return key


def _read_legacy_provider_secret(provider: str) -> dict[str, str] | None:
    ensure_workspace()
    paths = workspace_paths()
    vault_path = paths.get("llm_settings")
    master_key_path = paths.get("llm_master_key")
    if not vault_path or not master_key_path or not vault_path.exists() or not master_key_path.exists():
        return None
    try:
        payload: dict[str, Any] = json.loads(vault_path.read_text(encoding="utf-8"))
        profile = payload.get("profiles", {}).get(provider)
        if not profile and provider == "kimi":
            profile = payload.get("profiles", {}).get("anthropic")
        encrypted = profile.get("apiKey") if profile else None
        if not encrypted:
            return None
        plaintext = Fernet(master_key_path.read_text(encoding="utf-8").strip().encode("ascii")).decrypt(
            encrypted["ciphertext"].encode("ascii")
        )
    except (OSError, json.JSONDecodeError, InvalidToken, KeyError, AttributeError):
        return None
    return {
        "api_key": plaintext.decode("utf-8"),
        "model": profile.get("model") or "",
        "base_url": profile.get("baseUrl") or "",
    }
