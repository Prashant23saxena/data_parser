from __future__ import annotations

import traceback
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

from kriyax_workbench.audit import finish_action, snapshot_script, start_action
from kriyax_workbench.catalog import register_dataframe_table, safe_identifier, split_qualified_name
from kriyax_workbench.workspace import ensure_workspace, workspace_paths


def run_script(script_name: str, code: str | None = None) -> dict[str, Any]:
    ensure_workspace()
    script_path = script_file(script_name)
    if code is not None:
        script_path.write_text(code, encoding="utf-8")
    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")

    code_to_run = script_path.read_text(encoding="utf-8")
    audit_start = start_action(
        "script.run",
        {"scriptName": script_path.name, "scriptPath": str(script_path), "toolName": "tools/script_run.py"},
    )
    script_snapshot = snapshot_script(script_path, audit_start["eventId"])

    saved_tables: list[str] = []
    display_frames: list[dict[str, Any]] = []
    stdout_buffer = StringIO()
    stderr_buffer = StringIO()
    return_code = 0

    def load_table(name: str, columns: list[str] | None = None) -> pd.DataFrame:
        schema, table = split_qualified_name(name)
        selected = "*"
        if columns:
            selected = ", ".join([f'"{column}"' for column in columns])
        with duckdb.connect(str(workspace_paths()["database"])) as conn:
            return conn.execute(f'select {selected} from "{schema}"."{table}"').fetchdf()

    def save_table(df: pd.DataFrame, name: str, schema: str = "curated") -> str:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("save_table expects a pandas DataFrame")
        safe_schema = safe_identifier(schema)
        safe_table = safe_identifier(name)
        with duckdb.connect(str(workspace_paths()["database"])) as conn:
            conn.execute(f'create schema if not exists "{safe_schema}"')
            conn.register("save_frame", df)
            conn.execute(f'create or replace table "{safe_schema}"."{safe_table}" as select * from save_frame')
            conn.unregister("save_frame")
        qualified_name = register_dataframe_table(
            safe_schema,
            safe_table,
            df,
            {"kind": "python", "scriptName": script_path.name, "scriptPath": str(script_path)},
        )
        if qualified_name not in saved_tables:
            saved_tables.append(qualified_name)
        return qualified_name

    def show(df: pd.DataFrame, name: str = "result") -> pd.DataFrame:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("show expects a pandas DataFrame")
        display_frames.append({"name": name, "rowCount": int(len(df)), "columns": list(df.columns), "rows": df.head(50).to_dict("records")})
        return df

    namespace = {"__name__": "__main__", "load_table": load_table, "save_table": save_table, "show": show}
    with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
        try:
            exec(compile(code_to_run, str(script_path), "exec"), namespace)
        except Exception:
            return_code = 1
            traceback.print_exc()

    status = "success" if return_code == 0 else "error"
    run_id = f"{script_path.stem}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
    stdout_path = workspace_paths()["runs"] / f"{run_id}.stdout.txt"
    stderr_path = workspace_paths()["runs"] / f"{run_id}.stderr.txt"
    stdout_path.write_text(stdout_buffer.getvalue(), encoding="utf-8")
    stderr_path.write_text(stderr_buffer.getvalue(), encoding="utf-8")
    result = {
        "status": status,
        "runId": run_id,
        "scriptName": script_path.name,
        "scriptPath": str(script_path),
        "returnCode": return_code,
        "stdout": stdout_buffer.getvalue(),
        "stderr": stderr_buffer.getvalue(),
        "savedTables": saved_tables,
        "displayFrames": display_frames,
        "stdoutPath": str(stdout_path),
        "stderrPath": str(stderr_path),
    }
    finish_action(
        audit_start,
        status,
        {
            **script_snapshot,
            "runId": run_id,
            "scriptName": script_path.name,
            "scriptPath": str(script_path),
            "returnCode": return_code,
            "savedTables": saved_tables,
            "displayFrames": [frame["name"] for frame in display_frames],
            "stdoutPath": str(stdout_path),
            "stderrPath": str(stderr_path),
        },
    )
    return result


def script_file(script_name: str) -> Path:
    safe_name = script_name.strip()
    if not safe_name.endswith(".py"):
        safe_name = f"{safe_name}.py"
    return workspace_paths()["scripts"] / Path(safe_name).name


def list_scripts() -> list[dict[str, Any]]:
    ensure_workspace()
    scripts = []
    for path in sorted(workspace_paths()["scripts"].glob("*.py")):
        stat = path.stat()
        scripts.append(
            {
                "name": path.name,
                "path": str(path),
                "size": stat.st_size,
                "updatedAt": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
            }
        )
    return scripts


def read_script(script_name: str) -> dict[str, Any]:
    path = script_file(script_name)
    if not path.exists():
        raise FileNotFoundError(f"Script not found: {path.name}")
    return {"name": path.name, "path": str(path), "code": path.read_text(encoding="utf-8")}


def create_script(script_name: str, template: str = "blank") -> dict[str, Any]:
    path = script_file(script_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(script_template(template), encoding="utf-8")
    return read_script(path.name)


def script_template(template: str) -> str:
    if template == "join":
        return (
            'orders = load_table("raw_files.orders")\n'
            'customers = load_table("raw_files.customers")\n\n'
            'joined = orders.merge(customers, on="customer_id", how="left")\n'
            'result = joined.groupby("region", as_index=False)["amount"].sum()\n\n'
            'show(result, name="region_revenue_preview")\n'
            'save_table(result, "region_revenue", schema="curated")\n'
        )
    if template == "load-save":
        return (
            'df = load_table("raw_files.source_table")\n'
            'show(df.head(20), name="preview")\n'
            'save_table(df, "derived_table", schema="curated")\n'
        )
    return "# Write pandas transformations with load_table(), show(), and save_table().\n"
