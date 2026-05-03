# KriyaX Data Layer

> A Databricks-like data platform for KriyaX — connectors to third-party tools, data upload, schema management, and data cleaning pipelines.

This is a top-down app design project. Folder structure is intentional — each layer locks before the next begins.

## Quick start

Run the **sps-app-architect** skill at any time:
- "Continue working on kriyax-data-layer"
- "Where am I in the kriyax-data-layer project?"

It reads `00-meta/freeze-status.md` and routes you to the correct skill.

## Layer guide

| # | Folder | Skill | What it produces |
|---|---|---|---|
| 1 | `01-vision/` | sps-vision-definer | Purpose, user, promise, non-goals |
| 2 | `02-pillars/` | sps-pillar-mapper | 4-7 high-level capability areas |
| 3 | `03-features/{pillar}/` | sps-feature-lister | Features per pillar (loops) |
| 4 | `04-specs/{pillar}/{feature}/` | sps-feature-detailer | States, edge cases (loops) |
| 5 | `05-screens/` | sps-screen-planner | Sitemap and navigation |
| 6 | `06-mockups/` | sps-mockup-painter | Visual mockups (loops) |
| 7 | `07-build/` | sps-build-planner | Build plan and sequencing |

Plus horizontal utilities: `sps-idea-parker` (parking ideas in backlogs) and `sps-visual-maker` (generating visuals).

## Versioning

Each layer keeps every version: `v1.md`, `v2.md`, ... and a `current.md` pointing to the active one. History is preserved.

## Backlogs

Every layer has its own `backlog.md`. Items parked during brainstorming go there. They can be promoted into the active version later.
