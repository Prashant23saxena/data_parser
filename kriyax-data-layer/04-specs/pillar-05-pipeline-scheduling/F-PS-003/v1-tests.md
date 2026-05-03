# Test Scenarios — F-PS-003: Manual trigger

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 9  
**Spec file:** 04-specs/pillar-05-pipeline-scheduling/F-PS-003/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Manual trigger primary success path
**Given:** The app is configured and dependencies for F-PS-003 are available.
**When:** The user completes the main Manual trigger action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Manual trigger rejects invalid or missing required input
**Given:** The user is on the Manual trigger surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Edge cases

### TS-003: F-PS-003 edge case: Manual run allowed even if schedule disabled.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Manual run allowed even if schedule disabled.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-004: F-PS-003 edge case: Prevent duplicate concurrent runs for same pipeline.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Prevent duplicate concurrent runs for same pipeline.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-PS-003 edge case: Run appears in history.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Run appears in history.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-006: Click Run now executes pipeline.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Click Run now executes pipeline.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-007: Disabled scheduled pipeline can still run manually.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Disabled scheduled pipeline can still run manually.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-008: Concurrent run is blocked.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Concurrent run is blocked.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: Run history updates.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Run history updates.
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
