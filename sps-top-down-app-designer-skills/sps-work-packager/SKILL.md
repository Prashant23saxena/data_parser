---
name: sps-work-packager
description: Layer 8.5 of the sps app-design workflow. The fifth sub-step of L8. Decomposes each component from L8.2 into atomic, agent-claimable work packages — small enough to finish in one session, with explicit inputs, outputs, dependencies, mocks, build steps, test invocation, and acceptance criteria. Each WP is a checkbox in the implementation checklist. Use after L8.4 (dependency graph) is frozen, when sps-app-architect routes here, or when the user says "create the work packages", "break this into agent-sized tasks", "generate the build checklist". Each WP becomes its own file under 08-architecture/05-work-packages/.
---

# Work Packager (Layer 8.5)

The fifth sub-skill of L8. Converts components and streams into atomic work packages an agent can claim and execute. **This is what an autonomous coding agent will actually pick up and build from.**

Every WP is small enough to finish in one session, fully self-contained (an agent can execute without reading the whole architecture doc), and explicit about its mocks and tests.

## Preconditions

- L8.4 (dependency graph) must be `FROZEN`.
- L8.5 status must be `PENDING`, `IN PROGRESS`, or `NEEDS_REVISION`.

## Inputs

- Project root path
- Mode: `fresh` or `revise`

## Process

### Step 1 — Memory + context

Call `sps-memory-keeper read-context`.

Read everything frozen, especially:
- L8.2 components (each will decompose into multiple WPs)
- L8.3 contracts (WPs reference these for inputs)
- L8.4 build graph (WPs inherit stream membership)
- L4 specs + tests (WPs that build features reference both)

### Step 2 — Decomposition strategy

For each component from L8.2, decompose into WPs. Sizing rules:

- **One WP = one session of focused work.** Roughly 2–8 hours for a human; less for an agent.
- **Each WP delivers something testable.** Even if intermediate.
- **Each WP has clear acceptance.** Done is binary.

Common decomposition patterns:

**For a backend service component:**
- WP-X01: scaffold + project setup + first migration
- WP-X02: data models + repos for owned entities
- WP-X03: business logic services (one WP per major flow)
- WP-X04: HTTP handlers / API routes per contract
- WP-X05: error handling + middleware
- WP-X06: integration tests against fixtures
- WP-X07: deploy config + smoke test

**For a frontend component:**
- WP-Y01: scaffold + routing
- WP-Y02: shared UI components needed
- WP-Y03: each screen (one WP per screen, or grouped if small)
- WP-Y04: state management wiring
- WP-Y05: API client (using mocked contracts initially, swap to real later)
- WP-Y06: e2e tests for critical flows

**For a foundation component:**
- One WP per logical unit (e.g. WP-A01 db-schema, WP-A02 migration runner, WP-A03 shared-types package).

WP IDs follow stream prefix: `WP-A01`, `WP-A02` for stream A; `WP-B01` for stream B; etc.

### Step 3 — For each WP, fill the template

This is the heart of the skill. Every WP gets a complete, agent-readable spec.

```markdown
# Work Package: WP-{ID}

**Title:** {short title}
**Version:** v1
**Status:** PENDING (becomes CLAIMED, IN_PROGRESS, BLOCKED, DONE during build)
**Stream:** {A/B/C/...}
**Component:** {component from L8.2}
**Estimated effort:** S (≤2hr) / M (2-8hr) / L (full day, consider splitting)

## What this WP delivers

One paragraph in plain language. What will exist after this WP is done that didn't before.

## Why this WP exists

Which features (L3) and contracts (L8.3) it implements / supports.

## Inputs

What an agent needs before starting. Pointers (paths), not copies.

- L4 spec for feature {ID}: `04-specs/{pillar}/{feature}/current.md`
- Test scenarios: `04-specs/{pillar}/{feature}/current-tests.md`
- Contract C-{NNN}: `08-architecture/03-contracts/C-{NNN}-{slug}/current.md`
- Data model entity X: `08-architecture/01-data-model/current.md` (relevant section)

## Hard dependencies

WPs that must be `DONE` before this can start.

- WP-A01 (db schema)
- WP-A03 (shared types v1)

## Soft dependencies (can mock)

WPs that this would normally call but which can be mocked via contracts.

- WP-B02 (auth-service) — mock per Contract C-001's mock spec until B02 is done.

## Build steps

Concrete steps, in order. An agent should be able to execute these.

1. Create folder `services/auth/` and scaffold {framework} project.
2. Add dependencies: {list}.
3. Implement repository layer for User entity per data model.
4. Implement signup handler per Contract C-001 / signup endpoint.
5. Implement login handler per Contract C-001 / login endpoint.
6. Wire up middleware for requireAuth.
7. Add unit tests for each handler.
8. Run unit tests, ensure all pass.
9. Add this WP's component to the dev compose / deploy config.
10. Hand off to integration test stream.

## Outputs

What will physically exist after this WP. Helps the next agent.

Files / folders:
- `services/auth/`
- `services/auth/src/handlers/signup.ts`
- `services/auth/src/handlers/login.ts`
- `services/auth/src/middleware/require-auth.ts`
- `services/auth/tests/unit/*`

Capabilities:
- Local server running on port {N}, exposes endpoints per C-001.
- All unit tests pass.

## Test invocation

Exact commands to verify this WP is done.

```bash
cd services/auth
npm install
npm run test:unit
npm run test:contract C-001  # validates outputs match contract
```

Expected output: all green.

## Acceptance checklist

The literal checkboxes. Agent ticks each as done.

- [ ] Project scaffolded and runs locally
- [ ] All build steps complete
- [ ] All unit tests pass (target: 100% of test scenarios in v{N}-tests.md)
- [ ] Contract validation passes (responses match C-001 shape)
- [ ] No console errors / warnings
- [ ] Code formatted, lint clean

## Definition of done

When all acceptance checkboxes are ticked AND the test invocation passes AND no follow-up TODOs are open in the code.

## Notes / risks

Anything an agent should know:
- Watch out for timezone handling in expires_at — must be UTC.
- The bcrypt cost factor is 12; don't lower it.
- Email verification is OUT OF SCOPE for this WP (separate WP-B05).

## Open questions

Linked from `00-meta/open-questions.md`:
- OQ-007 (sync conflict) — does NOT affect this WP.
- OQ-012 (rate limit specifics) — affects this WP, default = 5/min per IP per Contract C-001.

## Status (live, agent-mutable)

Maintained in `00-meta/agent-claims.md` via `sps-memory-keeper`. Latest line for this WP-ID is current state.

---
```

Save each WP to `08-architecture/05-work-packages/WP-{ID}-{slug}/v1.md`. The folder pattern is critical so each WP versions independently and gets its own backlog if needed.

### Step 4 — Index file

Write `08-architecture/05-work-packages/index.md`:

```markdown
# Work Packages Index

Total: {N} packages across {S} streams. Foundation: {A_count}. Parallel-able: {parallel_count} after foundation.

## Stream A: Foundation

| WP | Title | Status | Effort | Hard deps |
|---|---|---|---|---|
| WP-A01 | DB schema and migrations | PENDING | M | — |
| WP-A02 | Shared types package | PENDING | S | — |
| WP-A03 | Auth bootstrap | PENDING | M | A01, A02 |

## Stream B: Backend domain

| WP | Title | Status | Effort | Hard deps | Soft deps |
|---|---|---|---|---|---|
| WP-B01 | Auth-service signup + login | PENDING | M | A03 | — |
| WP-B02 | Auth-service password reset | PENDING | M | B01 | email-svc (mocked) |
| WP-B03 | Content-service CRUD | PENDING | L | A01, A02 | B01 (mocked C-001) |
...

## Stream C: Frontend app shell
...

## Stream D: Frontend features
...

## Stream E: External integrations
...
```

### Step 5 — Critical path WP highlighting

Walk the build graph and identify the WPs that lie on the critical path. Mark them in their files with a top-of-document banner:

> **CRITICAL PATH** — this WP is on the project's critical path. Delays here delay the whole project.

### Step 6 — Cross-WP coverage check

Verify:
- Every feature in L3 is implemented by at least one WP.
- Every contract in L8.3 has a producer-side WP.
- Every component in L8.2 has at least one WP.
- Every test scenario from `sps-test-writer` outputs is covered by a WP that runs it.

Any gap → push back to the user, expand or add WPs.

### Step 7 — Freeze gate

Story summary:

```
=================================================
  FREEZE GATE — L8.5 Work Packages
=================================================

  ✓ {N} work packages created across {S} streams
  
    Foundation: {A} WPs (must finish first)
    Parallel-able: {P} WPs concurrent after foundation
    Critical path: {N} WPs — {WP list}
    Coverage: every feature, contract, component covered ✓

  → Next: L8.6 integration map + integration tests
    (cross-component flows)

=================================================
```

Ask: "Freeze L8.5?"

### Step 8 — On freeze

1. Save all WP files with FROZEN spec (status field is separate — agents will mutate that).
2. Update freeze-status.md: L8.5 → FROZEN, L8.6 → PENDING.
3. Call `sps-memory-keeper log-activity` with WP count.
4. Confirm: "L8.5 frozen. {N} WPs ready for agent assignment after L8.6-L8.8 complete."

## Backlog hook

Common parking at L8.5:
- Refactoring WPs ("after build, consolidate X")
- Performance WPs (load testing, optimization)
- Documentation WPs

## Critical rules

- **Every WP is self-contained.** An agent reads one WP file and the linked specs, then can execute.
- **Every WP has a test invocation command.** Not "tests pass" — the actual command.
- **Every WP has an acceptance checklist.** Binary, observable.
- **WP size: ≤8 hours.** Bigger → split.
- **Mocks are explicit.** What to mock, how, for which contracts.
- **Hard vs soft deps clearly distinguished.** Inherits from L8.4.
- **Status field is mutable.** Agents update it (via sps-memory-keeper) as they work.
- **Coverage check is mandatory** before freeze.
