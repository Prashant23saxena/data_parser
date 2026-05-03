---
name: sps-dependency-grapher
description: Layer 8.4 of the sps app-design workflow. The fourth sub-step of L8 implementation architecture. Builds the dependency graph and identifies parallel work streams — which builds must precede which, what the critical path is, what can run concurrently. Use after L8.3 (contracts) is frozen, when sps-app-architect routes here, or when the user says "what's the build order", "show me the dependency graph", "what can be built in parallel". Produces 08-architecture/04-build-graph/v1.md plus a build dependency visual. Sets up L8.5 work packages by defining the streams they fall into.
---

# Dependency Grapher (Layer 8.4)

The fourth sub-skill of L8. Computes the build dependency graph and the parallel work streams. This is what tells the user (and their agents) "you can build A and C simultaneously after B; D blocks everything else."

## Preconditions

- L8.3 (contracts) must be `FROZEN` overall (all contracts locked).
- L8.4 status must be `PENDING`, `IN PROGRESS`, or `NEEDS_REVISION`.

## Inputs

- Project root path
- Mode: `fresh` or `revise`

## Process

### Step 1 — Memory + context

Call `sps-memory-keeper read-context`.

Read:
- L8.1 data model (entities → foundation order)
- L8.2 components (component dependency graph)
- L8.3 contracts (cross-component wires — already locked, enable parallelism)
- L4 specs (feature priorities — must/should/could)
- L7 build plan (phase definitions — Phase 1 thin slice constraints)

### Step 2 — Build the raw dependency graph

For every component in L8.2, list:
- **Hard predecessors:** components that must exist (built and tested) before this one can be built. Driven by data model dependencies and runtime dependencies that CANNOT be mocked.
- **Soft predecessors:** components that this depends on but which CAN be mocked via L8.3 contracts. These don't block the start of work, only its full completion.
- **Successors:** the inverse.

Distinguishing hard vs soft is the central skill of this layer:
- A component depends hard on the database existing — DB schema must be done first.
- A frontend depends soft on a backend — once the contract is locked, frontend can build against mocks.
- A backend service depends soft on another backend service it calls — same principle.
- A consumer of an event depends soft on the producer — mock the event.

The contracts from L8.3 transform many "would be hard" deps into soft. That's why L8.3 came first.

### Step 3 — Identify foundation layer

The set of components with no soft mockable predecessors (only hard deps on infrastructure):
- Database schema and migrations
- Auth bootstrap (often)
- Shared types library (must exist, but tiny)
- Core infrastructure (logging, error types)

This is the foundation work stream — must be built first, blocks the most.

### Step 4 — Identify parallel streams

After the foundation, identify groups of work that can proceed in parallel because:
- Each group depends only on the foundation
- Each group's external dependencies are mockable via locked contracts

Common stream patterns:
- **Stream A: Foundation** (DB, auth bootstrap, shared types)
- **Stream B: Backend domain modules** (one per major service, parallel after foundation)
- **Stream C: Frontend app shell + shared UI** (parallel with B, mocks all backends)
- **Stream D: Frontend feature modules** (after app shell, can parallel within itself)
- **Stream E: External integrations** (often parallel with anything since they're isolated)
- **Stream F: Infrastructure deployment** (CI/CD, monitoring — often parallel with everything)

The exact streams depend on the project. Propose, the user refines.

### Step 5 — Compute the critical path

The longest chain of HARD dependencies. This is the minimum time to working thin slice (assuming infinite parallel labor):

> Foundation (DB + auth) → backend core domain → frontend wired up → integration test → done

If the critical path is much longer than the user's time budget from L7, flag it as a risk. Common mitigations:
- Reduce thin-slice scope in L7
- Add hard pre-builds (e.g. use a hosted DB instead of building DB layer)
- Adopt a backend-as-a-service to skip the foundation entirely

### Step 6 — Risk assessment for the graph

Look for graph patterns that hurt parallelism:
- **Long serial chains** — if there's a chain A → B → C → D → E with no parallelism, total time = sum of all.
- **Bottleneck nodes** — components many others depend on. Building these first / well-tested is critical.
- **Late integration risk** — many parallel streams that all converge at one integration point can mask failures until late.
- **Underspecified contracts** — if any contract was rushed in L8.3, downstream parallelism breaks down.

Flag these. For each, propose mitigation.

### Step 7 — Synthesize draft

Write `08-architecture/04-build-graph/v{N}.md`:

```markdown
# Build Dependency Graph — {App Name}

**Version:** v{N}
**Status:** DRAFT
**Last updated:** {today}
**Refs:** L8.1 data model v{X}, L8.2 components v{Y}, L8.3 contracts v{Z}

## Overview

{Plain language: how many components, how many streams, what the critical path is, time-to-thin-slice estimate.}

## Foundation layer (Stream A)

These must be built first. Nothing else proceeds until these are done.

| Component | Why foundation | Estimated effort |
|---|---|---|
| db-migrations | Schema is the basis for all DB-backed components | S |
| shared-types | All components import these | S |
| auth-bootstrap | Many endpoints need auth middleware | M |

Foundation criteria: hard dependency only on infrastructure (DB engine, runtime), no mockable predecessors.

## Parallel streams (after foundation)

### Stream B: Backend domain (parallel internally where indicated)

| Component | Hard deps | Soft deps (via contracts) | Parallel with |
|---|---|---|---|
| auth-service | foundation | — | C, D |
| content-service | foundation | auth-service (via C-001) | B/auth, C, D |
| notifications-service | foundation | content-service (via C-005 event) | B/content, C, D |

### Stream C: Frontend app shell

| Component | Hard deps | Soft deps | Parallel with |
|---|---|---|---|
| frontend-app-shell | foundation/shared-types | all backends (mocked) | B, D |
| frontend-shared-ui | foundation | — | B, C, D |

### Stream D: Frontend features

| Component | Hard deps | Soft deps | Parallel with |
|---|---|---|---|
| frontend-onboarding | shared-ui, app-shell | auth-service (via C-001) | B, C/finished, other D |
| frontend-content | shared-ui, app-shell | content-service (via C-003) | other D |

### Stream E: External integrations

| Component | Hard deps | Soft deps | Notes |
|---|---|---|---|
| email-svc-integration | foundation | auth-service | parallel from start |

## Critical path

Foundation (db + shared-types + auth-bootstrap) → auth-service → frontend-onboarding wired (no longer mocked) → end-to-end signup flow integration test passes.

Estimated critical path: {duration}.

## Bottleneck components

- **shared-types** — every other component imports. Must be high-quality from the start.
- **auth-service** — many components soft-depend; can mock during build but real auth blocks final integration.

## Risks

| # | Risk | Mitigation |
|---|---|---|
| R1 | shared-types churn during build forces rebuilds across streams | Lock shared-types at v1 strictly; bump to v2 only with notice |
| R2 | Late integration of all streams may surface cross-cutting bugs | Add integration smoke test early (Stream B/auth + Stream C ready → smoke test) |
| R3 | If contract C-005 (event) is wrong, notifications-svc + content-svc both rework | Add a contract review checkpoint before B starts |

## Stream completion order (suggested)

1. Stream A (foundation) — must finish first
2. Stream B + C + D + E in parallel
3. Stream F (integration / deploy) once each piece is done

## Open questions

- {raised during graph analysis}

---

*Frozen on: {date when frozen}*
```

### Step 8 — Visual

Call `sps-visual-maker`:
- type: `build-graph` (variant of dep-graph)
- format: ask (HTML strongly recommended; ASCII OK for small projects)
- content: components grouped by stream, edges showing hard deps (solid) and soft deps (dashed)
- output_path: `visuals/08-build-graph-v{N}.{ext}`

If using ASCII, render as columns (one per stream) with arrows between.

### Step 9 — Freeze gate

Story summary:

```
=================================================
  FREEZE GATE — L8.4 Build Dependency Graph
=================================================

  ✓ Build graph locked
  
    Streams: {N} parallel streams identified
    Critical path: {duration}, {N} components in chain
    Bottlenecks: {list}
    Risks: {N} identified, {N} mitigated, {N} accepted

  → Next: L8.5 work packages — each component breaks 
    into atomic agent-claimable units of work.

=================================================
```

Ask: "Freeze L8.4 at v{N}?"

### Step 10 — On freeze

1. Save FROZEN. Update freeze-status: L8.4 → FROZEN, L8.5 → PENDING.
2. Call `sps-memory-keeper`:
   - `log-activity`
   - `record-decision` for any major streaming/sequencing decision
3. Confirm: "L8.4 frozen. Run sps-app-architect or sps-work-packager next."

## Backlog hook

Common parking at L8.4:
- Future re-streaming if team grows / contracts split
- Optimization opportunities (build-time, parallel test runs)

## Critical rules

- **Hard vs soft dependency distinction is the whole point.** Get it right.
- **Critical path must be named.** Without it, scheduling is guessing.
- **Every component lives in exactly one stream.**
- **Risks must be enumerated with mitigations** — not just listed.
- **Visual is mandatory** — this is one of the most visualizable artifacts in the whole system.
