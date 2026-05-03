import duckdb

from kriyax_workbench.agent import generate_code
from kriyax_workbench.audit import read_events
from pathlib import Path

from kriyax_workbench.catalog import describe_table, drop_table, export_table, export_table_html, list_tables, preview_table, rename_table, search_tables, truncate_table
from kriyax_workbench.context_pack import build_context, render_markdown
from kriyax_workbench.db_viewer import connection_info
from kriyax_workbench.execution import script_file
from kriyax_workbench.file_import import commit_import, inspect_file
from kriyax_workbench.pipelines import create_pipeline, list_failures, list_runs, run_pipeline, set_enabled, set_schedule
from kriyax_workbench.workspace import ensure_workspace, workspace_paths


def test_file_import_search_export_and_table_management(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKBENCH_ROOT", str(tmp_path))
    ensure_workspace()
    csv_path = tmp_path / "orders.csv"
    csv_path.write_text("Customer,Amount\nAcme,12.5\nBravo,20\n", encoding="utf-8")

    inspection = inspect_file(csv_path)
    result = commit_import(csv_path, "raw_files", "orders", columns=inspection["columns"])

    assert result["qualifiedName"] == "raw_files.orders"
    assert Path(result["storedFilePath"]).exists()
    catalog_entry = list_tables()[0]
    assert Path(catalog_entry["source"]["filePath"]).exists()
    assert catalog_entry["source"]["originalFilePath"] == str(csv_path.resolve())
    assert describe_table("raw_files.orders")["rowCount"] == 2
    assert preview_table("raw_files.orders", limit=1)["rows"] == [{"customer": "Acme", "amount": 12.5}]
    assert search_tables("amount")[0]["qualifiedName"] == "raw_files.orders"

    export_path = export_table("raw_files.orders")
    assert export_path.endswith("raw_files_orders.csv")
    html_path = export_table_html("raw_files.orders")
    assert html_path.endswith("raw_files_orders.html")
    assert "Acme" in Path(html_path).read_text(encoding="utf-8")

    renamed = rename_table("raw_files.orders", "raw_files.orders_v2")
    assert renamed["qualifiedName"] == "raw_files.orders_v2"
    assert truncate_table("raw_files.orders_v2", confirmation="raw_files.orders_v2")["rowCount"] == 0
    assert drop_table("raw_files.orders_v2", confirmation="raw_files.orders_v2")["dropped"] is True
    assert any(event["eventType"] == "file.import.finished" for event in read_events(limit=20))


def test_pipeline_run_history_and_failure_ack(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKBENCH_ROOT", str(tmp_path))
    ensure_workspace()
    script_file("ok.py").write_text('print("ok")\n', encoding="utf-8")

    pipeline = create_pipeline("OK pipeline", "ok.py")
    set_schedule(pipeline["id"], {"type": "hourly"})
    set_enabled(pipeline["id"], False)
    run = run_pipeline(pipeline["id"])

    assert run["status"] == "success"
    assert list_runs(pipeline["id"])[0]["id"] == run["id"]

    script_file("bad.py").write_text('raise RuntimeError("boom")\n', encoding="utf-8")
    bad = create_pipeline("Bad pipeline", "bad.py")
    failed = run_pipeline(bad["id"])

    assert failed["status"] == "error"
    assert list_failures()[0]["runId"] == failed["id"]


def test_agent_generate_saves_code_and_audits_hashes(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKBENCH_ROOT", str(tmp_path))
    ensure_workspace()
    with duckdb.connect(str(workspace_paths()["database"])) as conn:
        conn.execute("create schema if not exists raw")
        conn.execute("create or replace table raw.orders as select 1 as id")

    from kriyax_workbench import agent as agent_module

    monkeypatch.setattr(agent_module, "complete_text", lambda prompt: 'df = load_table("raw.orders")\nshow(df)\n')
    result = generate_code("show orders", save_as="show_orders.py")

    assert "load_table" in result["code"]
    assert script_file("show_orders.py").exists()
    generated = [event for event in read_events(limit=10) if event["eventType"] == "agent.code.generated"]
    assert generated[0]["promptSha256"]
    assert generated[0]["codeSha256"]


def test_agent_context_pack_summarizes_workspace_without_llm(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKBENCH_ROOT", str(tmp_path))
    ensure_workspace()
    csv_path = tmp_path / "orders.csv"
    csv_path.write_text("Customer,Amount\nAcme,12.5\n", encoding="utf-8")
    inspection = inspect_file(csv_path)
    commit_import(csv_path, "raw_files", "orders", columns=inspection["columns"])
    script_file("check_orders.py").write_text('df = load_table("raw_files.orders")\nshow(df)\n', encoding="utf-8")

    context = build_context(limit=5)
    rendered = render_markdown(context)

    assert context["tables"][0]["qualifiedName"] == "raw_files.orders"
    assert context["scripts"][0]["name"] == "check_orders.py"
    assert "tools/table_view.py raw_files.orders" in rendered
    assert "DB Viewer" in rendered
    assert context["dbViewer"]["driver"] == "DuckDB"
    assert context["dbViewer"]["databasePath"].endswith("kriyax.duckdb")
    assert "Recent Audit" in rendered


def test_db_viewer_info_writes_metadata(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKBENCH_ROOT", str(tmp_path))
    ensure_workspace()
    csv_path = tmp_path / "orders.csv"
    csv_path.write_text("Customer,Amount\nAcme,12.5\n", encoding="utf-8")
    inspection = inspect_file(csv_path)
    commit_import(csv_path, "raw_files", "orders", columns=inspection["columns"])

    info = connection_info()

    assert info["driver"] == "DuckDB"
    assert info["tables"] == ["raw_files.orders"]
    assert info["metadataPath"].endswith("db-viewer.json")
    assert Path(info["metadataPath"]).exists()
