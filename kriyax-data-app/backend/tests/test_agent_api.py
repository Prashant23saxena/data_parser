from fastapi.testclient import TestClient

from app.main import app


def test_agent_api_generate_and_correct_require_real_llm(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))
    client = TestClient(app)

    generate = client.post("/api/agent/generate", json={"prompt": "clean orders"})
    assert generate.status_code == 400
    assert "LLM_KEY_MISSING" in generate.json()["detail"]

    correct = client.post(
        "/api/agent/correct",
        json={"code": "df = load_table('raw.orders')", "traceback": "KeyError: missing", "attempt": 1},
    )
    assert correct.status_code == 400
    assert "LLM_KEY_MISSING" in correct.json()["detail"]


def test_agent_chat_api_uses_real_llm_path(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))

    from app.services import agent

    monkeypatch.setattr(
        agent,
        "complete_text",
        lambda prompt: "Sure.\n```python\nshow(load_table('raw.orders'))\n```",
    )
    monkeypatch.setattr(agent, "runtime_status", lambda: {"provider": "kimi"})

    client = TestClient(app)
    response = client.post(
        "/api/agent/chat",
        json={
            "messages": [{"role": "user", "content": "write code"}],
            "currentCode": "",
            "selectedTable": "raw.orders",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["hasCode"] is True
    assert payload["code"] == "show(load_table('raw.orders'))\n"
