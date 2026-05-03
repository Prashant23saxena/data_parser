import json
import os
import re
import traceback
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

from app.services.file_import import list_catalog_tables
from app.services.workspace import ensure_workspace, workspace_paths


def run_script(*, script_name: str, code: str, persist_script: bool = False) -> dict[str, Any]:
    ensure_workspace()
    paths = workspace_paths()
    script_path = _script_path(script_name)
    result_path = paths["runs"] / f"{script_path.stem}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}.json"

    helper_path = paths["scripts"] / "_kriyax_runtime.py"
    helper_path.write_text(_runtime_helper_source(result_path), encoding="utf-8")
    compile_path = script_path if persist_script else paths["runs"] / f"{script_path.stem}-transient.py"
    if persist_script:
        script_path.write_text(code, encoding="utf-8")

    saved_tables: list[str] = []
    result_tables: list[dict[str, Any]] = []
    display_frames: list[dict[str, Any]] = []
    stdout_buffer = StringIO()
    stderr_buffer = StringIO()

    def load_table(name: str, columns: list[str] | None = None):
        return _load_table(name, columns)

    def save_table(df, name: str, schema: str = "curated"):
        qualified_name = _save_table(df, name, schema)
        if qualified_name not in saved_tables:
            saved_tables.append(qualified_name)
        preview = _preview_dataframe(df, name=qualified_name)
        result_tables[:] = [item for item in result_tables if item["qualifiedName"] != qualified_name]
        result_tables.append(
            {
                "name": qualified_name,
                "qualifiedName": qualified_name,
                "rowCount": preview["rowCount"],
                "columnCount": preview["columnCount"],
                "columns": preview["columns"],
                "rows": preview["rows"],
            }
        )
        result_path.write_text(json.dumps({"savedTables": saved_tables}), encoding="utf-8")
        return qualified_name

    def show(df, name: str = "result"):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("show expects a pandas DataFrame")
        display_frames.append(_preview_dataframe(df, name=name))
        return df

    namespace = {
        "__name__": "__main__",
        "load_table": load_table,
        "save_table": save_table,
        "show": show,
    }
    return_code = 0
    with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
        try:
            exec(compile(code, str(compile_path), "exec"), namespace)
        except Exception:
            return_code = 1
            traceback.print_exc()

    for qualified_name in saved_tables:
        schema, table = qualified_name.split(".", 1)
        _register_python_table(schema=schema, table=table, script_path=script_path, persisted=persist_script)

    status = "success" if return_code == 0 else "error"
    stderr = stderr_buffer.getvalue()
    if status == "error" and "Catalog Error" in stderr:
        stderr = f"{stderr}\nAvailable tables: {_available_table_names()}"

    preview = display_frames[0] if display_frames else result_tables[0] if result_tables else None

    return {
        "status": status,
        "scriptName": script_path.name,
        "scriptPath": str(script_path) if persist_script else None,
        "persistedScript": persist_script,
        "stdout": stdout_buffer.getvalue(),
        "stderr": stderr,
        "returnCode": return_code,
        "savedTables": saved_tables,
        "resultTables": result_tables,
        "displayFrames": display_frames,
        "preview": preview,
    }


def save_script(script_name: str, code: str) -> dict[str, Any]:
    ensure_workspace()
    path = _script_path(script_name)
    path.write_text(code, encoding="utf-8")
    stat = path.stat()
    return {
        "name": path.name,
        "path": str(path),
        "size": stat.st_size,
        "updatedAt": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
        "code": code,
    }


def list_scripts() -> list[dict[str, Any]]:
    ensure_workspace()
    scripts = []
    for path in sorted(workspace_paths()["scripts"].glob("*.py")):
        if path.name.startswith("_"):
            continue
        stat = path.stat()
        scripts.append(
            {
                "name": path.name,
                "path": str(path),
                "size": stat.st_size,
                "updatedAt": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
            }
        )
    return sorted(scripts, key=lambda script: script["updatedAt"], reverse=True)


def get_script(script_name: str) -> dict[str, Any]:
    path = _script_path(script_name)
    if not path.exists():
        raise FileNotFoundError(f"Saved script not found: {path.name}")
    return {
        "name": path.name,
        "path": str(path),
        "code": path.read_text(encoding="utf-8"),
        "updatedAt": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat(),
    }


def _script_path(script_name: str) -> Path:
    safe_name = re.sub(r"[^0-9a-zA-Z_.-]+", "_", script_name.strip()) or "script.py"
    if not safe_name.endswith(".py"):
        safe_name = f"{safe_name}.py"
    return workspace_paths()["scripts"] / safe_name


def _saved_tables(result_path: Path) -> list[str]:
    if not result_path.exists():
        return []
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    return payload.get("savedTables", [])


def _load_table(name: str, columns: list[str] | None = None):
    if "." in name:
        schema, table = name.split(".", 1)
    else:
        schema, table = "main", name
    selected = "*"
    if columns:
        selected = ", ".join([f'"{column}"' for column in columns])
    try:
        with duckdb.connect(str(workspace_paths()["database"])) as conn:
            return conn.execute(f'select {selected} from "{schema}"."{table}"').fetchdf()
    except Exception as exc:
        raise RuntimeError(f"Could not load table {schema}.{table}: {exc}") from exc


def _save_table(df, name: str, schema: str = "curated") -> str:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("save_table expects a pandas DataFrame")
    safe_schema = _safe_identifier(schema)
    safe_table = _safe_identifier(name)
    with duckdb.connect(str(workspace_paths()["database"])) as conn:
        conn.execute(f'create schema if not exists "{safe_schema}"')
        conn.register("save_frame", df)
        conn.execute(f'create or replace table "{safe_schema}"."{safe_table}" as select * from save_frame')
        conn.unregister("save_frame")
    return f"{safe_schema}.{safe_table}"


def _preview_dataframe(df: pd.DataFrame, *, name: str, row_limit: int = 100, column_limit: int = 40) -> dict[str, Any]:
    limited = df.iloc[:row_limit, :column_limit]
    return {
        "name": name,
        "rowCount": int(len(df)),
        "columnCount": int(len(df.columns)),
        "columns": [str(column) for column in limited.columns],
        "rows": _records(limited),
    }


def _records(df: pd.DataFrame) -> list[dict[str, Any]]:
    return json.loads(df.where(pd.notnull(df), None).to_json(orient="records", date_format="iso"))


def _register_python_table(*, schema: str, table: str, script_path: Path, persisted: bool) -> None:
    paths = workspace_paths()
    with duckdb.connect(str(paths["database"])) as conn:
        row_count = conn.execute(f'select count(*) from "{schema}"."{table}"').fetchone()[0]
        columns = conn.execute(f'describe "{schema}"."{table}"').fetchall()

    entry = {
        "qualifiedName": f"{schema}.{table}",
        "schema": schema,
        "tableName": table,
        "source": {
            "kind": "python",
            "scriptName": script_path.name,
            "scriptPath": str(script_path) if persisted else None,
            "persistedScript": persisted,
        },
        "rowCount": int(row_count),
        "columnCount": len(columns),
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "columns": [
            {"name": column[0], "sourceName": column[0], "type": _duckdb_type_to_app_type(str(column[1]))}
            for column in columns
        ],
    }
    _upsert_catalog(entry)


def _upsert_catalog(entry: dict[str, Any]) -> None:
    path = workspace_paths()["catalog"]
    catalog = json.loads(path.read_text(encoding="utf-8"))
    remaining = [item for item in catalog if item.get("qualifiedName") != entry["qualifiedName"]]
    remaining.append(entry)
    path.write_text(json.dumps(remaining, indent=2) + "\n", encoding="utf-8")


def _available_table_names() -> str:
    names = [table["qualifiedName"] for table in list_catalog_tables()]
    return ", ".join(names) if names else "none"


def _duckdb_type_to_app_type(duckdb_type: str) -> str:
    normalized = duckdb_type.upper()
    if "INT" in normalized:
        return "integer"
    if any(token in normalized for token in ["DOUBLE", "DECIMAL", "FLOAT", "REAL"]):
        return "decimal"
    if "DATE" == normalized:
        return "date"
    if "TIMESTAMP" in normalized:
        return "datetime"
    if "BOOL" in normalized:
        return "boolean"
    return "text"


def _safe_identifier(value: str) -> str:
    cleaned = re.sub(r"[^0-9a-zA-Z_]+", "_", value.strip().lower()).strip("_")
    cleaned = re.sub(r"_+", "_", cleaned)
    if cleaned and cleaned[0].isdigit():
        cleaned = f"_{cleaned}"
    return cleaned


def _runtime_helper_source(result_path: Path) -> str:
    return f'''import json
import os

import duckdb
import pandas as pd

_SAVED_TABLES = []
_DATABASE_PATH = os.environ["KRIYAX_DATABASE_PATH"]
_RESULT_PATH = {str(result_path)!r}


def load_table(name, columns=None):
    if "." in name:
        schema, table = name.split(".", 1)
    else:
        schema, table = "main", name
    selected = "*"
    if columns:
        selected = ", ".join([f'"{{column}}"' for column in columns])
    with duckdb.connect(_DATABASE_PATH) as conn:
        return conn.execute(f'select {{selected}} from "{{schema}}"."{{table}}"').fetchdf()


def save_table(df, name, schema="curated"):
    if not isinstance(df, pd.DataFrame):
        raise TypeError("save_table expects a pandas DataFrame")
    with duckdb.connect(_DATABASE_PATH) as conn:
        conn.execute(f'create schema if not exists "{{schema}}"')
        conn.register("save_frame", df)
        conn.execute(f'create or replace table "{{schema}}"."{{name}}" as select * from save_frame')
        conn.unregister("save_frame")
    qualified = f"{{schema}}.{{name}}"
    if qualified not in _SAVED_TABLES:
        _SAVED_TABLES.append(qualified)
    with open(_RESULT_PATH, "w", encoding="utf-8") as handle:
        json.dump({{"savedTables": _SAVED_TABLES}}, handle)
    return qualified
'''
