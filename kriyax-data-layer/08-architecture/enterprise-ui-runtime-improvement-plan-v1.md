# Enterprise UI + Runtime Improvement Plan v1

**Date:** 2026-05-03
**Mode:** Plan first, no implementation in this pass.
**App:** KriyaX Data Layer
**Current app URL:** `http://127.0.0.1:5173`

## References Reviewed

- Current app screenshots:
  - `visuals/connectors-polish.png`
  - `visuals/catalog-final.png`
  - `visuals/code-workspace-final.png`
  - `visuals/storage-llm-final.png`
- Generated enterprise reference:
  - `visuals/sleek-ui-reference-board.png`
  - `visuals/sleek-catalog-agent-reference.png`
- Existing audit:
  - `08-architecture/feature-availability-audit-v1.md`

## Diagnosis

The app is functionally strong but visually and interaction-wise still reads like a scaffold. The main issues are not isolated colors or icons; they are product-system problems:

1. The shell behaves manually instead of intelligently.
2. Detail pages are missing navigation affordances.
3. Connectors are too plain and icon treatment is inconsistent.
4. Catalog and Code Workspace waste vertical/horizontal space.
5. The Code Workspace table browser should be hierarchical, not a flat button list.
6. LLM setup exists, but there is no visible playground/test path, so the Agent feels disconnected.
7. Script execution returns text logs but not a proper tabular result explorer.
8. The current styling uses too much generic card/panel spacing and not enough enterprise-density layout.

## Target Product Standard

The app should feel closer to Databricks / Hex / Snowflake-style tooling than a demo dashboard:

- Compact persistent shell with hover expansion.
- Dense tables, sticky headers, filter bars, small action buttons.
- Hierarchical object browsers for schemas and tables.
- Result grids with stdout/stderr kept secondary.
- Clear workspace breadcrumbs and back actions.
- Provider playground and Agent status should be visible where the user expects to test runtime behavior.
- Icons should be subdued, functional, and source-specific, not decorative.

## Work Package A — Intelligent Sidebar Shell

### Problem

The sidebar currently has a manual collapse button and stays open unless clicked. User expectation: if the cursor is not over it for 2 seconds, it should minimize automatically. On hover, it should expand automatically. No collapse button should be needed.

### Files

- `kriyax-data-app/frontend/src/App.tsx`
- `kriyax-data-app/frontend/src/styles.css`

### Changes

- Replace `sidebarCollapsed` manual toggle with hover-intent state:
  - Default state: collapsed after initial mount.
  - `onMouseEnter`: expand immediately.
  - `onMouseLeave`: start 2-second timer, then collapse.
  - Clear timer on re-enter.
- Remove the visible collapse button.
- Keep icon-only collapsed rail always usable.
- Use tooltips/titles for collapsed nav labels.
- Preserve active-route highlighting in both expanded and collapsed states.
- Ensure sidebar expansion does not resize content jarringly:
  - Use CSS transition on grid column width.
  - Recommended: collapsed `72px`, expanded `232px`.

### Acceptance Criteria

- Sidebar expands on hover.
- Sidebar collapses automatically 2 seconds after mouse leaves.
- No manual collapse/expand button is visible.
- All top-level routes remain accessible in collapsed mode.
- Playwright verifies hover expand/collapse timing.

## Work Package B — Enterprise Icon + Connector Redesign

### Problem

The connector icons and cards feel cartoonish. File upload and Odoo do not visually read as professional source connectors. The generated board had stronger connector tiles with badges, recent status, and proper source identity.

### Files

- `kriyax-data-app/frontend/src/App.tsx`
- `kriyax-data-app/frontend/src/styles.css`

### Changes

- Replace current connector action rows with source cards:
  - File Upload card: document/table icon, CSV/XLSX badges, recent imports list, primary action.
  - Odoo card: integration/source icon, connection status, model/delta-sync badges, primary action.
- Use lucide icons only, but choose restrained ones:
  - File: `FileSpreadsheet` or `FileUp`
  - Odoo/source: `Network`, `Boxes`, or `Plug`
  - Avoid oversized colored square icon backgrounds.
- Add a compact "Connector capabilities" strip:
  - Auto schema detection
  - Preview before import
  - Incremental sync
  - Table auto-creation
- Reduce empty page space by constraining the connector grid to the useful content width and adding useful status content rather than blank canvas.

### Acceptance Criteria

- Connectors page matches the reference board structure.
- Icons are subtle, consistent, and professional.
- File/Odoo are visually distinct but part of one design system.
- Clicking File/Odoo still drills into `/connectors/file-import` and `/connectors/odoo`.

## Work Package C — Global Breadcrumbs + Back Navigation

### Problem

Detail pages such as Table Detail, Manage Table, Export Table, File Import, Odoo Import, Agent view, and Pipeline Run Detail do not show a clear back button. The user must click the parent nav item, which feels unfinished.

### Files

- `kriyax-data-app/frontend/src/App.tsx`
- `kriyax-data-app/frontend/src/styles.css`

### Changes

- Add route metadata:
  - `parentPath`
  - `parentLabel`
  - `breadcrumb`
  - optional `primaryAction`
- Topbar should show:
  - Back button for nested routes.
  - Breadcrumb: `Catalog > Table Detail`, `Connectors > File Import`, etc.
  - Page title and compact subtitle.
- Back button behavior:
  - `/connectors/file-import` -> `/connectors`
  - `/connectors/odoo` -> `/connectors`
  - `/catalog/table*` -> `/catalog`
  - `/code/agent` -> `/code`
  - `/pipelines/run` -> `/pipelines`
- Make back button icon-only with tooltip plus label on wider screens.

### Acceptance Criteria

- Every nested/detail page has a visible back affordance.
- Browser back still works normally.
- Playwright verifies Table Detail -> Back -> Catalog.

## Work Package D — Catalog Density + Detail Behavior

### Problem

Catalog is usable, but still has too much whitespace and the table/detail relationship does not feel like an enterprise data catalog.

### Files

- `kriyax-data-app/frontend/src/App.tsx`
- `kriyax-data-app/frontend/src/styles.css`

### Changes

- Keep Catalog as a dense table registry.
- Improve toolbar:
  - Search
  - Schema filter
  - Source filter
  - Refresh
  - Compact metrics: total tables, schemas, rows, last updated.
- Keep expanded row inline, but make it more structured:
  - Overview column
  - Columns preview
  - Row preview if available
  - Actions on the right
- Add sticky table header.
- Reduce row height and padding.
- Add horizontal scrolling only when needed.
- Table Detail page:
  - Add Back to Catalog.
  - Split content into compact tabs: Overview, Columns, Preview.
  - Avoid large full-width panels when only metadata exists.

### Acceptance Criteria

- Catalog first viewport shows useful table rows and filters.
- Expanded row looks like the generated reference, not a loose info band.
- Table Detail has a clear parent navigation path.

## Work Package E — Databricks-Style Schema/Table Browser in Code Workspace

### Problem

Available Tables is a flat list of large buttons. It consumes too much space and does not scale. User expects schema accordion behavior like Databricks: schema -> tables.

### Files

- `kriyax-data-app/frontend/src/App.tsx`
- `kriyax-data-app/frontend/src/styles.css`

### Changes

- Replace flat `table-picker-list` with `SchemaBrowser`.
- Group catalog tables by schema:
  - `raw_files`
  - `raw_odoo`
  - `curated`
  - `staging`
- Each schema row:
  - Chevron accordion.
  - Table count.
  - Optional search within tables.
- Each table row:
  - Table icon.
  - Table name only, not full schema prefix.
  - Row count and column count in muted text.
  - Inline actions on hover:
    - Insert load
    - Preview
    - Open catalog
- Default expanded schemas:
  - Most recently used schema.
  - Or schema of currently loaded table.
- Add a narrow browser width:
  - Default `220px`.
  - Resizable later if needed, but not in this pass.
- Reduce Code Workspace spacing:
  - More editor height.
  - Less gap between editor and output.
  - Agent panel should not force large whitespace.

### Acceptance Criteria

- Code Workspace left panel is hierarchical and compact.
- User can insert `load_table("schema.table")` from a table row.
- User can preview a table without leaving Code Workspace.
- Layout fits editor, output, and agent in one desktop viewport.

## Work Package F — Script Result Table Explorer

### Problem

After running Python, the app shows success/log text, but not a proper table output. User expects a result/grid explorer similar to notebook/data platforms.

### Backend Files

- `kriyax-data-app/backend/app/services/execution.py`
- `kriyax-data-app/backend/app/api/execution.py`
- `kriyax-data-app/backend/tests/test_execution.py`
- `kriyax-data-app/backend/tests/test_execution_api.py`

### Frontend Files

- `kriyax-data-app/frontend/src/api.ts`
- `kriyax-data-app/frontend/src/App.tsx`
- `kriyax-data-app/frontend/src/styles.css`
- `kriyax-data-app/frontend/e2e/code-workspace.spec.ts`

### Changes

- Extend script execution response with structured result artifacts:
  - `resultTables`: saved tables from `save_table()`.
  - `preview`: first saved table preview, if any.
  - `displayFrames`: optional preview if script calls a helper like `show(df)` or returns a DataFrame.
- Add helper in execution wrapper:
  - `show(df, name="result")` captures a dataframe preview.
  - Limit rows to 100 and columns to a safe count.
- Frontend Run Output becomes tabbed:
  - `Result`
  - `stdout`
  - `stderr`
  - `Saved tables`
- Result tab shows:
  - Data grid.
  - Row/column count.
  - Open in Catalog.
  - Export CSV if saved.
- Keep stdout/stderr visible but secondary.

### Acceptance Criteria

- Running a script that saves a table shows a table preview.
- Running `show(df)` shows an unsaved result grid.
- E2E verifies result grid cells are visible.

## Work Package G — LLM Playground + Provider Runtime Test

### Problem

LLM provider setup exists under Storage, but there is no playground to test a real provider. The Agent feels "not running" because there is no visible runtime status or test path.

### Backend Files

- `kriyax-data-app/backend/app/services/llm_settings.py`
- `kriyax-data-app/backend/app/api/llm.py`
- New: `kriyax-data-app/backend/app/services/llm_gateway.py`
- `kriyax-data-app/backend/app/services/agent.py`
- `kriyax-data-app/backend/tests/test_llm_api.py`
- New: `kriyax-data-app/backend/tests/test_llm_gateway.py`
- Update: `kriyax-data-app/backend/requirements.txt` only if provider SDKs are chosen. Prefer `httpx` first to avoid dependency sprawl.

### Frontend Files

- `kriyax-data-app/frontend/src/api.ts`
- `kriyax-data-app/frontend/src/App.tsx`
- `kriyax-data-app/frontend/src/styles.css`
- New/updated E2E for LLM settings and agent status.

### Changes

- Add `/api/llm/playground`:
  - Input: provider, prompt, optional model override.
  - Uses saved encrypted key.
  - Returns response text, model, latency, status.
- Add `/api/llm/status`:
  - Shows active provider.
  - Shows whether key exists.
  - Never returns the key.
- Storage page gains `LLM Playground` section:
  - Prompt textbox.
  - Provider selector.
  - Test button.
  - Response output.
  - Latency/status chip.
- Agent dock gains runtime banner:
  - `Using OpenAI gpt-...`
  - `Using Anthropic claude-...`
  - or `No provider configured: deterministic fallback`
- Agent generate/correct/follow-up should use real LLM when provider is configured.
- Deterministic local generation remains fallback for no-key and tests.

### Acceptance Criteria

- User can save OpenAI or Anthropic key, test a prompt, and see model output.
- Agent visibly says whether it is using real LLM or fallback.
- Raw API key never appears in UI, API responses, screenshots, logs, or test output.

## Work Package H — Agent UX as Real Work Panel

### Problem

Agent panel currently looks like three stacked forms. It should feel like a coding assistant/workbench.

### Files

- `kriyax-data-app/frontend/src/App.tsx`
- `kriyax-data-app/frontend/src/styles.css`
- Backend agent files if real LLM is wired in Work Package G.

### Changes

- Convert Agent dock to a compact chat/work panel:
  - Runtime status header.
  - Prompt input at bottom.
  - Message stream.
  - Generated code block with actions: Insert, Replace editor, Copy.
  - Error correction card appears when last run failed.
- Add "Use last error" button:
  - Pulls latest `stderr`/traceback from Code Workspace run result into correction prompt.
- Agent should feel docked into Code Workspace, not like a separate screen.

### Acceptance Criteria

- Agent can generate code, insert code, and correct last run error from one panel.
- No need to guess what command to type to start the Agent.
- UI shows provider/fallback state.

## Work Package I — Enterprise Design System Pass

### Problem

The UI is still too home-made. The reference works because it has a stricter design system: tighter density, smaller controls, less playful icon treatment, clear grids, and better hierarchy.

### Files

- `kriyax-data-app/frontend/src/styles.css`
- `kriyax-data-app/frontend/src/App.tsx`

### Changes

- Create consistent component classes:
  - `app-page`
  - `page-toolbar`
  - `data-panel`
  - `data-table`
  - `status-chip`
  - `icon-button`
  - `source-card`
  - `object-browser`
  - `result-grid`
- Reduce default spacing:
  - Page gap: 12px.
  - Panel padding: 12px.
  - Table cell padding: 6px 8px.
  - Buttons: 30-34px height.
- Remove oversized empty panels.
- Avoid pale icon blocks unless they communicate status.
- Use restrained color:
  - Dark shell.
  - Lime only for active state/primary run.
  - Green/red/yellow only for status.
  - No decorative tinting.
- Improve type scale:
  - Page title 22-24px.
  - Panel title 14px.
  - Dense metadata 12px.

### Acceptance Criteria

- Screens visually align with `sleek-ui-reference-board.png`.
- First viewport has useful density on Connectors, Catalog, Code Workspace, Pipelines, and Storage.
- No obvious blank canvas unless the workspace is genuinely empty.

## Work Package J — Empty State + Large Workspace UAT

### Problem

The audit still has UAT-010, UAT-011, and UAT-012 open. These overlap with the current professional polish issue.

### Files

- `kriyax-data-layer/08-architecture/checklist.md`
- Frontend E2E files.
- Backend tests as needed.

### Changes

- Empty workspace:
  - Ensure every screen has useful guidance and no awkward blank page.
- Large-ish local data:
  - Seed 100+ catalog tables and verify Catalog/Code Browser remain usable.
  - Add scroll bounds and sticky headers.
- Local-only privacy:
  - Verify LLM keys stay encrypted.
  - Verify no key is returned from API.
  - Verify all project files stay under workspace root.

### Acceptance Criteria

- UAT-010, UAT-011, UAT-012 can be checked off.
- Playwright covers the large-catalog layout.

## Recommended Build Order

1. **Shell + navigation foundation**
   - Work Package A
   - Work Package C

2. **Enterprise density and connector/catalog polish**
   - Work Package B
   - Work Package D
   - Work Package I base CSS classes

3. **Code Workspace productivity**
   - Work Package E
   - Work Package F

4. **LLM runtime and playground**
   - Work Package G
   - Work Package H

5. **UAT hardening**
   - Work Package J

## Concrete Implementation Sequence

### Step 1 — Shell Hover Collapse

- Edit `App.tsx` sidebar state.
- Remove collapse button markup.
- Add hover handlers and timer cleanup.
- Edit sidebar CSS transition.
- Add Playwright hover timing test.

### Step 2 — Topbar Breadcrumbs

- Add route metadata helper in `App.tsx`.
- Update topbar rendering.
- Add `Back` icon button.
- Verify every nested route has parent path.

### Step 3 — Connector Cards

- Replace `Connectors()` panel layout.
- Add source-card CSS.
- Use badges/status rows/recent imports.
- Make icons smaller and less decorative.

### Step 4 — Catalog Toolbar + Inline Detail

- Tighten existing toolbar and table.
- Add source filter.
- Improve expanded row layout.
- Add detail tabs/back button.

### Step 5 — Schema Browser

- Add grouping helper in `CodeWorkspace`.
- Build `SchemaBrowser` component inside `App.tsx` first; extract later only if needed.
- Add preview action and route/open action.

### Step 6 — Result Explorer

- Extend backend execution contract.
- Add `show(df)` helper.
- Return preview tables.
- Add frontend output tabs and result grid.

### Step 7 — LLM Playground + Gateway

- Add gateway service using saved profile.
- Add status/playground endpoints.
- Add Storage playground UI.
- Add Agent runtime status.
- Wire Agent to real LLM when configured.

### Step 8 — Agent Workbench

- Convert forms into message/action panel.
- Add use-last-error correction flow.
- Keep deterministic fallback for no-key.

### Step 9 — Full Regression + Screenshot QA

- Backend: `.venv/bin/python -m pytest`
- Frontend: `npm run build`
- E2E: `npm run e2e`
- Screenshot QA:
  - Connectors
  - File Import
  - Catalog
  - Table Detail
  - Code Workspace with Agent
  - Storage with LLM Playground
  - Pipeline Run Detail

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Sidebar hover behavior feels jumpy | Annoying shell UX | Use delayed collapse only, instant expand, and smooth width transition. |
| Real LLM tests become flaky | CI/local test instability | Mock gateway in tests; keep live playground manual. |
| Result explorer bloats execution payload | Slow UI for big frames | Limit preview rows/columns, keep full data in DuckDB. |
| Large catalog slows rendering | Bad professional feel | Cap visible rows, sticky scroll container, schema accordion. |
| Too much redesign at once breaks E2E | Regression churn | Ship in the recommended order and update tests per WP. |

## Definition Of Done For This Improvement Pass

- Sidebar auto-collapses and expands on hover.
- Detail pages have back/breadcrumb navigation.
- Connectors look like professional source cards.
- Catalog is dense, searchable, and not blank-heavy.
- Code Workspace uses schema/table accordion browser.
- Script run output includes a proper result grid/table explorer.
- Storage includes LLM Provider Setup and LLM Playground.
- Agent clearly shows real provider vs fallback and can be tested.
- All existing E2E flows still pass, plus new coverage for sidebar, breadcrumbs, result grid, LLM playground, and large catalog.
