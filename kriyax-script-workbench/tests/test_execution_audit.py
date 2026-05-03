import duckdb

from kriyax_workbench.audit import read_events
from kriyax_workbench.catalog import preview_table
from kriyax_workbench.execution import run_script, script_file
from kriyax_workbench.workspace import ensure_workspace, workspace_paths


def test_script_run_saves_joined_table_and_writes_audit(monkeypatch, tmp_path):
    monkeypatch.setenv("KRIYAX_WORKBENCH_ROOT", str(tmp_path))
    ensure_workspace()
    with duckdb.connect(str(workspace_paths()["database"])) as conn:
        conn.execute("create schema if not exists raw_files")
        conn.execute("create or replace table raw_files.orders as select 1 as customer_id, 10.0 as amount")
        conn.execute("create or replace table raw_files.customers as select 1 as customer_id, 'West' as region")

    script_file("join_orders.py").write_text(
        'orders = load_table("raw_files.orders")\n'
        'customers = load_table("raw_files.customers")\n'
        'joined = orders.merge(customers, on="customer_id", how="left")\n'
        'result = joined.groupby("region", as_index=False)["amount"].sum()\n'
        'show(result, name="preview")\n'
        'save_table(result, "region_revenue", schema="curated")\n',
        encoding="utf-8",
    )

    result = run_script("join_orders.py")

    assert result["status"] == "success"
    assert result["savedTables"] == ["curated.region_revenue"]
    assert preview_table("curated.region_revenue")["rows"] == [{"region": "West", "amount": 10.0}]
    finished = [event for event in read_events() if event["eventType"] == "script.run.finished"]
    assert finished[0]["scriptName"] == "join_orders.py"
    assert finished[0]["scriptSha256"]
    assert finished[0]["snapshotPath"].endswith("join_orders.py")
