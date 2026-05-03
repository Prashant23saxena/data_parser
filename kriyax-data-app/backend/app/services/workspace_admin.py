import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb

from app.services.workspace import ensure_workspace, workspace_paths, workspace_root


TUTORIAL_SCRIPT = """df = load_table("raw_files.tutorial_orders")
print(f"loaded {len(df)} tutorial rows")
clean = df[df["amount"] >= 100].copy()
save_table(clean, "tutorial_orders_curated", schema="curated")
show(clean, name="tutorial_orders_curated")
"""


def archive_workspace(*, archive_base: Path | None = None, timestamp: str | None = None) -> dict[str, Any]:
    ensure_workspace()
    stamp = timestamp or datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    target = (archive_base or _default_archive_base()) / stamp
    target.mkdir(parents=True, exist_ok=False)

    paths = workspace_paths()
    copied: list[str] = []
    for key in ["uploads", "exports", "scripts", "runs", "warehouse", "metadata"]:
        source = paths[key]
        if not source.exists():
            continue
        destination = target / source.relative_to(paths["root"])
        if source.is_dir():
            shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        copied.append(str(destination))

    manifest = {
        "archivedAt": datetime.now(timezone.utc).isoformat(),
        "workspaceRoot": str(paths["root"]),
        "archivePath": str(target),
        "copied": copied,
    }
    (target / "archive-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def reset_to_tutorial_sample(*, archive: bool = True, archive_base: Path | None = None) -> dict[str, Any]:
    archive_manifest = archive_workspace(archive_base=archive_base) if archive else None
    paths = workspace_paths()
    ensure_workspace()

    for key in ["uploads", "exports", "scripts", "runs"]:
        shutil.rmtree(paths[key], ignore_errors=True)
        paths[key].mkdir(parents=True, exist_ok=True)

    for database_path in [paths["database"], paths["database"].with_suffix(paths["database"].suffix + ".wal")]:
        if database_path.exists():
            database_path.unlink()

    _write_json(paths["catalog"], [_tutorial_catalog_entry(paths)])
    _write_json(paths["pipelines"], [_tutorial_pipeline()])
    _write_json(paths["import_drafts"], [])
    _write_json(paths["odoo_sync_cursors"], [])
    paths["pipeline_failures"].write_text("{}\n", encoding="utf-8")

    tutorial_csv = paths["uploads"] / "tutorial_orders.csv"
    tutorial_csv.write_text(
        "order_id,customer,order_date,amount,status\n"
        "1001,Acme Manufacturing,2026-04-01,1250.50,shipped\n"
        "1002,Northstar Retail,2026-04-03,88.75,pending\n"
        "1003,Acme Manufacturing,2026-04-08,420.00,shipped\n",
        encoding="utf-8",
    )
    (paths["scripts"] / "tutorial_clean_orders.py").write_text(TUTORIAL_SCRIPT, encoding="utf-8")

    with duckdb.connect(str(paths["database"])) as conn:
        conn.execute("create schema if not exists raw_files")
        conn.execute(
            """
            create or replace table raw_files.tutorial_orders as
            select
              order_id::BIGINT as order_id,
              customer::VARCHAR as customer,
              order_date::DATE as order_date,
              amount::DOUBLE as amount,
              status::VARCHAR as status
            from read_csv_auto(?)
            """,
            [str(tutorial_csv)],
        )

    return {
        "status": "seeded",
        "archive": archive_manifest,
        "tables": ["raw_files.tutorial_orders"],
        "scripts": ["tutorial_clean_orders.py"],
        "pipelines": ["Tutorial Orders Refresh"],
    }


def _tutorial_catalog_entry(paths: dict[str, Path]) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    csv_path = paths["uploads"] / "tutorial_orders.csv"
    return {
        "qualifiedName": "raw_files.tutorial_orders",
        "schema": "raw_files",
        "tableName": "tutorial_orders",
        "source": {"kind": "file", "fileName": "tutorial_orders.csv", "filePath": str(csv_path)},
        "rowCount": 3,
        "columnCount": 5,
        "createdAt": now,
        "columns": [
            {"name": "order_id", "sourceName": "order_id", "type": "integer"},
            {"name": "customer", "sourceName": "customer", "type": "text"},
            {"name": "order_date", "sourceName": "order_date", "type": "date"},
            {"name": "amount", "sourceName": "amount", "type": "decimal"},
            {"name": "status", "sourceName": "status", "type": "text"},
        ],
    }


def _tutorial_pipeline() -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    return {
        "id": "tutorial-orders-refresh",
        "name": "Tutorial Orders Refresh",
        "scriptId": "tutorial_clean_orders.py",
        "connectorSyncId": None,
        "enabled": False,
        "schedule": None,
        "createdAt": now,
        "updatedAt": now,
    }


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _default_archive_base() -> Path:
    default_root = Path(__file__).resolve().parents[4] / "workspace_archives"
    configured_root = workspace_root()
    if configured_root == workspace_paths()["root"]:
        return default_root
    return configured_root.parent / "workspace_archives"
