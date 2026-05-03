import json


def test_llm_settings_encrypts_and_restores_key(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))

    from app.services.llm_settings import get_runtime_profile, save_profile, settings_summary, validate_profile
    from app.services.workspace import workspace_paths

    profile = save_profile(
        "openai",
        model="gpt-test",
        base_url="https://api.openai.com/v1",
        api_key="sk-local-secret",
    )

    assert profile["hasApiKey"] is True
    assert settings_summary()["activeProvider"] == "openai"
    assert validate_profile("openai")["status"] == "ready"
    assert get_runtime_profile("openai")["apiKey"] == "sk-local-secret"

    vault_text = workspace_paths()["llm_settings"].read_text(encoding="utf-8")
    vault = json.loads(vault_text)
    assert "sk-local-secret" not in vault_text
    assert vault["profiles"]["openai"]["apiKey"]["ciphertext"]


def test_llm_settings_preserves_key_when_profile_is_edited(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))

    from app.services.llm_settings import get_runtime_profile, save_profile

    save_profile("anthropic", model="claude-original", api_key="anthropic-secret")
    updated = save_profile("anthropic", model="claude-updated", api_key=None)

    assert updated["model"] == "claude-updated"
    assert updated["hasApiKey"] is True
    assert get_runtime_profile("anthropic")["apiKey"] == "anthropic-secret"


def test_llm_validate_reports_missing_key(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))

    from app.services.llm_settings import save_profile, validate_profile

    save_profile("openai", model="gpt-test")
    result = validate_profile("openai")

    assert result["status"] == "missing_key"
