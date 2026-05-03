import importlib
import json

import duckdb


def _workspace(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKSPACE_ROOT", str(tmp_path / "workspace"))

    import app.services.workspace as workspace

    importlib.reload(workspace)
    workspace.ensure_workspace()
    return workspace


def test_archive_and_reset_to_one_tutorial_sample(monkeypatch, tmp_path):
    workspace = _workspace(monkeypatch, tmp_path)
    paths = workspace.workspace_paths()
    (paths["uploads"] / "old.csv").write_text("id\n1\n", encoding="utf-8")
    (paths["scripts"] / "old.py").write_text("print('old')\n", encoding="utf-8")
    (paths["runs"] / "old.json").write_text("{}\n", encoding="utf-8")
    paths["catalog"].write_text(json.dumps([{"qualifiedName": "old.table"}]) + "\n", encoding="utf-8")
    paths["pipelines"].write_text(json.dumps([{"name": "Old"}]) + "\n", encoding="utf-8")
    with duckdb.connect(str(paths["database"])) as conn:
        conn.execute("create schema if not exists old")
        conn.execute("create or replace table old.table as select 1 as id")

    from app.services.workspace_admin import reset_to_tutorial_sample

    result = reset_to_tutorial_sample(archive=True, archive_base=tmp_path / "archives")

    assert result["status"] == "seeded"
    archive_path = tmp_path / "archives"
    assert list(archive_path.glob("*/data/uploads/old.csv"))
    assert list(archive_path.glob("*/scripts/old.py"))
    assert list(archive_path.glob("*/warehouse/kriyax.duckdb"))

    catalog = json.loads(paths["catalog"].read_text(encoding="utf-8"))
    pipelines = json.loads(paths["pipelines"].read_text(encoding="utf-8"))

    assert [item["qualifiedName"] for item in catalog] == ["raw_files.tutorial_orders"]
    assert [path.name for path in paths["scripts"].glob("*.py")] == ["tutorial_clean_orders.py"]
    assert [path.name for path in paths["uploads"].glob("*.csv")] == ["tutorial_orders.csv"]
    assert pipelines[0]["name"] == "Tutorial Orders Refresh"
    assert pipelines[0]["enabled"] is False
    assert json.loads(paths["import_drafts"].read_text(encoding="utf-8")) == []

    with duckdb.connect(str(paths["database"])) as conn:
        rows = conn.execute("select count(*) from raw_files.tutorial_orders").fetchone()[0]

    assert rows == 3
