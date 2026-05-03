---
name: sps-project-builder
description: Scaffold a new top-down app-design project with the standard 7-layer folder structure, freeze tracking, and per-layer backlogs. Use when the user says "I want to start defining a new app", "set up a new project", "scaffold a project for my app idea", "I have an app idea, help me structure it", or anything indicating the start of a fresh app-design effort. Creates the folder skeleton at a path the user provides (or default ~/projects/{name}/), initializes freeze-status.md and project-name.md, and prepares the project for the sps-app-architect orchestrator and the 7 vertical layer skills.
---

# Project Builder

A system skill that scaffolds the folder structure used by the entire top-down app-design workflow. Run this once per new app idea, before anything else.

## What it creates

```
{project-root}/
├── 00-meta/
│   ├── project-name.md
│   ├── freeze-status.md
│   ├── activity-log.md
│   ├── decisions.md
│   ├── glossary.md
│   ├── open-questions.md
│   ├── revision-flags.md
│   └── references/
│       └── index.md
├── 01-vision/
│   └── backlog.md
├── 02-pillars/
│   └── backlog.md
├── 03-features/
│   └── (pillar folders created later by sps-feature-lister)
├── 04-specs/
│   └── (feature folders created later by sps-feature-detailer)
├── 05-screens/
│   └── backlog.md
├── 06-mockups/
│   └── backlog.md
├── 07-build/
│   └── backlog.md
├── 08-architecture/
│   ├── 01-data-model/
│   │   └── backlog.md
│   ├── 02-components/
│   │   └── backlog.md
│   ├── 03-contracts/
│   │   └── (contract folders created later by sps-contract-definer)
│   ├── 04-build-graph/
│   │   └── backlog.md
│   ├── 05-work-packages/
│   │   └── (WP folders created later by sps-work-packager)
│   ├── 06-integration/
│   │   └── backlog.md
│   ├── 07-uat/
│   │   └── backlog.md
│   └── 08-agent-instructions/
│       └── backlog.md
├── visuals/
└── README.md
```

Note: `03-features/`, `04-specs/`, `08-architecture/03-contracts/`, and `08-architecture/05-work-packages/` start empty. Subfolders are created on demand by their owning skills as the user works through those layers.

## When this skill runs

User says they want to start a new app design / spec / definition project. Examples:
- "I want to start defining my new app idea"
- "Scaffold a project for my todo-app idea"
- "Set up the structure so I can begin"



## Process

### Step 1 — Gather basics

Ask the user:

1. **App name** — short, snake_case if possible, used as folder name.
2. **One-line description** — what is this app, in one sentence (just for the README; the real vision lock happens in L1 via `sps-vision-definer`).
3. **Path** — where to create the project folder. Default: `~/projects/{app-name}/`. Confirm or override.
4. **Reference docs (optional)** — "Any product docs, help centers, manuals, or competitor sites I should harvest as reference material? Paste URLs (comma-separated), file paths, or 'skip'."

If the user is vague on the name, suggest one based on the description.

If they provide reference URLs/files, note them — we'll invoke `sps-doc-harvester` after scaffolding completes (Step 8b).

### Step 2 — Verify the path

Check if the target folder already exists. If it does:
- If empty, proceed.
- If it has content, ask: "Folder exists and has content. Overwrite, choose a different path, or merge?" Default to choosing a different path.

### Step 3 — Create the structure

Use bash to create the folder tree. Then write the files described below.

### Step 4 — Write `00-meta/project-name.md`

```markdown
# {App Name}

> {one-line description}

**Created:** {today's date}
**Path:** {project root path}

This project follows the top-down app-design workflow:
1. Vision (frozen first)
2. Pillars (4-7 high-level capability areas)
3. Features (per pillar)
4. Specs (per feature: states, edge cases)
5. Screens (sitemap + navigation)
6. Mockups (visual screens)
7. Build plan

Use the `sps-app-architect` skill to navigate this project. It reads `freeze-status.md` and routes you to the correct next step.
```

### Step 5 — Write `00-meta/freeze-status.md`

This is the live tracker. Initialize with everything pending:

```markdown
# Freeze Status

> Single source of truth for project progress. Updated by every vertical layer skill on freeze.
> The sps-app-architect skill reads this to decide what to run next.

**Last updated:** {today's date}

## Layers

| Layer | Skill | Status | Version | Notes |
|---|---|---|---|---|
| L1 Vision | sps-vision-definer | PENDING | — | |
| L2 Pillars | sps-pillar-mapper | BLOCKED | — | waiting on L1 |
| L3 Features | sps-feature-lister | BLOCKED | — | waiting on L2; loops per pillar |
| L4 Specs | sps-feature-detailer | BLOCKED | — | waiting on L3; loops per feature |
| L5 Screens | sps-screen-planner | BLOCKED | — | waiting on L4 |
| L6 Mockups | sps-mockup-painter | BLOCKED | — | waiting on L5; loops per screen |
| L7 Build | sps-build-planner | BLOCKED | — | waiting on L6 |
| L8 Architecture | (sub-pipeline below) | BLOCKED | — | waiting on L7 |
| L8.1 Data model | sps-data-modeler | BLOCKED | — | waiting on L7 |
| L8.2 Components | sps-component-mapper | BLOCKED | — | waiting on L8.1 |
| L8.3 Contracts | sps-contract-definer | BLOCKED | — | waiting on L8.2; per-contract freeze |
| L8.4 Build graph | sps-dependency-grapher | BLOCKED | — | waiting on L8.3 |
| L8.5 Work packages | sps-work-packager | BLOCKED | — | waiting on L8.4 |
| L8.6 Integration | sps-integration-mapper | BLOCKED | — | waiting on L8.5 |
| L8.7 UAT | sps-uat-scripter | BLOCKED | — | waiting on L8.6 |
| L8.8 Agent briefer | sps-agent-briefer | BLOCKED | — | waiting on L8.7; FINAL design step |

## Loop progress

### L3 Features (per pillar)
<!-- populated when L2 freezes; one row per pillar -->
| Pillar | Status | Version |
|---|---|---|

### L4 Specs (per feature)
<!-- populated as L3 pillars freeze; one row per feature -->
| Pillar | Feature | Status | Version |
|---|---|---|---|

### L6 Mockups (per screen)
<!-- populated when L5 freezes; one row per screen -->
| Screen | Status | Version |
|---|---|---|

## Status legend

- **PENDING** — ready to run, not started
- **BLOCKED** — waiting on a previous layer/loop iteration
- **IN PROGRESS** — interview started, not yet frozen
- **FROZEN** — locked at current version; downstream may proceed
- **NEEDS_REVISION** — flagged by a later layer; needs an updated version
```

### Step 6 — Create empty backlog files

For each of: `01-vision/backlog.md`, `02-pillars/backlog.md`, `05-screens/backlog.md`, `06-mockups/backlog.md`, `07-build/backlog.md`, `08-architecture/01-data-model/backlog.md`, `08-architecture/02-components/backlog.md`, `08-architecture/04-build-graph/backlog.md`, `08-architecture/06-integration/backlog.md`, `08-architecture/07-uat/backlog.md`, `08-architecture/08-agent-instructions/backlog.md`, write the standard backlog template (see `sps-idea-parker` skill for the template format).

Do NOT pre-create backlog files in `03-features/`, `04-specs/`, `08-architecture/03-contracts/`, or `08-architecture/05-work-packages/` — those happen lazily as pillars/features/contracts/WPs are defined.

### Step 6b — Initialize 00-meta memory files

Write empty templates for the shared memory files (full templates in `sps-memory-keeper` skill):

- `00-meta/activity-log.md` — append-only log header
- `00-meta/decisions.md` — decisions log header
- `00-meta/glossary.md` — glossary header
- `00-meta/open-questions.md` — open questions registry header
- `00-meta/revision-flags.md` — revision flags header
- `00-meta/references/index.md` — references index header (empty table)

Do NOT create `agent-claims.md` — that's created when L8 freezes and build phase starts.

### Step 7 — Write `README.md` at project root

```markdown
# {App Name}

> {one-line description}

This is a top-down app design project. Folder structure is intentional — each layer locks before the next begins.

## Quick start

Run the **sps-app-architect** skill at any time:
- "Continue working on {app-name}"
- "Where am I in the {app-name} project?"

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
```

### Step 8 — Confirm to user

Show:
- The full folder structure created (use `find` or `tree`).
- The path to the project.
- The next step: "Now run the **sps-app-architect** skill, or directly run **sps-vision-definer** to begin Layer 1."

### Step 8b — Harvest references if provided

If the user provided reference URLs/files in Step 1:

For each reference, invoke `sps-doc-harvester`:
- source_type: url / pdf / text (detect)
- source: the URL or path
- mode: `feature-inventory` (good default, not too deep)
- slug: derive from URL/filename

Tell the user: "Harvesting {N} references now. Each will save to `00-meta/references/{slug}.md` and inform every layer's research."

After harvesting completes, list the references that were saved.

If harvesting fails for any (network/auth), report the failure and continue — the project is still scaffolded successfully.

## Critical rules

- **Never overwrite an existing project** without explicit permission.
- **Always create all the folders even if empty** — the structure is the contract.
- **Do not run any vertical layer skill from inside this skill** — this skill only scaffolds. The user (or sps-app-architect) decides when to start L1.
- **Use snake_case or kebab-case for the app folder name** — no spaces.

## Default path behavior

- Default base: `~/projects/`
- Default folder name: derived from app name, lowercased, spaces → hyphens.
- User can always override.
- If `~/projects/` doesn't exist, create it.
