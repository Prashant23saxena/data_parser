from fastapi.testclient import TestClient

from app.main import app


def test_llm_settings_api_saves_sanitized_profile(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    client = TestClient(app)

    response = client.post(
        "/api/llm/settings",
        json={
            "provider": "openai",
            "model": "gpt-test",
            "baseUrl": "https://api.openai.com/v1",
            "apiKey": "sk-secret",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["profile"]["hasApiKey"] is True
    assert "apiKey" not in payload["profile"]
    assert payload["settings"]["activeProvider"] == "openai"

    test = client.post("/api/llm/test", json={"provider": "openai"})
    assert test.status_code == 200
    assert test.json()["status"] == "ready"


def test_llm_settings_api_lists_supported_providers(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    client = TestClient(app)

    response = client.get("/api/llm/settings")

    assert response.status_code == 200
    providers = {item["provider"] for item in response.json()["supportedProviders"]}
    assert providers == {"openai", "kimi", "anthropic", "azure-openai"}


def test_llm_status_never_returns_api_key(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    client = TestClient(app)

    client.post(
        "/api/llm/settings",
        json={
            "provider": "openai",
            "model": "gpt-test",
            "baseUrl": "https://api.openai.com/v1",
            "apiKey": "sk-secret",
        },
    )

    response = client.get("/api/llm/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ready"
    assert payload["hasApiKey"] is True
    assert "sk-secret" not in response.text


def test_llm_playground_blocks_without_key(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    client = TestClient(app)

    response = client.post("/api/llm/playground", json={"provider": "openai", "prompt": "hello"})

    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "LLM_KEY_MISSING"
