# Test Scenarios — F-PS-004: Run history & status

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 11  
**Spec file:** 04-specs/pillar-05-pipeline-scheduling/F-PS-004/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Run history & status primary success path
**Given:** The app is configured and dependencies for F-PS-004 are available.
**When:** The user completes the main Run history & status action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Run history & status rejects invalid or missing required input
**Given:** The user is on the Run history & status surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-PS-004 handles error:history-unavailable
**Given:** The feature can be forced into error:history-unavailable.
**When:** The triggering failure occurs.
**Then:** The error:history-unavailable state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-004: F-PS-004 edge case: Newest runs first.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Newest runs first.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-PS-004 edge case: Failed run shows traceback/log.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Failed run shows traceback/log.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-PS-004 edge case: Running run updates status.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Running run updates status.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-PS-004 edge case: Long history paginated.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Long history paginated.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-008: Manual run appears in history.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Manual run appears in history.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: Failed run shows error.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Failed run shows error.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Running status updates to success/failure.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Running status updates to success/failure.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: History persists across sessions.
**Given:** The feature and dependencies are available.
**When:** Tester performs: History persists across sessions.
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
