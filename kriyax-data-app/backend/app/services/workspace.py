import os
from pathlib import Path


DEFAULT_WORKSPACE_ROOT = Path(__file__).resolve().parents[3] / "workspace"


def workspace_root() -> Path:
    configured = os.environ.get("KRIYAX_WORKSPACE_ROOT")
    return Path(configured).expanduser().resolve() if configured else DEFAULT_WORKSPACE_ROOT


def workspace_paths() -> dict[str, Path]:
    root = workspace_root()
    return {
        "root": root,
        "uploads": root / "data" / "uploads",
        "exports": root / "data" / "exports",
        "scripts": root / "scripts",
        "runs": root / "runs",
        "warehouse": root / "warehouse",
        "metadata": root / "metadata",
        "database": root / "warehouse" / "kriyax.duckdb",
        "catalog": root / "metadata" / "catalog.json",
        "connections": root / "metadata" / "connections.json",
        "llm_settings": root / "metadata" / "llm-settings.vault",
        "llm_master_key": root / "metadata" / "llm-master.key",
        "pipelines": root / "metadata" / "pipelines.json",
        "pipeline_failures": root / "metadata" / "pipeline-failures.json",
        "odoo_sync_cursors": root / "metadata" / "odoo-sync-cursors.json",
        "import_drafts": root / "metadata" / "import-drafts.json",
    }


def ensure_workspace() -> dict[str, str]:
    paths = workspace_paths()
    for key in ["uploads", "exports", "scripts", "runs", "warehouse", "metadata"]:
        paths[key].mkdir(parents=True, exist_ok=True)

    for key in ["catalog", "connections", "pipelines", "import_drafts"]:
        if not paths[key].exists():
            paths[key].write_text("[]\n", encoding="utf-8")
    if not paths["pipeline_failures"].exists():
        paths["pipeline_failures"].write_text("{}\n", encoding="utf-8")
    if not paths["odoo_sync_cursors"].exists():
        paths["odoo_sync_cursors"].write_text("[]\n", encoding="utf-8")

    return {name: str(path) for name, path in paths.items()}
