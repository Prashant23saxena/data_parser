---
name: sps-component-mapper
description: Layer 8.2 of the sps app-design workflow. The second sub-step of L8 implementation architecture. Groups features and entities into components/services/modules — frontend components, backend services, shared libraries, infrastructure. Defines what each component owns, depends on, and exposes. Use after L8.1 (data model) is frozen, when sps-app-architect routes here, or when the user says "define the components", "what services do I need", "map features to modules". Produces 08-architecture/02-components/v1.md and a component diagram. Sets up L8.3 contracts (which define the wires between components).
---

# Component Mapper (Layer 8.2)

The second sub-skill of L8. Groups the spec into named components — the boxes in the architecture diagram. Each component owns specific entities and features, depends on specific others, and exposes a specific interface (which L8.3 will lock down as contracts).

## Preconditions

- L8.1 (data model) must be `FROZEN`.
- L8.2 status must be `PENDING`, `IN PROGRESS`, or `NEEDS_REVISION`.

## Inputs

- Project root path
- Mode: `fresh` or `revise`

## Process

### Step 1 — Memory + context

Call `sps-memory-keeper read-context` with caller=`sps-component-mapper`.

Read:
- L1 vision (constraints)
- L2 pillars (mental groupings — often align with components but not always)
- L3 features (by pillar)
- L5 screens (frontend component shape)
- L7 build plan (tech stack — informs frontend framework, backend framework)
- L8.1 data model (entities — must be allocated to components)
- `00-meta/references/*.md` if present (competitor architectures)

Greet:

> "Starting L8.2 component architecture. I'll group your {N} features and {M} entities into components. Tech stack: {frontend} + {backend}. This sets up the contract definition in L8.3."

### Step 2 — Domain research

3-5 searches:
- "Component architecture for {framework}"
- "Folder structure {framework}"
- "{app type} backend service decomposition"
- "Microservices vs modular monolith for solo dev" (if relevant given L7 context)

### Step 3 — Initial decomposition (you propose, user refines)

Propose component groups based on patterns. Common starting decomposition:

**Frontend:**
- One component group per pillar (often)
- Plus shared UI components (buttons, forms, modals — extracted from L5/L6)
- Plus app-shell (routing, layout, providers)

**Backend:**
- One module per pillar (often) OR
- Domain-driven modules (auth, content, billing, notifications) cutting across pillars

**Shared:**
- Type definitions / data shapes (used by both ends)
- Utilities (date handling, validation, etc.)

**Infrastructure:**
- Database
- Auth provider (if external)
- Email / notification service
- Storage (if any)
- Cache / queue (if any)

Show the user this draft and explicitly note: "Pillars from L2 don't always equal components. Sometimes a pillar splits (Discovery → Search + Recommendations + Browse). Sometimes pillars share infrastructure."

### Step 4 — Refine each component (interview)

For each proposed component:

**4a. Name and scope.** Confirm name. One-sentence description.

**4b. What it owns.**
- Which entities (from L8.1)
- Which features (from L3)
- Which screens (from L5, for frontend components)

**4c. What it depends on.** Other components that must exist for this to work. Distinguish:
- **Hard dependency** — calls into the other component's interface
- **Shared dependency** — both consume a third (e.g. both use auth)

**4d. What it exposes.** The interface other components see. Examples:
- HTTP API endpoints (for backend services)
- Exported React components/hooks (for shared frontend libs)
- Events emitted (for event-driven components)
- DB schema (for data layers — but usually internal)

**4e. Boundaries / non-goals.** What this component does NOT do. Prevents scope creep.

### Step 5 — Cross-cutting concerns at component level

- **Auth:** dedicated component, or middleware threaded through?
- **Logging / observability:** one component or shared lib?
- **Error handling:** centralized or per-component?
- **Configuration:** one source (env vars / config service) or scattered?
- **Validation:** server-side, client-side, or shared?

For each, decide and call `sps-memory-keeper record-decision`.

### Step 6 — Coverage and conflict checks

**Coverage:**
- Every entity from L8.1 must be owned by exactly one component (or explicitly shared with rule).
- Every feature from L3 must be implemented by at least one component.
- Every screen from L5 must be rendered by at least one frontend component.

If gaps: either expand a component or add a new one.

**Conflicts:**
- Two components both claiming the same entity → resolve, maybe split.
- Circular dependencies → break by extracting a third component or inverting one direction.

Push back hard on circular deps. They're the source of most "I can't build this in parallel" pain.

### Step 7 — Synthesize draft

Write `08-architecture/02-components/v{N}.md`:

```markdown
# Components — {App Name}

**Version:** v{N}
**Status:** DRAFT
**Last updated:** {today}
**Refs:** L8.1 data model v{X}, L7 build plan v{Y}

## Overview

{Plain language: how many components, the major split (e.g. "frontend SPA + backend modular monolith + 2 external services"), notable patterns.}

## Component map

| Component | Type | Owns entities | Implements features | Depends on |
|---|---|---|---|---|
| auth-service | backend module | User, Session | F-ON-001..004 | DB |
| content-service | backend module | Task, Tag | F-CO-* | DB, auth-service |
| frontend-app-shell | frontend | — | navigation only | — |
| frontend-onboarding | frontend feature | — | F-ON-* (UI) | app-shell, contracts |
| frontend-content | frontend feature | — | F-CO-* (UI) | app-shell, contracts |
| shared-types | shared lib | — | — | — |
| db | infrastructure | (all entities) | — | — |
| email-svc | external | — | — | (used by auth-service) |

## Components

### auth-service (backend module)

**Purpose:** authenticate users; manage sessions.

**Owns entities:** User, Session, AuditEvent (login subset)

**Implements features:** F-ON-001 (signup), F-ON-002 (login), F-ON-003 (forgot password), F-ON-004 (logout)

**Exposes (preliminary — locked in L8.3):**
- HTTP API: POST /auth/signup, POST /auth/login, POST /auth/refresh, DELETE /auth/session
- Middleware: requireAuth(req)

**Depends on:** db (Postgres), email-svc (for verification)

**Boundaries:** does NOT manage user profile data beyond email/auth (that's profile-service if/when added).

**Internal structure:**
- handlers/ — HTTP entry points
- services/ — business logic
- repos/ — DB access for User and Session

### content-service (backend module)
...

### frontend-onboarding (frontend feature module)
...

(continue for each)

## Cross-cutting components

### Logging
Shared library `lib/log` used by all backend components. Centralized config.

### Error handling
Shared error types in `shared-types`. Each backend component maps its errors to standard codes.

### Validation
Shared validators in `shared-types`. Used by frontend (immediate feedback) and backend (server-of-record).

## Dependency rules

- Frontend components NEVER call DB directly — only through backend service contracts.
- Backend components NEVER reach into another backend component's DB tables — only through contracts.
- Shared libs have no runtime dependencies on services.

## Open questions

- {OQs raised}

---

*Frozen on: {date when frozen}*
```

### Step 8 — Visual

Call `sps-visual-maker`:
- type: `dep-graph` variant for components
- format: ask (HTML recommended for >6 components)
- content: components as nodes, dependency arrows
- output_path: `visuals/08-components-v{N}.{ext}`

### Step 9 — Freeze gate

Story summary:

```
=================================================
  FREEZE GATE — L8.2 Components
=================================================

  ✓ Component architecture locked
  
    Components: {N} ({F} frontend, {B} backend, {S} shared, {I} infra)
    Every entity owned: ✓
    Every feature mapped: ✓
    No circular deps: ✓ / ✗ ({if any, list})

  → Next: L8.3, define contracts (the wires between components — 
    these enable parallel builds)

=================================================
```

Ask: "Freeze L8.2 at v{N}?"

### Step 10 — On freeze

1. Write FROZEN status. Update current.md.
2. Update freeze-status.md: L8.2 → FROZEN, L8.3 → PENDING.
3. Call `sps-memory-keeper`:
   - `log-activity`
   - `record-decision` for major component-level choices
4. Confirm: "L8.2 frozen. Run sps-app-architect or sps-contract-definer to start L8.3."

## Backlog hook

Common parking moments at L8.2:
- Future component splits ("we should split content-service when it grows")
- Performance components for v2 (caching layer, search indexer)
- Optional infrastructure (CDN, monitoring add-ons)

## Revision cascade

Revising L8.2 invalidates L8.3 (contracts depend on component boundaries) and downstream. Cascade as `NEEDS_REVISION`.

## Critical rules

- **No circular dependencies.** Hard rule. If you find one, break it.
- **Every entity owned by exactly one component.** Sharing is allowed only with explicit, documented rules.
- **Boundaries are explicit.** "Does not do X" is part of the spec.
- **Pillars ≠ components automatically.** Justify the mapping.
- **Visual is mandatory.**
