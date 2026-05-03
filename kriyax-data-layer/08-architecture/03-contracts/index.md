# Contracts Index

**Status:** FROZEN
**Last updated:** 2026-05-03
**Refs:** L8.1 data model v1, L8.2 components v1

L8.3 contracts freeze independently. L8.3 overall can freeze only after every contract below is frozen.

| Contract | Name | Type | Producer | Consumers | Status | Version |
|---|---|---|---|---|---|---|
| C-001 | Shared Types | shared-type | shared-contract-types | all frontend and backend modules | FROZEN | v1 |
| C-002 | Storage API | http-api | backend-storage-service via backend-api-routers | frontend-storage-settings, frontend-catalog | FROZEN | v1 |
| C-003 | Catalog API | http-api | backend-catalog-service via backend-api-routers | frontend-catalog, frontend-code-workspace, frontend-agent-panel | FROZEN | v1 |
| C-004 | Imports API | http-api | backend-imports-service via backend-api-routers | frontend-connectors | FROZEN | v1 |
| C-005 | Execution API | http-api | backend-execution-service via backend-api-routers | frontend-code-workspace, frontend-pipelines, frontend-agent-panel | FROZEN | v1 |
| C-006 | Odoo API | http-api | backend-odoo-service via backend-api-routers | frontend-connectors, frontend-pipelines | FROZEN | v1 |
| C-007 | Pipelines API | http-api | backend-pipelines-service via backend-api-routers | frontend-pipelines, frontend-app-shell | FROZEN | v1 |
| C-008 | Agent API | http-api | backend-agent-service via backend-api-routers | frontend-agent-panel, frontend-code-workspace | FROZEN | v1 |

## Drafting Notes

- Existing implemented APIs are preserved where they already work.
- Remaining endpoints are marked as target additions inside each contract.
- Standard error shape comes from C-001.
- Mocks are mandatory so frontend and backend work can proceed independently.
