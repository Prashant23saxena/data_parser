from fastapi.testclient import TestClient

from app.main import app


def test_developer_llm_config_lists_real_providers_and_missing_key(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("KIMI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_API_KEY", raising=False)
    client = TestClient(app)

    response = client.get("/api/v1/developer/llm/config?provider=kimi")

    assert response.status_code == 200
    payload = response.json()
    assert payload["provider"] == "kimi"
    assert payload["model"] == "kimi-for-coding"
    assert payload["base_url"] == "https://api.kimi.com/coding/v1/chat/completions"
    assert payload["masked_key_status"] == "missing"
    assert payload["source"] == "missing"


def test_developer_llm_test_blocks_missing_key(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    monkeypatch.delenv("KIMI_API_KEY", raising=False)
    client = TestClient(app)

    response = client.post(
        "/api/v1/developer/llm/test",
        json={"provider": "kimi", "message": "Say OK for the LLM test runner."},
    )

    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "LLM_KEY_MISSING"


def test_developer_llm_vault_profile_and_audit_flow(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    monkeypatch.delenv("KIMI_API_KEY", raising=False)
    client = TestClient(app)

    save = client.post(
        "/api/v1/developer/llm/vault-key",
        json={
            "provider": "kimi",
            "api_key": "sk-test-secret",
            "model": "kimi-for-coding",
            "base_url": "https://api.kimi.com/coding/v1/chat/completions",
        },
    )
    assert save.status_code == 200
    assert "sk-test-secret" not in save.text
    assert save.json()["masked_key_status"].startswith("sk-")

    created = client.post(
        "/api/v1/developer/llm/profiles",
        json={
            "label": "Kimi Coding",
            "provider": "kimi",
            "model": "kimi-for-coding",
            "base_url": "https://api.kimi.com/coding/v1/chat/completions",
        },
    )
    assert created.status_code == 200
    profile = created.json()
    assert "api_key" not in profile

    defaulted = client.post(f"/api/v1/developer/llm/profiles/{profile['id']}/default")
    assert defaulted.status_code == 200

    def fake_complete(request):
        assert request.provider == "kimi"
        assert request.messages[-1].content == "Say OK for the LLM test runner."
        return "OK"

    monkeypatch.setattr("app.services.developer_llm.complete_chat", fake_complete)
    result = client.post(
        "/api/v1/developer/llm/test",
        json={"provider": "kimi", "message": "Say OK for the LLM test runner."},
    )
    assert result.status_code == 200
    assert result.json()["response"] == "OK"
    assert result.json()["success"] is True

    audit = client.get("/api/v1/developer/llm/audit")
    assert audit.status_code == 200
    assert audit.json()["items"][0]["provider"] == "kimi"
    assert "sk-test-secret" not in audit.text


def test_developer_llm_playground_reuses_test_execution(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    client = TestClient(app)
    client.post("/api/v1/developer/llm/vault-key", json={"provider": "anthropic", "api_key": "anthropic-key"})

    calls = []

    def fake_complete(request):
        calls.append([message.content for message in request.messages])
        return "chat response"

    monkeypatch.setattr("app.services.developer_llm.complete_chat", fake_complete)
    response = client.post(
        "/api/v1/developer/llm/playground",
        json={"provider": "anthropic", "message": "Use the same path."},
    )

    assert response.status_code == 200
    assert response.json()["response"] == "chat response"
    assert calls == [["Use the same path."]]
