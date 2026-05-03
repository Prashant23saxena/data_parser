# KriyaX Script Workbench

Barebones Python-first data workbench for KriyaX.

This is a separate application from `kriyax-data-app`. It is designed to be operated by Codex, Antigravity, or a human from the terminal using real Python scripts, deterministic audit logs, and local DuckDB storage.

## Storage Model

```text
kriyax-script-workbench/
  workspace/
    warehouse/kriyax.duckdb       # actual table data
    metadata/catalog.json         # table registry
    data/uploads/                 # permanent copy of imported source files
    data/exports/                 # CSV/HTML exports when needed
    scripts/*.py                  # user/agent transformation scripts
    runs/                         # stdout/stderr/run summaries
    audit/audit.jsonl             # append-only action trace
    audit/snapshots/*.py          # exact script code that ran
```

Tables are stored in DuckDB as schema-qualified names:

```text
raw_files.orders
odoo.sale_order
curated.region_revenue
```

The catalog is only metadata. The actual rows live in `workspace/warehouse/kriyax.duckdb`.

When a file is imported, the workbench first copies the source file into `workspace/data/uploads/` and then imports from that preserved evidence copy. The catalog stores both the original path and the preserved workspace path.

## Install

```bash
cd /Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-script-workbench
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## First Commands

```bash
.venv/bin/python tools/workspace_status.py
.venv/bin/python tools/agent_context.py
.venv/bin/python tools/catalog_list.py
.venv/bin/python tools/script_run.py example_join.py
.venv/bin/python tools/audit_tail.py --limit 10
```

## Capability Map

### Workspace and Audit

```bash
.venv/bin/python tools/workspace_status.py
.venv/bin/python tools/agent_context.py
.venv/bin/python tools/agent_context.py --output workspace/context/current.md
.venv/bin/python tools/db_viewer_info.py
.venv/bin/python tools/audit_tail.py --limit 20
.venv/bin/python tools/audit_show.py <event-id>
.venv/bin/python tools/audit_verify.py <event-id>
```

### File Import

```bash
.venv/bin/python tools/file_inspect.py ./orders.csv --json
.venv/bin/python tools/file_import.py ./orders.csv --schema raw_files --table orders --auto
```

### Catalog and Tables

```bash
.venv/bin/python tools/catalog_list.py
.venv/bin/python tools/catalog_search.py amount
.venv/bin/python tools/table_describe.py raw_files.orders
.venv/bin/python tools/table_view.py raw_files.orders --limit 20
.venv/bin/python tools/db_viewer_info.py
.venv/bin/python tools/table_export.py raw_files.orders
.venv/bin/python tools/table_html.py raw_files.orders --limit 100
.venv/bin/python tools/table_export.py raw_files.orders --format html --limit 100
.venv/bin/python tools/table_rename.py raw_files.orders raw_files.orders_v2
.venv/bin/python tools/table_truncate.py raw_files.orders_v2 --confirm raw_files.orders_v2
.venv/bin/python tools/table_drop.py raw_files.orders_v2 --confirm raw_files.orders_v2
```

### Scripts and Transformations

```bash
.venv/bin/python tools/script_create.py revenue_by_region.py --template join
.venv/bin/python tools/script_list.py
.venv/bin/python tools/script_show.py revenue_by_region.py
.venv/bin/python tools/script_run.py revenue_by_region.py
```

### Agent/LLM

```bash
.venv/bin/python tools/llm_status.py
.venv/bin/python tools/llm_test.py "Say ready"
.venv/bin/python tools/agent_generate.py "join orders and customers" --save revenue_by_region.py
.venv/bin/python tools/agent_fix.py --script revenue_by_region.py --traceback-file /tmp/traceback.txt --save
.venv/bin/python tools/agent_follow_up.py --script revenue_by_region.py "filter to this year" --save
```

By default, the workbench reuses the existing encrypted LLM profile from the sibling `kriyax-data-app/workspace/metadata/` vault when local environment variables are not set. Override with `KRIYAX_LEGACY_LLM_METADATA=/path/to/metadata` or normal provider variables such as `KRIYAX_LLM_PROVIDER`, `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL`, and `ANTHROPIC_BASE_URL`.

The LLM layer is optional when a coding agent such as Codex or Antigravity is operating the app. The primary agent entry point is deterministic context:

```bash
.venv/bin/python tools/agent_context.py
```

That command summarizes workspace paths, tables, columns, saved scripts, pipelines, active failures, recent audit, and recommended next commands.

### Odoo

```bash
.venv/bin/python tools/odoo_test_connection.py --url https://example.odoo.com --database db --username user --api-key key
.venv/bin/python tools/odoo_save_connection.py --name production --url https://example.odoo.com --database db --username user --api-key key
.venv/bin/python tools/odoo_list_connections.py
.venv/bin/python tools/odoo_models.py --connection production --search sale
.venv/bin/python tools/odoo_fields.py --connection production --model sale.order
.venv/bin/python tools/odoo_fetch.py --connection production --model sale.order --fields id,name,amount_total,write_date --schema odoo --table sale_order
.venv/bin/python tools/odoo_cursor_create.py --connection production --model sale.order --fields id,name,amount_total,write_date --schema odoo --table sale_order --cursor-field write_date
.venv/bin/python tools/odoo_sync.py <cursor-id>
```

### Pipelines

```bash
.venv/bin/python tools/pipeline_create.py "Revenue refresh" --script revenue_by_region.py
.venv/bin/python tools/pipeline_schedule.py <pipeline-id> --hourly
.venv/bin/python tools/pipeline_schedule.py <pipeline-id> --daily 06:00
.venv/bin/python tools/pipeline_enable.py <pipeline-id> false
.venv/bin/python tools/pipeline_run.py <pipeline-id>
.venv/bin/python tools/pipeline_runs.py --pipeline <pipeline-id>
.venv/bin/python tools/pipeline_failures.py
.venv/bin/python tools/pipeline_ack_failure.py <run-id>
.venv/bin/python tools/pipeline_process_due.py
```

## Transformation Contract

Scripts in `workspace/scripts/` should use:

```python
orders = load_table("raw_files.orders")
customers = load_table("raw_files.customers")

joined = orders.merge(customers, on="customer_id", how="left")
result = joined.groupby("region", as_index=False)["amount"].sum()

show(result, name="preview")
save_table(result, "region_revenue", schema="curated")
```

Do not run scripts directly with `python workspace/scripts/name.py`. Always use:

```bash
.venv/bin/python tools/script_run.py name.py
```

That is what injects helpers and writes audit evidence.

After a join/import/cleaning step, use:

```bash
.venv/bin/python tools/catalog_list.py
.venv/bin/python tools/table_view.py curated.region_revenue --limit 20
.venv/bin/python tools/db_viewer_info.py
.venv/bin/python tools/audit_tail.py --limit 10
```

Use terminal previews for quick checks. For visual inspection, connect DBCode or another DuckDB-compatible viewer to the database file printed by `tools/db_viewer_info.py`. HTML export remains available as a fallback when a DB viewer is not available.

## DBCode / Database Viewer

The workbench writes a DB viewer metadata file at:

```text
workspace/metadata/db-viewer.json
```

Run:

```bash
.venv/bin/python tools/db_viewer_info.py
```

Then connect DBCode to the printed DuckDB database file:

```text
workspace/warehouse/kriyax.duckdb
```

Use DBCode to browse schemas/tables and run ad hoc inspection queries. Keep audited writes in the workbench scripts. If DuckDB reports a lock while an agent is writing, disconnect the DB viewer and rerun the workbench command.

## Verify

```bash
PYTHONPATH=src .venv/bin/python -m pytest tests -v
PYTHONPATH=src .venv/bin/python -m compileall src tools tests
```
