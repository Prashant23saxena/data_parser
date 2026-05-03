import os
from dataclasses import dataclass
from pathlib import Path


Provider = str

BACKEND_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class ProviderDefaults:
    label: str
    model: str
    base_url: str
    api_key_env: str
    model_env: str
    base_url_env: str


SUPPORTED_LLM_PROVIDERS: dict[Provider, ProviderDefaults] = {
    "openai": ProviderDefaults(
        label="OpenAI",
        model="gpt-4o-mini",
        base_url="https://api.openai.com/v1",
        api_key_env="OPENAI_API_KEY",
        model_env="OPENAI_MODEL",
        base_url_env="OPENAI_BASE_URL",
    ),
    "kimi": ProviderDefaults(
        label="Kimi",
        model="kimi-for-coding",
        base_url="https://api.kimi.com/coding/v1/chat/completions",
        api_key_env="KIMI_API_KEY",
        model_env="KIMI_MODEL",
        base_url_env="KIMI_BASE_URL",
    ),
    "anthropic": ProviderDefaults(
        label="Anthropic",
        model="claude-3-5-sonnet-20241022",
        base_url="https://api.anthropic.com",
        api_key_env="ANTHROPIC_API_KEY",
        model_env="ANTHROPIC_MODEL",
        base_url_env="ANTHROPIC_BASE_URL",
    ),
    "azure-openai": ProviderDefaults(
        label="Azure OpenAI",
        model="",
        base_url="",
        api_key_env="AZURE_OPENAI_API_KEY",
        model_env="AZURE_OPENAI_MODEL",
        base_url_env="AZURE_OPENAI_BASE_URL",
    ),
}


def developer_mode_enabled() -> bool:
    return os.environ.get("KRIYA_DEVELOPER_MODE", "1") == "1"


def default_llm_provider() -> Provider:
    provider = os.environ.get("KRIYA_LLM_PROVIDER", "kimi")
    return provider if provider in SUPPORTED_LLM_PROVIDERS else "kimi"


def provider_default(provider: Provider) -> ProviderDefaults:
    try:
        return SUPPORTED_LLM_PROVIDERS[provider]
    except KeyError as exc:
        raise ValueError("Unsupported LLM provider.") from exc


def env_value(name: str) -> str | None:
    value = os.environ.get(name)
    return value.strip() if value and value.strip() else None


def local_secret_vault_path() -> Path:
    configured = os.environ.get("KRIYA_LOCAL_SECRET_VAULT_PATH")
    if configured:
        return Path(configured).expanduser().resolve()
    from app.services.workspace import workspace_paths

    return workspace_paths()["metadata"] / "secrets.json.enc"


def local_secret_master_key_path() -> Path:
    configured = os.environ.get("KRIYA_LOCAL_SECRET_MASTER_KEY_PATH")
    if configured:
        return Path(configured).expanduser().resolve()
    from app.services.workspace import workspace_paths

    return workspace_paths()["metadata"] / "master.key"
