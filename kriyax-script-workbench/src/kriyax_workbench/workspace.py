from __future__ import annotations

import os
from pathlib import Path


DEFAULT_WORKSPACE_ROOT = Path(__file__).resolve().parents[2] / "workspace"


def workspace_root() -> Path:
    configured = os.environ.get("KRIYAX_WORKBENCH_ROOT")
    return Path(configured).expanduser().resolve() if configured else DEFAULT_WORKSPACE_ROOT


def workspace_paths() -> dict[str, Path]:
    root = workspace_root()
    return {
        "root": root,
        "warehouse": root / "warehouse",
        "database": root / "warehouse" / "kriyax.duckdb",
        "metadata": root / "metadata",
        "catalog": root / "metadata" / "catalog.json",
        "connections": root / "metadata" / "connections.json",
        "odoo_cursors": root / "metadata" / "odoo-cursors.json",
        "pipelines": root / "metadata" / "pipelines.json",
        "pipeline_failures": root / "metadata" / "pipeline-failures.json",
        "scripts": root / "scripts",
        "runs": root / "runs",
        "audit": root / "audit",
        "audit_log": root / "audit" / "audit.jsonl",
        "audit_snapshots": root / "audit" / "snapshots",
        "exports": root / "data" / "exports",
        "uploads": root / "data" / "uploads",
    }


def ensure_workspace() -> dict[str, str]:
    paths = workspace_paths()
    for key in ["warehouse", "metadata", "scripts", "runs", "audit", "audit_snapshots", "exports", "uploads"]:
        paths[key].mkdir(parents=True, exist_ok=True)
    if not paths["catalog"].exists():
        paths["catalog"].write_text("[]\n", encoding="utf-8")
    if not paths["connections"].exists():
        paths["connections"].write_text("[]\n", encoding="utf-8")
    if not paths["odoo_cursors"].exists():
        paths["odoo_cursors"].write_text("[]\n", encoding="utf-8")
    if not paths["pipelines"].exists():
        paths["pipelines"].write_text("[]\n", encoding="utf-8")
    if not paths["pipeline_failures"].exists():
        paths["pipeline_failures"].write_text("{}\n", encoding="utf-8")
    if not paths["audit_log"].exists():
        paths["audit_log"].write_text("", encoding="utf-8")
    return {key: str(value) for key, value in paths.items()}
