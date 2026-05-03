# KriyaX Data Layer App

First runnable implementation of the frozen SPS design contract in `../kriyax-data-layer`.

## Current scope

Implemented:

- FastAPI backend shell.
- Workspace folder bootstrap.
- DuckDB storage health endpoint.
- React/Vite frontend shell.
- Sidebar navigation for all 14 approved screens.
- Storage Settings screen wired to backend status.
- CSV/XLSX upload inspection with preview rows.
- Editable import column mapping and selected types.
- New DuckDB table creation under user-selected schemas.
- Catalog registration and table preview APIs.
- File Import, Catalog, and Table Detail screens wired to real backend data.
- Catalog row Open action routes to the exact selected table detail.
- Code Workspace available table list is wired to catalog data.
- Code Workspace can save and run real `.py` scripts with `load_table()` and `save_table()`.
- Run output captures stdout/stderr and derived tables are registered in Catalog.
- Saved Scripts lists persisted `.py` files and can open them back into Code Workspace for rerun.
- Phase 2 Odoo connector slice: connection normalization, XML-RPC test connection, masked save/list connections, model browsing, field metadata browsing, selected-field fetch into DuckDB, Odoo catalog registration, and S-04 UI wiring.
- Phase 3 pipeline slice: create saved-script pipelines, enable/disable pipelines, run manually, persist run history/status/logs, and inspect S-13 run detail.
- Enterprise UI/runtime pass: hover-auto-collapsing sidebar, global breadcrumbs/back navigation, professional connector source cards, denser Catalog tabs, Code Workspace schema/table browser, structured result grids for `save_table()` and `show(df)`, LLM playground/status, and Agent workbench runtime fallback.

## Project layout

```text
kriyax-data-app/
  backend/
    app/
      api/
      services/
      main.py
    requirements.txt
  frontend/
    src/
    package.json
  workspace/
    data/uploads/
    data/exports/
    scripts/
    runs/
    warehouse/kriyax.duckdb
    metadata/
```

## Run backend

```bash
cd /Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-data-app/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8001
```

## Run frontend

```bash
cd /Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-data-app/frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173/`.

## Run tests

Backend unit/API tests:

```bash
cd /Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-data-app/backend
.venv/bin/python -m pytest
```

Frontend build:

```bash
cd /Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-data-app/frontend
npm run build
```

Translated SPS browser scenarios:

```bash
# Keep backend and frontend running first.
cd /Users/shivanitidke/Desktop/Kriya_DataParser/kriyax-data-app/frontend
npm run e2e
```

Current E2E coverage maps to Phase 1 file-import/code scenarios, Phase 2 Odoo UI wiring, Phase 3 manual pipeline execution, and the enterprise runtime polish pass:

- Import a CSV through the UI, create a DuckDB table, see it in Catalog, and verify Table Detail preview.
- Open the exact imported table from the Catalog row action.
- See the imported table in Code Workspace available tables.
- Run Python code that loads a table and saves a derived table.
- Verify the derived table appears in Code Workspace after execution.
- Open a saved script from S-11 back into Code Workspace and rerun it.
- Block duplicate target column names until the user renames them.
- Mock an Odoo connection, browse models/fields, select supported fields, and fetch records into a catalog table.
- Create a pipeline from a saved script, disable it, run it manually, and inspect run detail logs.
- Verify sidebar hover expansion and 2-second auto-collapse.
- Verify Table Detail breadcrumb/back navigation through Catalog.
- Verify Code Workspace result grid cells from a saved dataframe preview.
- Verify Storage LLM Playground fallback output without leaking raw keys.

## Current live slices

Phase 1 now supports the first real import-to-derived-table path:

1. Upload CSV/XLSX.
2. Choose target schema/storage area.
3. Edit column names and types.
4. Preview rows.
5. Create new DuckDB table.
6. Register it in catalog metadata.
7. Show it in Catalog and Table Detail.
8. Run Python against the table with `load_table()`.
9. Save a derived table with `save_table()`.
10. Reopen and rerun saved scripts.

Phase 2 now supports the first real Odoo import path:

1. Enter Odoo connection details.
2. Test and save the connection.
3. Load and search Odoo models.
4. Open a model and inspect field names, labels, types, relation targets, and supported/unsupported status.
5. Select supported fields.
6. Fetch records into a new DuckDB table.
7. Register the Odoo table in Catalog.
8. Load the Odoo table from Code Workspace through the existing catalog-backed table list.

Phase 3 now supports the first saved-script pipeline path:

1. Create a pipeline from a saved `.py` script.
2. Enable or disable the pipeline.
3. Run the pipeline manually even while disabled.
4. Persist run records under workspace runs.
5. Show last run status in S-12 Pipelines.
6. Open S-13 Pipeline Run Detail with status, duration, script reference, logs, and saved tables.

Enterprise runtime now supports the professional workbench path:

1. Use an icon-only sidebar that expands on hover and collapses after mouse leave.
2. Navigate nested screens with breadcrumbs and parent Back actions.
3. Open File and Odoo connectors from source cards with source capabilities and recent status.
4. Filter Catalog by search, schema, and source, then inspect table detail through Overview, Columns, and Preview tabs.
5. Browse Code Workspace tables by schema accordion and insert `load_table("schema.table")`.
6. Run Python and inspect the first saved or displayed dataframe in a result grid.
7. Test LLM runtime from Storage playground and see Agent provider/fallback status in the workbench.

## Next build target

Continue UAT hardening and scale validation.

1. Seed/check a 100+ table workspace against Catalog and Schema Browser scroll behavior.
2. Add explicit empty-workspace checks for every screen.
3. Add a manual live-provider playground checklist for real OpenAI/Anthropic credentials.
4. Review remaining UAT-010, UAT-011, and UAT-012 checklist items in the architecture docs.
