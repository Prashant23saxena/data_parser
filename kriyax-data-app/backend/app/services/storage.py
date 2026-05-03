from datetime import datetime, timezone

from app.services.workspace import ensure_workspace, workspace_paths


def storage_status() -> dict[str, object]:
    paths = workspace_paths()
    ensure_workspace()

    try:
        import duckdb

        with duckdb.connect(str(paths["database"])) as conn:
            conn.execute("select 1").fetchone()
        database_ready = True
        error = None
    except Exception as exc:  # pragma: no cover - exact driver errors vary by system
        database_ready = False
        error = str(exc)

    return {
        "status": "ready" if database_ready else "unreachable",
        "databaseReady": database_ready,
        "databasePath": str(paths["database"]),
        "workspaceRoot": str(paths["root"]),
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "error": error,
    }
