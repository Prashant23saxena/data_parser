---
name: kriyax-script-workbench
description: Use when operating the KriyaX Script Workbench through Python scripts, including catalog inspection, table viewing, transformations, audit verification, and agent-assisted data work.
---

# KriyaX Script Workbench

Work from:

```bash
cd /Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-script-workbench
```

Use `.venv/bin/python tools/*.py` for product actions.

Do not run `workspace/scripts/*.py` directly. Use:

```bash
.venv/bin/python tools/script_run.py script_name.py
```

This injects `load_table()`, `save_table()`, and `show()`, and writes deterministic audit records.

Start by grounding yourself with deterministic context:

```bash
.venv/bin/python tools/agent_context.py
.venv/bin/python tools/db_viewer_info.py
```

Read that output before choosing tables, scripts, or next commands. Prefer this context pack over optional in-app LLM utilities.

Before writing or changing transformation code:

```bash
.venv/bin/python tools/catalog_list.py
.venv/bin/python tools/table_describe.py schema.table
.venv/bin/python tools/table_view.py schema.table --limit 20
```

After any write action:

```bash
.venv/bin/python tools/catalog_list.py
.venv/bin/python tools/table_view.py schema.table --limit 20
.venv/bin/python tools/db_viewer_info.py
.venv/bin/python tools/audit_tail.py --limit 10
```

Never manually edit `workspace/audit/*`.

If the user wants to inspect data visually after a join/import/cleaning step, prefer DBCode or another DuckDB-compatible viewer. Run `tools/db_viewer_info.py` and return the database file path. Use `tools/table_html.py` only as a fallback.
