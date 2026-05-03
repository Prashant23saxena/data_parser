### [2026-05-03 16:48:50]

**Changes:**
- Added encrypted local OpenAI/Anthropic LLM provider setup under Storage.
- Applied the sleek UI reference direction across the shell, Catalog, Code Workspace, and Storage surfaces.
- Added a feature availability audit and remaining implementation plan.

**Files Affected:**
- `kriyax-data-app/backend/app/services/workspace.py`: Added LLM vault and master-key paths to the project workspace.
- `kriyax-data-app/backend/app/services/llm_settings.py`: Added Fernet-encrypted local LLM profile persistence.
- `kriyax-data-app/backend/app/api/llm.py`: Added LLM settings and readiness endpoints.
- `kriyax-data-app/backend/app/main.py`: Registered the LLM API router.
- `kriyax-data-app/backend/requirements.txt`: Added `cryptography` for credential encryption.
- `kriyax-data-app/backend/tests/test_llm_settings.py`: Added LLM vault service tests.
- `kriyax-data-app/backend/tests/test_llm_api.py`: Added LLM API tests.
- `kriyax-data-app/frontend/src/api.ts`: Added LLM settings client types and API helpers.
- `kriyax-data-app/frontend/src/App.tsx`: Added Storage LLM setup UI, live Home metrics, Catalog search/filter, and improved Code Workspace table picker.
- `kriyax-data-app/frontend/src/styles.css`: Applied professional UI polish and new layout classes.
- `kriyax-data-layer/visuals/sleek-ui-reference-board.png`: Saved generated UI reference board.
- `kriyax-data-layer/visuals/sleek-catalog-agent-reference.png`: Saved generated catalog/agent reference.
- `kriyax-data-layer/08-architecture/feature-availability-audit-v1.md`: Added feature status audit and remaining implementation plan.
- `kriyax-data-layer/00-meta/activity-log.md`: Logged the SPS build update.

**References:**
- `kriyax-data-layer/visuals/current-ui-contact-sheet.png`
- `kriyax-data-layer/visuals/sleek-ui-reference-board.png`
- `kriyax-data-layer/visuals/sleek-catalog-agent-reference.png`

### [2026-05-03 17:46:17]

**Changes:**
- Implemented the enterprise UI/runtime improvement plan across shell navigation, connector cards, catalog density, Code Workspace schema browsing, result grids, LLM playground, and Agent runtime fallback.
- Extended Python execution results with structured dataframe artifacts from `save_table()` and `show(df)`.
- Added LLM runtime status/playground endpoints and hardened Agent fallback when a configured provider request fails.
- Expanded backend and Playwright coverage for result previews, breadcrumbs, sidebar hover timing, and LLM playground privacy.

**Files Affected:**
- `kriyax-data-app/backend/app/services/execution.py`: Added bounded dataframe preview artifacts for saved and displayed results.
- `kriyax-data-app/backend/app/api/llm.py`: Added LLM runtime status and playground endpoints.
- `kriyax-data-app/backend/app/services/llm_gateway.py`: Added provider gateway, playground execution, sanitized status, and agent-safe fallback behavior.
- `kriyax-data-app/backend/app/services/agent.py`: Wired Agent generation/correction/follow-up to real LLM when available with deterministic fallback.
- `kriyax-data-app/backend/tests/test_execution.py`: Added structured result and `show(df)` preview coverage.
- `kriyax-data-app/backend/tests/test_execution_api.py`: Added API coverage for saved-table and unsaved dataframe previews.
- `kriyax-data-app/backend/tests/test_llm_api.py`: Added status/playground privacy and fallback coverage.
- `kriyax-data-app/frontend/src/api.ts`: Added result artifact, LLM status, and playground client contracts.
- `kriyax-data-app/frontend/src/App.tsx`: Rebuilt sidebar behavior, breadcrumbs, connector cards, catalog tabs, schema browser, result explorer, LLM playground, and Agent workbench.
- `kriyax-data-app/frontend/src/styles.css`: Added compact enterprise layout classes for shell, source cards, object browser, result grids, tabs, and runtime banners.
- `kriyax-data-app/frontend/e2e/code-workspace.spec.ts`: Added result-grid and sidebar hover/collapse coverage.
- `kriyax-data-app/frontend/e2e/file-import.spec.ts`: Added breadcrumb back-navigation and table detail tab coverage.
- `kriyax-data-app/frontend/e2e/pipelines.spec.ts`: Updated run-output assertion for tabbed output.
- `kriyax-data-app/frontend/e2e/storage-agent.spec.ts`: Added LLM playground privacy coverage and stabilized Agent fallback testing.
- `kriyax-data-app/README.md`: Updated live slice, coverage, and next target notes.
- `kriyax-data-layer/00-meta/activity-log.md`: Logged the completed improvement pass.

**References:**
- `kriyax-data-layer/08-architecture/enterprise-ui-runtime-improvement-plan-v1.md`

### [2026-05-03 18:48:44]

**Changes:**
- Fixed LLM playground endpoint handling so custom API URLs are used exactly instead of always appending provider paths such as `/messages`.
- Kept default OpenAI/Anthropic `/v1` behavior intact by appending the standard endpoint only for default-style `/v1` URLs.
- Updated the Storage form label to clarify the field can be an API URL or exact endpoint.

**Files Affected:**
- `kriyax-data-app/backend/app/services/llm_gateway.py`: Added provider URL resolution that preserves custom endpoints.
- `kriyax-data-app/backend/tests/test_llm_gateway.py`: Added regression coverage for custom Anthropic-compatible endpoint URLs and default Anthropic `/v1/messages`.
- `kriyax-data-app/frontend/src/App.tsx`: Updated the Storage provider URL label.
- `changelog.md`: Logged the endpoint handling fix.

**References:**
- Browser comment on `http://127.0.0.1:5173/storage` Base URL field.
