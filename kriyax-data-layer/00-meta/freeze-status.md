# Freeze Status

> Single source of truth for project progress. Updated by every vertical layer skill on freeze.
> The sps-app-architect skill reads this to decide what to run next.

**Last updated:** 2026-05-03

## Layers

| Layer | Skill | Status | Version | Notes |
|---|---|---|---|---|
| L1 Vision | sps-vision-definer | FROZEN | v2 | frozen 2026-05-02; revised to Python-only direction |
| L2 Pillars | sps-pillar-mapper | FROZEN | v2 | frozen 2026-05-02; Code Workspace and Agentic Layer revised to Python-only |
| L3 Features | sps-feature-lister | FROZEN | v4 | frozen 2026-05-02; all 6 pillars reviewed, 36 features total |
| L4 Specs | sps-feature-detailer | FROZEN | mixed | all 36 feature specs frozen with tests; F-DC-002/F-DC-003 revised to v3 |
| L5 Screens | sps-screen-planner | FROZEN | v1 | 14 screens frozen; L6 mockups seeded |
| L6 Mockups | sps-mockup-painter | FROZEN | v2 | all 14 detailed low-fidelity mockups approved and frozen |
| L7 Build | sps-build-planner | FROZEN | v1 | frozen 2026-05-02; implementation may begin from L8/build contract |
| L8.1 Data Model | sps-data-modeler | FROZEN | v1 | frozen 2026-05-03; grounded in existing kriyax-data-app build slices |
| L8.2 Components | sps-component-mapper | FROZEN | v1 | frozen 2026-05-03; maps existing app modules and remaining feature ownership |
| L8.3 Contracts | sps-contract-definer | FROZEN | v1 | frozen 2026-05-03; all 8 contracts locked |
| L8.4 Dependencies | sps-dependency-grapher | FROZEN | v1 | frozen 2026-05-03; maps remaining streams from current build baseline |
| L8.5 Work Packages | sps-work-packager | FROZEN | v1 | 11 remaining-work packages across 6 streams |
| L8.6 Integration Tests | sps-integration-mapper | FROZEN | v1 | 8 scenarios cover all frozen contracts |
| L8.7 UAT Scripts | sps-uat-scripter | FROZEN | v1 | 7 critical UATs plus 3 edge/non-functional checks |
| L8.8 Agent Brief | sps-agent-briefer | FROZEN | v1 | final design step frozen; agent instructions and checklist generated |

## Loop progress

### L3 Features (per pillar)
<!-- populated when L2 freezes; one row per pillar -->
| Pillar | Status | Version |
|---|---|---|
| pillar-01-data-connectors | FROZEN | v3 |
| pillar-02-schema-catalog | FROZEN | v3 |
| pillar-03-code-workspace | FROZEN | v2 |
| pillar-04-agentic-layer | FROZEN | v2 |
| pillar-05-pipeline-scheduling | FROZEN | v2 |
| pillar-06-data-storage | FROZEN | v1 |

### L4 Specs (per feature)
<!-- populated as L3 pillars freeze; one row per feature -->
| Pillar | Feature | Status | Version |
|---|---|---|---|
| data-connectors | F-DC-001 Upload CSV/Excel | FROZEN | v1 |
| data-connectors | F-DC-002 Auto-detect columns | FROZEN | v3 |
| data-connectors | F-DC-003 Preview before import | FROZEN | v3 |
| data-connectors | F-DC-004 Configure Odoo connection | FROZEN | v2 |
| data-connectors | F-DC-005 Browse Odoo models | FROZEN | v2 |
| data-connectors | F-DC-006 Fetch Odoo records | FROZEN | v2 |
| data-connectors | F-DC-007 Incremental/delta sync | FROZEN | v2 |
| data-connectors | F-DC-008 Manage saved connections | FROZEN | v2 |
| schema-catalog | F-SC-001 Table registry | FROZEN | v1 |
| schema-catalog | F-SC-002 Column metadata viewer | FROZEN | v2 |
| schema-catalog | F-SC-003 Auto-register on ingest | FROZEN | v2 |
| schema-catalog | F-SC-004 Browse & search catalog | FROZEN | v2 |
| schema-catalog | F-SC-005 Preview table rows | FROZEN | v1 |
| code-workspace | F-CW-001 Python code editor | FROZEN | v2 |
| code-workspace | F-CW-002 Show available tables | FROZEN | v2 |
| code-workspace | F-CW-003 Load tables as DataFrames | FROZEN | v2 |
| code-workspace | F-CW-004 Save DataFrame as table | FROZEN | v1 |
| code-workspace | F-CW-005 View execution output | FROZEN | v1 |
| code-workspace | F-CW-006 Save & re-run scripts | FROZEN | v1 |
| agentic-layer | F-AL-001 Chat interface | FROZEN | v1 |
| agentic-layer | F-AL-002 Schema-aware context | FROZEN | v1 |
| agentic-layer | F-AL-003 Generate Python code | FROZEN | v1 |
| agentic-layer | F-AL-004 Insert code into editor | FROZEN | v1 |
| agentic-layer | F-AL-005 Self-correction on error | FROZEN | v1 |
| agentic-layer | F-AL-006 Conversational follow-ups | FROZEN | v1 |
| pipeline-scheduling | F-PS-001 Create pipeline | FROZEN | v1 |
| pipeline-scheduling | F-PS-002 Schedule pipeline | FROZEN | v1 |
| pipeline-scheduling | F-PS-003 Manual trigger | FROZEN | v1 |
| pipeline-scheduling | F-PS-004 Run history & status | FROZEN | v1 |
| pipeline-scheduling | F-PS-005 Error notifications | FROZEN | v1 |
| pipeline-scheduling | F-PS-006 Enable/disable pipeline | FROZEN | v1 |
| data-storage | F-DS-001 Backing database setup | FROZEN | v1 |
| data-storage | F-DS-002 Auto-create tables on import | FROZEN | v1 |
| data-storage | F-DS-003 Persist derived tables | FROZEN | v1 |
| data-storage | F-DS-004 Basic table management | FROZEN | v1 |
| data-storage | F-DS-005 Export table data | FROZEN | v1 |

### L6 Mockups (per screen)
<!-- populated when L5 freezes; one row per screen -->
| Screen | Status | Version |
|---|---|---|
| S-01-home | FROZEN | v2 |
| S-02-connectors | FROZEN | v2 |
| S-03-file-import-wizard | FROZEN | v2 |
| S-04-odoo-import-workspace | FROZEN | v2 |
| S-05-catalog | FROZEN | v2 |
| S-06-table-detail | FROZEN | v2 |
| S-07-table-management-confirmation | FROZEN | v2 |
| S-08-export-table-modal | FROZEN | v2 |
| S-09-code-workspace | FROZEN | v2 |
| S-10-agent-panel | FROZEN | v2 |
| S-11-saved-scripts | FROZEN | v2 |
| S-12-pipelines | FROZEN | v2 |
| S-13-pipeline-run-detail | FROZEN | v2 |
| S-14-storage-settings | FROZEN | v2 |

## Status legend

- **PENDING** — ready to run, not started
- **BLOCKED** — waiting on a previous layer/loop iteration
- **IN PROGRESS** — interview started, not yet frozen
- **FROZEN** — locked at current version; downstream may proceed
- **NEEDS_REVISION** — flagged by a later layer; needs an updated version
