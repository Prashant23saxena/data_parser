import importlib
import json

import duckdb


def _workspace(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path))

    import app.services.workspace as workspace

    importlib.reload(workspace)
    workspace.ensure_workspace()
    return workspace


def _seed_table(workspace):
    with duckdb.connect(str(workspace.workspace_paths()["database"])) as conn:
        conn.execute("create schema if not exists raw_files")
        conn.execute(
            "create or replace table raw_files.orders as "
            "select * from (values ('Acme', 12.50), ('Bravo', 20.00)) as t(customer, amount)"
        )


def test_run_script_loads_table_saves_derived_table_and_updates_catalog(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)
    _seed_table(workspace)

    from app.services.execution import run_script

    result = run_script(
        script_name="make_big_orders.py",
        code=(
            'df = load_table("raw_files.orders")\n'
            'print(f"loaded {len(df)} rows")\n'
            'big = df[df["amount"] > 15]\n'
            'save_table(big, "big_orders", schema="curated")\n'
        ),
    )

    assert result["status"] == "success"
    assert "loaded 2 rows" in result["stdout"]
    assert result["scriptPath"] is None
    assert result["persistedScript"] is False
    assert result["savedTables"] == ["curated.big_orders"]
    assert result["preview"]["name"] == "curated.big_orders"
    assert result["preview"]["rows"] == [{"customer": "Bravo", "amount": 20.0}]
    assert result["resultTables"][0]["qualifiedName"] == "curated.big_orders"
    assert not (workspace.workspace_paths()["scripts"] / "make_big_orders.py").exists()

    with duckdb.connect(str(workspace.workspace_paths()["database"])) as conn:
        rows = conn.execute("select customer, amount from curated.big_orders").fetchall()

    assert rows == [("Bravo", 20.0)]

    catalog = json.loads(workspace.workspace_paths()["catalog"].read_text(encoding="utf-8"))
    assert catalog[0]["qualifiedName"] == "curated.big_orders"
    assert catalog[0]["source"]["kind"] == "python"
    assert catalog[0]["source"]["persistedScript"] is False


def test_run_script_returns_clear_missing_table_error(monkeypatch, tmp_path):
    _workspace(monkeypatch, tmp_path)

    from app.services.execution import run_script

    result = run_script(
        script_name="missing_table.py",
        code='df = load_table("raw_files.missing_orders")\n',
    )

    assert result["status"] == "error"
    assert "raw_files.missing_orders" in result["stderr"]
    assert "Available tables" in result["stderr"]


def test_run_script_show_captures_unsaved_dataframe_preview(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)
    _seed_table(workspace)

    from app.services.execution import run_script

    result = run_script(
        script_name="show_orders.py",
        code='df = load_table("raw_files.orders")\nshow(df[df["amount"] > 15], name="large_orders")\n',
    )

    assert result["status"] == "success"
    assert result["savedTables"] == []
    assert result["displayFrames"][0]["name"] == "large_orders"
    assert result["displayFrames"][0]["rows"] == [{"customer": "Bravo", "amount": 20.0}]
    assert result["preview"]["name"] == "large_orders"


def test_saved_scripts_can_be_listed_and_loaded(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)
    _seed_table(workspace)

    from app.services.execution import get_script, list_scripts, run_script, save_script

    run_script(
        script_name="make_big_orders.py",
        code='df = load_table("raw_files.orders")\nprint(len(df))\n',
    )
    assert list_scripts() == []

    save_script(
        script_name="make_big_orders.py",
        code='df = load_table("raw_files.orders")\nprint(len(df))\n',
    )

    scripts = list_scripts()

    assert scripts[0]["name"] == "make_big_orders.py"
    assert scripts[0]["path"].endswith("make_big_orders.py")
    assert scripts[0]["size"] > 0
    assert "updatedAt" in scripts[0]
    assert get_script("make_big_orders.py")["code"] == 'df = load_table("raw_files.orders")\nprint(len(df))\n'
