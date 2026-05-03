# Test Scenarios — F-AL-005: Self-correction on error

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 12  
**Spec file:** 04-specs/pillar-04-agentic-layer/F-AL-005/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Self-correction on error primary success path
**Given:** The app is configured and dependencies for F-AL-005 are available.
**When:** The user completes the main Self-correction on error action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Self-correction on error rejects invalid or missing required input
**Given:** The user is on the Self-correction on error surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-AL-005 handles error captured
**Given:** The feature can be forced into error captured.
**When:** The triggering failure occurs.
**Then:** The error captured state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-004: F-AL-005 handles error:fix-failed
**Given:** The feature can be forced into error:fix-failed.
**When:** The triggering failure occurs.
**Then:** The error:fix-failed state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-005: F-AL-005 edge case: Limit automatic correction attempts, recommended max 2 before asking u
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Limit automatic correction attempts, recommended max 2 before asking user.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-AL-005 edge case: Fix proposal never auto-runs.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Fix proposal never auto-runs.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-AL-005 edge case: Tracebacks are included; secrets are redacted.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Tracebacks are included; secrets are redacted.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-008: F-AL-005 edge case: If error indicates missing table/column, refresh schema context.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: If error indicates missing table/column, refresh schema context.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-009: KeyError triggers corrected column reference or clarification.
**Given:** The feature and dependencies are available.
**When:** Tester performs: KeyError triggers corrected column reference or clarification.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Syntax error returns valid corrected code.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Syntax error returns valid corrected code.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Second failed fix stops with clear message.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Second failed fix stops with clear message.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-012: User must approve insert/run.
**Given:** The feature and dependencies are available.
**When:** Tester performs: User must approve insert/run.
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
