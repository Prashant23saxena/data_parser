# Backend Execution Model — Local Python Execution Wrapper

**Status:** DRAFT
**Last updated:** 2026-05-02

## Direction

The product should stay bare-bones and understandable:

- User-authored transformations are saved as real `.py` files in the workspace.
- The UI writes script metadata, but the script itself remains a normal Python file.
- Running a script uses the laptop's configured Python, usually a project `.venv/bin/python` or system `python`.
- The app adds a thin execution wrapper around that Python call so it can provide helper functions such as `load_table(name)` and `save_table(df, name, schema=None)`.
- Tables live in the local backing database, currently modeled as DuckDB.
- File uploads and Odoo pulls land as new tables.
- Pipeline runs execute the saved `.py` script on a schedule and store run logs/status.

## Proposed workspace shape

```text
kriyax-workspace/
  data/
    uploads/
    exports/
  scripts/
    clean_customers.py
    inventory_rollup.py
  runs/
    customer_sync/
      2026-05-02T10-30-00.log
      2026-05-02T10-30-00.json
  warehouse/
    kriyax.duckdb
  metadata/
    catalog.json
    connections.json
    pipelines.json
```

## Runtime contract

1. User writes or generates Python/pandas code in Code Workspace.
2. User saves it as a `.py` file under `scripts/`.
3. User clicks Run, or a pipeline scheduler triggers the script later.
4. The app calls the configured local Python with a small wrapper/context module.
5. `load_table()` reads from DuckDB into pandas.
6. `save_table()` writes a DataFrame back as a new/derived table.
7. Run output, traceback, duration, and affected tables are saved under `runs/` and surfaced in Pipeline Run Detail.

## Why this fits the product

- It is simpler than a full notebook/Jupyter system.
- It is transparent: users can inspect the actual Python files.
- It supports scheduling without inventing a separate transform format.
- It keeps the UI and backend aligned: Code Workspace, Saved Scripts, Pipelines, and Run Detail all point at the same script artifact.

## Open design points

- Whether schema names are physical DuckDB schemas or logical storage zones exposed by the app.
- Whether the first implementation uses pandas only or allows Polars later internally.
- Which local Python should be used by default: project `.venv/bin/python` first, then system `python`.
- How strict the execution wrapper should be for local/internal use.
