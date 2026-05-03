---
name: sps-integration-mapper
description: Layer 8.6 of the sps app-design workflow. The sixth sub-step of L8. Defines integration tests — the cross-component test scenarios that run when two or more work packages are done and need to verify they wire correctly. Maps every cross-pillar link (from L3) and every cross-component contract (from L8.3) into integration test scenarios. Use after L8.5 (work packages) is frozen, when sps-app-architect routes here, or when the user says "define integration tests", "what cross-component tests do I need", "how do I verify the wires work". Produces 08-architecture/06-integration/v1.md plus sequence diagrams.
---

# Integration Mapper (Layer 8.6)

The sixth sub-skill of L8. After WPs from L8.5 are done individually, integration tests verify they work *together*. This is where cross-component bugs are caught — the auth service might be perfect, the content service might be perfect, but their interaction might be wrong.

## Preconditions

- L8.5 (work packages) must be `FROZEN`.
- L8.6 status must be `PENDING`, `IN PROGRESS`, or `NEEDS_REVISION`.

## Inputs

- Project root path
- Mode: `fresh` or `revise`

## Process

### Step 1 — Memory + context

Call `sps-memory-keeper read-context`.

Read:
- L3 features — especially the **cross-pillar links** captured during feature decomposition. These are integration points by design.
- L4 specs — side effects sections often imply integration scenarios.
- L8.2 components — the boundaries.
- L8.3 contracts — every contract is an integration point that needs verification.
- L8.5 work packages — integration tests reference WPs (which must be done before the test can run).

### Step 2 — Enumerate integration scenarios

Walk three sources to build the integration test list:

**2a. From L3 cross-pillar links.** Every time a feature notes "cross-pillar link to F-XX-YYY", that's an integration scenario. Example:
- F-ON-001 (signup) creates default workspace via cross-link to F-CO-001
- → INT-001: signup successfully creates a default workspace in content-service

**2b. From L8.3 contracts.** Each contract has at least one integration test verifying:
- Producer matches contract spec exactly
- Consumer correctly calls and parses
- Error paths work end-to-end (not just at the producer)

**2c. From L4 side effects.** Side effects that span components imply integration. Example:
- F-CO-005 spec says "on task created, send notification" → INT-005: creating a task fires a notification event consumed by notifications-service

For each, assign INT-NNN and describe.

### Step 3 — For each integration scenario, define

```
INT-{NNN}: {Scenario name}

Components involved:
  Producer: {component} (WP-{ID})
  Consumer: {component} (WP-{ID})
  Optional intermediaries: {list}

Contract under test: C-{NNN} (or "multiple")

Preconditions (WPs that must be DONE):
  WP-A01, WP-A03 (foundation)
  WP-B01 (auth-service)
  WP-B03 (content-service)

Test setup:
  - Empty DB
  - One test user created via auth-service signup
  - Auth token obtained

Test steps (Given/When/Then):
  Given: authenticated user, no tasks
  When: POST /tasks with valid payload
  Then: 
    - 201 returned with task shape per C-003
    - Task visible in DB (verify via direct query OR via GET /tasks)
    - Event emitted on `task.created` channel per C-005
    - Notifications-service received event (verify via its log/state)

Failure modes covered:
  - Network failure between services → 5xx, no partial state
  - Auth token expired → 401, no task created
  - DB unavailable → 5xx, retry contract honored
  - Event broker down → task still created, event reconciliation on broker recovery (per OQ-008 default)

Test invocation:
  cd integration-tests
  npm run test:integration -- INT-001

Verification:
  - All assertions pass
  - No log errors except expected ones
  - DB state matches expected post-state
```

### Step 4 — Sequence diagrams

For each integration scenario, generate a sequence diagram showing message flow over time:

```
User → auth-service: POST /signup {email, password, name}
auth-service → DB: INSERT user
auth-service → email-svc: send verification email
auth-service ⇒ User: 201 {user, session}
[user clicks email link]
User → auth-service: POST /verify {token}
auth-service → DB: UPDATE user.verified=true
auth-service ⇒ content-service: emit user.verified event
content-service → DB: INSERT default workspace
content-service ⇒ User: (no direct response — via next request)
```

Call `sps-visual-maker` per scenario:
- type: `sequence-diagram` (variant of flow-chart)
- format: ask (ASCII default; HTML for >5 actors)
- output_path: `visuals/08-int-{INT-ID}-v{N}.{ext}`

### Step 5 — Coverage checks

Verify:
- Every contract has at least one integration test
- Every cross-pillar link from L3 has a test
- Every multi-component side effect from L4 has a test
- Every critical user flow from L5 has at least one integration test (full e2e flow tests are L8.7 UAT, but the mid-level integration smoke tests can also live here — flag overlap and split appropriately)

If gaps: add tests or note explicitly why omitted.

### Step 6 — Synthesize draft

Write `08-architecture/06-integration/v{N}.md`:

```markdown
# Integration Tests — {App Name}

**Version:** v{N}
**Status:** DRAFT
**Last updated:** {today}

## Overview

{N} integration scenarios covering all cross-component interactions. Total contracts under test: {N}. Cross-pillar links covered: {N}/{N}.

## Test environment

- Database: in-memory or test instance, reset between scenarios
- External services: mocked or sandboxed
- Auth: real auth-service (via test user) — no mocks for it at integration level

## Scenarios

### INT-001: Signup creates default workspace

(full structured definition per Step 3)

### INT-002: ...

...

## Test ordering

Some integration tests build on others (faster/cheaper to run shared setup). Recommended order:
1. Foundation tests (auth alone, content alone)
2. Two-service tests (auth + content)
3. Three-service tests (auth + content + notifications)
4. Full end-to-end (deferred to L8.7 UAT)

## Coverage matrix

| Contract | Tested by |
|---|---|
| C-001 (Auth API) | INT-001, INT-002, INT-003 |
| C-003 (Task API) | INT-001, INT-005 |
| C-005 (task.created event) | INT-001, INT-005, INT-006 |
| ... | ... |

| Cross-pillar link | Tested by |
|---|---|
| F-ON-001 → F-CO-001 (default workspace creation) | INT-001 |
| F-CO-005 → F-NO-001 (task notifications) | INT-005 |
| ... | ... |

## Gaps

(scenarios intentionally not covered, with reason)

---

*Frozen on: {date when frozen}*
```

### Step 7 — Freeze gate

Story summary:

```
=================================================
  FREEZE GATE — L8.6 Integration Tests
=================================================

  ✓ {N} integration scenarios defined
  
    Contracts covered: {N}/{N}
    Cross-pillar links covered: {N}/{N}
    Sequence diagrams: {N}
    Failure modes per scenario: {N} avg

  → Next: L8.7 UAT scenarios (end-to-end user flows
    from L5 critical flows)

=================================================
```

Ask: "Freeze L8.6?"

### Step 8 — On freeze

1. Save FROZEN. Update freeze-status.md: L8.6 → FROZEN, L8.7 → PENDING.
2. Call `sps-memory-keeper log-activity`.
3. Confirm: "L8.6 frozen. Run sps-uat-scripter for L8.7."

## Backlog hook

- Performance integration tests for v2
- Chaos / fault injection scenarios for resilience phase

## Critical rules

- **Every contract must be tested at integration level.** Not just unit-level.
- **Failure modes are required per scenario.** Happy path alone isn't integration testing.
- **Sequence diagrams are required.** They're how a developer sees the flow.
- **Tests cite WP preconditions explicitly.** So agents know when a test is runnable.
- **Distinct from UAT.** Integration tests are between 2-N components; UAT is full user journey.
