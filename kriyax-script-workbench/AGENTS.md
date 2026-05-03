# KriyaX Script Workbench Agent Instructions

Work from:

```bash
cd /Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-script-workbench
```

Use `python tools/*.py` for product actions. Do not run `workspace/scripts/*.py` directly.

Start every work session with:

```bash
.venv/bin/python tools/agent_context.py
.venv/bin/python tools/db_viewer_info.py
```

Use that deterministic context before making assumptions about tables, scripts, prior runs, or failures.

Before writing transformation code:

```bash
.venv/bin/python tools/catalog_list.py
.venv/bin/python tools/table_describe.py schema.table
.venv/bin/python tools/table_view.py schema.table --limit 20
```

Write user transformations in `workspace/scripts/*.py` using:

```python
df = load_table("schema.table")
show(df, name="preview")
save_table(df, "new_table", schema="curated")
```

After any data write or script run:

```bash
.venv/bin/python tools/catalog_list.py
.venv/bin/python tools/table_view.py schema.table --limit 20
.venv/bin/python tools/db_viewer_info.py
.venv/bin/python tools/audit_tail.py --limit 10
```

Never manually edit `workspace/audit/*`. It is system-owned evidence.

When the user asks to see data visually, prefer DBCode or another DuckDB-compatible viewer. Run `tools/db_viewer_info.py` and report the database file path. Use `tools/table_html.py` only as a fallback when no DB viewer is available.
