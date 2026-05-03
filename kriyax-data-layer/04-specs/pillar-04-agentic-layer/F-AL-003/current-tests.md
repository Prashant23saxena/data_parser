# Test Scenarios — F-AL-003: Generate Python/pandas code

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 11  
**Spec file:** 04-specs/pillar-04-agentic-layer/F-AL-003/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Generate Python/pandas code primary success path
**Given:** The app is configured and dependencies for F-AL-003 are available.
**When:** The user completes the main Generate Python/pandas code action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Generate Python/pandas code rejects invalid or missing required input
**Given:** The user is on the Generate Python/pandas code surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-AL-003 handles error:generation-failed
**Given:** The feature can be forced into error:generation-failed.
**When:** The triggering failure occurs.
**Then:** The error:generation-failed state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-004: F-AL-003 edge case: Ambiguous requests produce a clarification question.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Ambiguous requests produce a clarification question.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-AL-003 edge case: Generated code must not include secrets or raw DB credentials.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Generated code must not include secrets or raw DB credentials.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-AL-003 edge case: No SQL generation in v1.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: No SQL generation in v1.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-AL-003 edge case: Persisting results is suggested but not automatic unless user asked.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Persisting results is suggested but not automatic unless user asked.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-008: Request for join produces pandas merge code.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Request for join produces pandas merge code.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: Request for cleaning produces pandas transformation code.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Request for cleaning produces pandas transformation code.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Unknown column asks clarification.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Unknown column asks clarification.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Generated code uses load_table/save_table helpers.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Generated code uses load_table/save_table helpers.
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
