import importlib
import json


def _workspace(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))

    import app.services.workspace as workspace

    importlib.reload(workspace)
    workspace.ensure_workspace()
    return workspace


def test_agent_generate_requires_real_llm(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)
    workspace.workspace_paths()["catalog"].write_text(
        json.dumps(
            [
                {
                    "qualifiedName": "raw.orders",
                    "rowCount": 2,
                    "columns": [{"name": "id", "type": "integer"}, {"name": "amount", "type": "decimal"}],
                }
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    from app.services import agent

    try:
        agent.generate_code("sum amount")
    except ValueError as exc:
        assert "LLM_KEY_MISSING" in str(exc)
    else:
        raise AssertionError("Expected missing LLM key to block agent generation")


def test_agent_correct_limits_attempts(monkeypatch, tmp_path):
    _workspace(monkeypatch, tmp_path)

    from app.services import agent

    try:
        agent.correct_code("df = load_table('raw.orders')", "KeyError: amount", attempt=2)
    except ValueError as exc:
        assert "LLM_KEY_MISSING" in str(exc)
    else:
        raise AssertionError("Expected missing LLM key to block agent correction")

    try:
        agent.correct_code("x", "trace", attempt=4)
    except ValueError as exc:
        assert str(exc) == "Maximum correction attempts reached."
    else:
        raise AssertionError("Expected correction attempt guard")


def test_agent_chat_returns_message_and_code_block(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)
    workspace.workspace_paths()["catalog"].write_text(
        json.dumps(
            [
                {
                    "qualifiedName": "raw.orders",
                    "rowCount": 2,
                    "columns": [{"name": "amount", "type": "decimal"}],
                }
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    from app.services import agent

    monkeypatch.setattr(
        agent,
        "complete_text",
        lambda prompt: "Use this:\n```python\ndf = load_table('raw.orders')\nshow(df)\n```",
    )
    monkeypatch.setattr(agent, "runtime_status", lambda: {"provider": "kimi"})

    response = agent.chat(
        messages=[{"role": "user", "content": "show orders"}],
        current_code="",
        selected_table="raw.orders",
    )

    assert response["status"] == "success"
    assert response["hasCode"] is True
    assert response["code"] == "df = load_table('raw.orders')\nshow(df)\n"
    assert response["schemaContext"]["tables"][0]["qualifiedName"] == "raw.orders"
