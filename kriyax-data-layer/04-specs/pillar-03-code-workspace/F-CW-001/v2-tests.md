# Test Scenarios — F-CW-001: Python code editor

**Spec version:** v2  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 14  
**Spec file:** 04-specs/pillar-03-code-workspace/F-CW-001/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Python code editor primary success path
**Given:** The app is configured and dependencies for F-CW-001 are available.
**When:** The user completes the main Python code editor action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Python code editor rejects invalid or missing required input
**Given:** The user is on the Python code editor surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-CW-001 handles error:syntax
**Given:** The feature can be forced into error:syntax.
**When:** The triggering failure occurs.
**Then:** The error:syntax state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-004: F-CW-001 handles error:runtime
**Given:** The feature can be forced into error:runtime.
**When:** The triggering failure occurs.
**Then:** The error:runtime state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-005: F-CW-001 handles error:timeout
**Given:** The feature can be forced into error:timeout.
**When:** The triggering failure occurs.
**Then:** The error:timeout state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-006: F-CW-001 edge case: Run disabled for empty code.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Run disabled for empty code.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-CW-001 edge case: Editor becomes read-only during execution to avoid racing state.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Editor becomes read-only during execution to avoid racing state.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-008: F-CW-001 edge case: Syntax errors are reported in output without losing code.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Syntax errors are reported in output without losing code.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-009: F-CW-001 edge case: Long-running scripts are killed at timeout.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Long-running scripts are killed at timeout.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-010: F-CW-001 edge case: Only approved packages are available in the sandbox.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Only approved packages are available in the sandbox.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-011: Write pandas code and run it successfully.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Write pandas code and run it successfully.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-012: Syntax error shows line-linked traceback.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Syntax error shows line-linked traceback.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-013: Infinite loop times out and returns control.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Infinite loop times out and returns control.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-014: Code remains in editor after failure.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Code remains in editor after failure.
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
