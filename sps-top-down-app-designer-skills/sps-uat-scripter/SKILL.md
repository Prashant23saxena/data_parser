---
name: sps-uat-scripter
description: Layer 8.7 of the sps app-design workflow. The seventh sub-step of L8. Defines User Acceptance Test scenarios — end-to-end user journeys built from L5's critical flows. UAT is what a human (or human-simulating agent) runs at the end to validate "the app actually does what was promised in L1's vision". Use after L8.6 (integration tests) is frozen, when sps-app-architect routes here, or when the user says "write UAT scenarios", "define end-to-end tests", "what does final acceptance look like". Produces 08-architecture/07-uat/v1.md.
---

# UAT Scripter (Layer 8.7)

The seventh sub-skill of L8. Defines end-to-end user acceptance tests. Where unit tests verify a feature, integration tests verify components wire correctly, UAT verifies **the user can actually accomplish what L1 promised**.

UAT scenarios should be runnable by a non-developer human, or a UI-driving agent, with no engineering knowledge of the system internals.

## Preconditions

- L8.6 (integration tests) must be `FROZEN`.
- L8.7 status must be `PENDING`, `IN PROGRESS`, or `NEEDS_REVISION`.

## Inputs

- Project root path
- Mode: `fresh` or `revise`

## Process

### Step 1 — Memory + context

Call `sps-memory-keeper read-context`.

Read:
- L1 vision (the promise — UAT verifies this is delivered)
- L1 success criteria (these are literally UAT acceptance)
- L3 features (must / should priorities — UAT covers musts, optionally shoulds)
- L5 screens + critical user flows (the basis for UAT scenarios)
- L8.6 integration tests (UAT shouldn't duplicate; UAT is end-user view)

### Step 2 — Map L5 critical flows to UAT

Every critical flow from L5 becomes at least one UAT scenario. Common patterns:

- **First-run flow** → UAT-001: "New user can sign up, complete onboarding, and reach first useful state"
- **Daily core flow** → UAT-002: "Returning user can perform their primary action successfully"
- **Recovery flow** → UAT-003: "User who forgot password can reset and log back in"
- **Error recovery flow** → UAT-004: "User experiencing network failure can retry and recover"

Add UAT scenarios for L1 success criteria not yet covered:
- If L1 says "user spends <30 sec completing primary action" → UAT-005 with timing assertion
- If L1 says "no data lost across devices" → UAT-006 multi-device scenario

### Step 3 — Write each UAT scenario

These differ from integration tests in three ways:
- **User-language steps,** not API calls
- **Observable from UI only,** no DB inspection or log diving
- **Whole-flow,** not single integration

```
UAT-{NNN}: {Scenario title — phrased as user achievement}

Persona: {who the user is — usually from L1, "first-time user", "returning user", etc.}

Goal: {what the user is trying to accomplish in plain language}

Preconditions:
  - {observable prerequisite, e.g. "no account exists with email tester+1@example.com"}
  - {known initial state}

Setup data:
  - {test account credentials, fixtures}

Steps (user actions, not API calls):
  1. Navigate to {URL or open app}
  2. Click "{button/link visible to user}"
  3. Enter "{value}" in field labeled "{label}"
  4. Click "{button}"
  5. Wait for {observable state change}
  6. Verify {observable on screen}
  ...

Expected end state:
  - {what the user sees/can do that they couldn't before}
  - {data persisted observably}

Pass criteria (binary):
  - [ ] All steps completable by following on-screen affordances only
  - [ ] No error messages shown unless step expects one
  - [ ] End state achieved within {time budget if applicable}
  - [ ] No console errors visible to user
  - [ ] {specific success criteria from L1}

Fail modes (any of these = fail):
  - User can't find a required UI element
  - Error shown without expected recovery path
  - Action takes >{N}x longer than expected
  - End state not reached

Linked to: L1 success criteria {N}, L5 critical flow {name}, features F-XX-YYY
```

### Step 4 — Edge cases at UAT level

In addition to happy-path UAT, define a few edge UAT scenarios. These differ from L4 unit edge cases — UAT edges are user-experienced edge journeys:

- **Slow network UAT:** "User on 3G can still complete primary action within {N}s"
- **Re-entry UAT:** "User who closes and reopens app mid-flow can resume"
- **Device switch UAT:** "User who starts on phone, continues on desktop, sees same state"
- **Empty-state UAT:** "First-time user is gracefully guided when nothing exists yet"
- **Saturated-state UAT:** "User with 1000+ items can still find and use a specific one"

Pick the ones that matter for this app's vision. Don't write UAT for everything — UAT is expensive to run.

### Step 5 — UAT for non-functional requirements

If L1 or L7 includes non-functional requirements (performance, security, accessibility), UAT covers them:

- **Accessibility UAT:** "User with screen reader can complete primary flow"
- **Performance UAT:** "Page loads in <2s on slowest target device"
- **Security UAT:** "User logged out from Device A cannot access via stale session on Device B"

These are often the differentiators between "works" and "shipped."

### Step 6 — Synthesize draft

Write `08-architecture/07-uat/v{N}.md`:

```markdown
# UAT Scenarios — {App Name}

**Version:** v{N}
**Status:** DRAFT
**Last updated:** {today}

## Overview

{N} UAT scenarios verifying L1 vision is delivered. Run order: critical flows first, edge UAT after, non-functional last.

## Vision recap

(copy from L1 — this is what UAT verifies)

> Promise: ...
> Success criteria: ...

## Critical flow scenarios

### UAT-001: {Scenario title}
(full structured definition per Step 3)

### UAT-002: ...

## Edge journey scenarios

### UAT-010: Slow network completion
...

## Non-functional scenarios

### UAT-020: Screen reader accessibility — primary flow
...

## Coverage matrix

| L1 success criterion | UAT covering it |
|---|---|
| {criterion 1} | UAT-001, UAT-005 |
| {criterion 2} | UAT-002 |
| ... | ... |

| L5 critical flow | UAT covering it |
|---|---|
| First-run signup | UAT-001 |
| Daily core | UAT-002 |
| ... | ... |

## Run protocol

Recommended order for executing UAT:
1. UAT-001..00X — critical flows (must all pass before considering shipping)
2. UAT-010..01X — edge journeys (high-value bugs surface here)
3. UAT-020..02X — non-functional (often deferred to last)

Pass threshold for shipping: 100% of critical-flow UATs, ≥80% of edge UATs, all non-functional UATs.

## Tools recommended

- Manual: human follows the steps, ticks the checkboxes
- Automated: Playwright/Cypress/etc. (links to scripts if implemented)
- AI-driven: agent with browser-automation capability + this UAT file as input

## Gaps

UAT scenarios intentionally omitted:
- {scenario} — {reason: covered by integration tests, deferred, etc.}

---

*Frozen on: {date when frozen}*
```

### Step 7 — Freeze gate

Story summary:

```
=================================================
  FREEZE GATE — L8.7 UAT Scenarios
=================================================

  ✓ {N} UAT scenarios defined
  
    Critical flows covered: {N}/{N}
    L1 success criteria covered: {N}/{N}
    Edge journeys: {N}
    Non-functional: {N}

  → Next: L8.8 agent briefer (the final L8 step — produces
    agent-instructions.md and the live build checklist)

=================================================
```

Ask: "Freeze L8.7?"

### Step 8 — On freeze

1. Save FROZEN. Update freeze-status.md: L8.7 → FROZEN, L8.8 → PENDING.
2. Call `sps-memory-keeper log-activity`.
3. Confirm: "L8.7 frozen. Run sps-agent-briefer for L8.8 — the final design step."

## Backlog hook

- Localization UAT (multi-language flows)
- A/B variant UAT
- Long-running session UAT (week-long usage)

## Critical rules

- **Steps are user-observable only.** No API calls, no DB queries.
- **Pass criteria binary.** Either all checkboxes tick or it failed.
- **Every L1 success criterion has at least one UAT.**
- **Every L5 critical flow has at least one UAT.**
- **UAT scenarios runnable by non-developer.** Test the test by reading it aloud.
- **Don't duplicate integration tests.** UAT is the user's view; integration tests are component-pair view.
