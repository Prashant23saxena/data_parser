# Test Scenarios — F-PS-005: Error notifications

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 9  
**Spec file:** 04-specs/pillar-05-pipeline-scheduling/F-PS-005/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Error notifications primary success path
**Given:** The app is configured and dependencies for F-PS-005 are available.
**When:** The user completes the main Error notifications action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Error notifications rejects invalid or missing required input
**Given:** The user is on the Error notifications surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Edge cases

### TS-003: F-PS-005 edge case: UI notification only in v1; no email/Slack.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: UI notification only in v1; no email/Slack.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-004: F-PS-005 edge case: Acknowledging does not delete run history.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Acknowledging does not delete run history.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-PS-005 edge case: New failure reopens badge.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: New failure reopens badge.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-006: Failed scheduled run shows badge.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Failed scheduled run shows badge.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-007: Opening detail shows error.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Opening detail shows error.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-008: Acknowledge hides active alert but keeps history.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Acknowledge hides active alert but keeps history.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: New failure returns alert.
**Given:** The feature and dependencies are available.
**When:** Tester performs: New failure returns alert.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

## Coverage map

| Spec area | Covered by scenarios |
|---|---|
| Inputs and validation | Validation scenarios plus acceptance scenarios |
| States and transitions | Happy path, error state, and acceptance scenarios |
| Edge cases | Edge case scenarios |
| Side effects and recovery | Happy path, negative, and error state scenarios |

## Gaps

- None identified at draft-test generation time. User validation may add more scenarios.

---
*Frozen on: 2026-05-02*
