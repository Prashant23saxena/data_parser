# Test Scenarios — F-CW-005: View execution output

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 11  
**Spec file:** 04-specs/pillar-03-code-workspace/F-CW-005/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: View execution output primary success path
**Given:** The app is configured and dependencies for F-CW-005 are available.
**When:** The user completes the main View execution output action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: View execution output rejects invalid or missing required input
**Given:** The user is on the View execution output surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-CW-005 handles error output
**Given:** The feature can be forced into error output.
**When:** The triggering failure occurs.
**Then:** The error output state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-004: F-CW-005 edge case: Large output truncates with explicit message and retained downloadable
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Large output truncates with explicit message and retained downloadable log later if needed.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-CW-005 edge case: DataFrame result preview shows head rows and shape.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: DataFrame result preview shows head rows and shape.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-CW-005 edge case: Tracebacks preserve line numbers.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Tracebacks preserve line numbers.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-CW-005 edge case: Re-run clears old output only after new run starts.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Re-run clears old output only after new run starts.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-008: print output appears.
**Given:** The feature and dependencies are available.
**When:** Tester performs: print output appears.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: DataFrame preview appears with shape.
**Given:** The feature and dependencies are available.
**When:** Tester performs: DataFrame preview appears with shape.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Runtime traceback appears clearly.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Runtime traceback appears clearly.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Large output is truncated safely.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Large output is truncated safely.
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
