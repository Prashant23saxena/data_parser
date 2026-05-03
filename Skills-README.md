# sps Top-Down App Designer — Skill Suite

A set of **22 skills** that walk you through defining and pre-architecting an app idea in a strict, freeze-gated, top-down order. Built for solo developers who know the failure mode: starting to build before fully defining, then realizing things are missing.

The output is a complete spec + implementation architecture that an autonomous coding agent (or you) can execute against — work-package by work-package, with tests at every layer.

## The 22 skills

### Horizontal utilities (5) — callable by anyone, any time
1. **sps-idea-parker** — park stray ideas into the right per-layer backlog
2. **sps-visual-maker** — generate ASCII / HTML / image visuals on demand
3. **sps-doc-harvester** — ingest external product docs / manuals / notes as reference material
4. **sps-test-writer** — convert a frozen feature spec into actionable test scenarios
5. **sps-memory-keeper** — read/write shared project memory (decisions, glossary, open questions, activity log, agent claims)

### System (2)
6. **sps-project-builder** — scaffold a new project's folder structure (run once per app)
7. **sps-app-architect** — master orchestrator; reads progress, routes to the next correct skill

### Vertical layer skills (7) — the design layers
8. **sps-vision-definer** (L1) — purpose, user, promise, non-goals
9. **sps-pillar-mapper** (L2) — 4-7 high-level capability areas
10. **sps-feature-lister** (L3) — features per pillar (loops per pillar)
11. **sps-feature-detailer** (L4) — states & edge cases per feature (loops per feature; auto-invokes sps-test-writer)
12. **sps-screen-planner** (L5) — sitemap, screens, navigation
13. **sps-mockup-painter** (L6) — visual mockups per screen (loops per screen)
14. **sps-build-planner** (L7) — tech stack, phases, risks, thin slice

### L8 sub-pipeline (8) — implementation architecture
15. **sps-data-modeler** (L8.1) — entities, relationships, source of truth
16. **sps-component-mapper** (L8.2) — components/services/modules
17. **sps-contract-definer** (L8.3) — APIs, events, shared types (per-contract freeze; enables parallel builds)
18. **sps-dependency-grapher** (L8.4) — build graph + parallel work streams + critical path
19. **sps-work-packager** (L8.5) — atomic agent-claimable work packages
20. **sps-integration-mapper** (L8.6) — cross-component integration tests
21. **sps-uat-scripter** (L8.7) — end-to-end user acceptance tests
22. **sps-agent-briefer** (L8.8) — final agent-instructions.md + live build checklist

## How it flows

```
sps-project-builder
      ↓
sps-app-architect  ←──────────────────────────────────┐
      ↓                                               │
sps-vision-definer (L1) ── freeze ────────────────────┤
      ↓                                               │
sps-pillar-mapper (L2) ── freeze ─────────────────────┤
      ↓                                               │
sps-feature-lister (L3) ── per pillar ────────────────┤
      ↓                                               │
sps-feature-detailer (L4) ── per feature ─────────────┤  HORIZONTAL UTILITIES
   + sps-test-writer (auto, per feature)              │  (called throughout)
      ↓                                               │
sps-screen-planner (L5) ── freeze ────────────────────┤  • sps-idea-parker
      ↓                                               │  • sps-visual-maker
sps-mockup-painter (L6) ── per screen ────────────────┤  • sps-doc-harvester
      ↓                                               │  • sps-test-writer
sps-build-planner (L7) ── freeze ─────────────────────┤  • sps-memory-keeper
      ↓                                               │
sps-data-modeler (L8.1) ── freeze ────────────────────┤
      ↓                                               │
sps-component-mapper (L8.2) ── freeze ────────────────┤
      ↓                                               │
sps-contract-definer (L8.3) ── per-contract freeze ───┤
      ↓                                               │
sps-dependency-grapher (L8.4) ── freeze ──────────────┤
      ↓                                               │
sps-work-packager (L8.5) ── freeze ───────────────────┤
      ↓                                               │
sps-integration-mapper (L8.6) ── freeze ──────────────┤
      ↓                                               │
sps-uat-scripter (L8.7) ── freeze ────────────────────┤
      ↓                                               │
sps-agent-briefer (L8.8) ── FINAL freeze ─────────────┘
      ↓
  ALL 8 LAYERS FROZEN — agents can begin building
```

## Project structure created by sps-project-builder

```
{project-root}/
├── 00-meta/                         ← shared memory
│   ├── project-name.md
│   ├── freeze-status.md             ← single source of truth for progress
│   ├── activity-log.md              ← timeline
│   ├── decisions.md                 ← decisions log
│   ├── glossary.md                  ← project vocabulary
│   ├── open-questions.md            ← unresolved questions
│   ├── revision-flags.md            ← cascade tracking
│   └── references/                  ← from sps-doc-harvester
│       ├── index.md
│       └── {source}.md
├── 01-vision/                       (versioned spec + backlog)
├── 02-pillars/                      (versioned spec + backlog)
├── 03-features/
│   └── pillar-XX-{name}/            (versioned spec + backlog, per pillar)
├── 04-specs/
│   └── pillar-XX-{name}/
│       └── feature-YYY-{name}/      (vN.md + vN-tests.md siblings)
├── 05-screens/
├── 06-mockups/
│   └── {screen-id}/
├── 07-build/
├── 08-architecture/
│   ├── 01-data-model/
│   ├── 02-components/
│   ├── 03-contracts/
│   │   └── C-NNN-{slug}/            (one folder per contract — per-contract freeze)
│   ├── 04-build-graph/
│   ├── 05-work-packages/
│   │   └── WP-{ID}-{slug}/          (one folder per WP — agent-claimable)
│   ├── 06-integration/
│   ├── 07-uat/
│   ├── 08-agent-instructions/
│   ├── agent-instructions.md        ← root-level for easy agent access
│   └── checklist.md                 ← live build checklist (mutable)
├── visuals/                         ← all generated visuals
└── README.md
```

## Key design decisions

- **Versioned folders.** Every layer keeps `v1.md`, `v2.md`, ... + `current.md`.
- **Per-layer backlogs.** Stray ideas live next to the spec they relate to.
- **Freeze gates.** A layer cannot proceed until the previous is FROZEN.
- **Loop tracking.** L3 (per pillar), L4 (per feature), L6 (per screen), L8.3 (per contract), L8.5 (WP-level status).
- **Domain research per layer.** Each vertical reads `00-meta/references/*.md` (if harvested) and supplements with web search.
- **Visuals at every layer.** ASCII default, HTML / image when fidelity matters.
- **Revision cascades.** Later layers can flag earlier ones as `NEEDS_REVISION`.
- **Tests are first-class.** L4 specs and tests freeze together. L8 has integration tests + UAT. Test invocation is in every WP.
- **Agent-shaped work packages.** Atomic, self-contained, claimable via append-only log.
- **Shared memory.** Decisions, glossary, OQs, activity log persist across the whole project — every skill uses sps-memory-keeper.
- **Parallel-first L8.** Contracts freeze independently to unblock parallel build streams.

## Quick start

1. Install the skills.
2. "Use **sps-project-builder** to scaffold a project for my app idea: ..."
3. "Run **sps-app-architect**."
4. Follow the routing through L1 → L8.8.
5. Hand `08-architecture/agent-instructions.md` to your build agent(s).

## Reusable

Domain-agnostic. Run for any new app idea.
