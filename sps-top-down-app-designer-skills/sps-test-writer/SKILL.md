---
name: sps-test-writer
description: Convert a frozen L4 feature spec into actionable test scenarios — happy path, validation, error states, edge cases, state transitions, side effects. Output is a sibling test file (vN-tests.md) next to the spec, version-locked to it. Use when sps-feature-detailer reaches its freeze gate (auto-invoked), or when the user says "write tests for feature X", "generate test scenarios for {feature ID}", "I want a test plan for the {feature} spec". Each scenario follows Given/When/Then with verifiable outcomes, test data, and a coverage map proving every spec section is tested. Horizontal utility.
---

# Test Writer

Generates a complete test scenario file for one frozen feature spec at a time. The output is a sibling document to the spec (`vN-tests.md` next to `vN.md`), version-locked, that a human or AI tester can execute against.

## When this skill runs

**Embedded mode:** Invoked by `sps-feature-detailer` at its L4 freeze gate, automatically, for the feature being frozen. The spec and tests freeze together as siblings.

**Standalone mode:** User says "write tests for F-XX-YYY". The skill reads the frozen spec and produces tests independently. Useful when re-generating tests after spec changes, or when adding tests to features specced before this skill existed.

## Inputs

- Project root path
- `feature_ref` — pillar slug + feature ID (e.g. `pillar-01-onboarding/F-ON-001`)
- Mode: `embedded` (called from sps-feature-detailer) or `standalone`

## Preconditions

- The feature spec (`04-specs/{pillar}/{feature}/v{N}.md`) must exist and be DRAFT or FROZEN.
- If in standalone mode and spec is DRAFT, warn the user that tests written now may need updating when spec freezes.

## Process

### Step 1 — Memory + spec read

Call `sps-memory-keeper read-context` with caller=`sps-test-writer`.

Read the target feature spec in full. Parse out:
- Inputs (with validation rules)
- States (and transitions)
- Edge cases
- Side effects
- Acceptance checklist (if exists)

If any section is empty or vague, note it — tests will be limited there.

### Step 2 — Light domain research

1-2 web searches if helpful for testing patterns specific to the feature type:
- "{feature type} test scenarios"
- "Common bugs in {feature type}"

Optional. Skip if the spec is already detailed enough to drive scenarios directly.

### Step 3 — Generate scenarios by category

Walk the spec systematically. For each spec section, generate scenarios.

**3a. Happy path scenarios.** From the primary state path. Usually 1-3 scenarios:
- The simplest valid case
- The most common case
- A representative successful variation

**3b. Validation scenarios.** One per validation rule from the Inputs section:
- Empty field (when required)
- Each format rule (e.g. email format)
- Min/max length boundary
- Each allowed-value constraint

**3c. Error state scenarios.** One per error state from the States section:
- Network failure
- Server error
- Conflict (e.g. duplicate)
- Rate limit
- Timeout
- Auth/permission failure

**3d. Edge case scenarios.** One per edge case from the spec:
- Whatever the spec listed in its edge cases section
- Additionally probe: very long input, special characters, trailing whitespace, Unicode, concurrent action, slow connection, offline, expired session

**3e. State transition scenarios.** Cover every transition in the spec's state diagram:
- For each (from → to) pair, a scenario that triggers it
- Confirm side effects fire

**3f. Side effect scenarios.** Each side effect from the spec gets a verification scenario, especially cross-pillar ones.

**3g. Negative scenarios.** What should NOT happen:
- Action prevented when in wrong state
- Action prevented for unauthorized user
- No partial state on failure (atomicity)

### Step 4 — Write test file

Write to `04-specs/{pillar}/{feature}/v{N}-tests.md`:

```markdown
# Test Scenarios — {Feature ID}: {Feature Name}

**Spec version:** v{N}  
**Generated:** {today}  
**Status:** DRAFT (or FROZEN once spec freezes)  
**Total scenarios:** {count}  
**Pillar:** {pillar slug}

## How to use

Each scenario has Given/When/Then plus verification steps. Run them in order within each section. Test data sample appendix at the bottom. Coverage map at the end shows which spec sections are covered.

## 1. Happy path

### TS-001: {Scenario name — concise}
**Given:** {preconditions, environment, prior state}
**When:** {single user action or trigger}
**Then:** {expected outcome — observable}

**Verify:**
- [ ] {observable check 1}
- [ ] {observable check 2}

**Test data:** {specific values used}

---

### TS-002: ...

## 2. Validation

### TS-010: {Validation rule}
... (same format)

## 3. Error states

### TS-020: ...

## 4. Edge cases

### TS-030: ...

## 5. State transitions

### TS-040: {from-state → to-state via trigger}
**Given:** feature is in state {from-state}, {context}
**When:** {trigger}
**Then:** feature moves to state {to-state}

**Verify:**
- [ ] state visible to user matches {to-state}'s spec
- [ ] side effects fired: {list}
- [ ] no unintended side effects

## 6. Side effects

### TS-050: {side effect name}
... 

## 7. Negative scenarios

### TS-060: {action that should be blocked}
**Given:** {context that should block the action}
**When:** {action attempted}
**Then:** action is rejected, no state changes, error message: "{exact text}"

## Test data appendix

| Variable | Sample valid | Sample invalid |
|---|---|---|
| {field} | {valid example(s)} | {invalid examples with reason} |
| ... | ... | ... |

## Coverage map

This section proves every part of the spec is tested. Update if scenarios change.

| Spec section | Covered by scenarios |
|---|---|
| Inputs / {field 1} validation | TS-010, TS-011, ... |
| Inputs / {field 2} validation | TS-012, TS-013, ... |
| State: {state 1} | TS-001, TS-040, ... |
| State: {state 2} | TS-020, ... |
| Edge case: {description} | TS-030 |
| Side effect: {name} | TS-050 |
| Negative: {description} | TS-060 |

## Gaps

Sections of the spec that are not covered by scenarios (and why):
- {section} — {reason: not testable, deferred to integration tests, etc.}

---

*Frozen on: {date when frozen, copied from spec freeze}*
```

### Step 5 — Show summary to user

Show the user:
- Total scenarios by category (3 happy, 5 validation, 4 error, 6 edge, 8 transitions, 3 side effects, 2 negative = 31 total)
- Coverage map highlights — anything not covered
- Gaps section if any

Ask: "Looks good? Any scenarios to add, refine, or remove?"

Iterate until the user is satisfied. In embedded mode (auto-invoked by feature-detailer), skip the iteration if the user just wants to freeze quickly — but still show the summary.

### Step 6 — Save and tie to spec

In standalone mode, save with status DRAFT and tell the user "tests are draft until the spec freezes".

In embedded mode, save with status matching the spec — when feature-detailer freezes the spec at v{N}, the test file freezes at the same time.

### Step 7 — Memory hygiene

Call `sps-memory-keeper`:
- `log-activity` — event="generated test scenarios for {feature ID} ({count} scenarios)"
- If scenarios revealed gaps in the spec (e.g. "this state can't be tested because the trigger isn't specified"), call `flag-revision` against L4 for that feature.

## Coverage rules (hard)

Before declaring done, verify:
- Every input field with a validation rule has at least one validation scenario
- Every state in the spec has at least one scenario where the system is observed in that state
- Every transition has at least one scenario
- Every edge case in the spec has at least one scenario
- Every side effect has at least one scenario

If any of these are missing, either add the missing scenario or note it explicitly in the Gaps section with a reason.

## Critical rules

- **One feature per run.** Don't merge tests for multiple features.
- **Scenarios must be observable.** "Then: it works" is bad. "Then: a 200 response with body matching {schema}" or "Then: the success state is visible with the text 'Welcome, {user}'" is good.
- **Exact error text.** When the spec specifies error messages, the test scenarios use the exact text.
- **Test data is concrete.** Don't write "a valid email" — write "user@example.com".
- **Coverage map is mandatory.** Without it, the test file is just a wishlist.
- **Tie test file version to spec version.** v{N}-tests.md goes with v{N}.md.
- **Negative scenarios are mandatory.** What shouldn't happen is as important as what should.
