# Test Scenarios — F-PS-006: Enable/disable pipeline

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 10  
**Spec file:** 04-specs/pillar-05-pipeline-scheduling/F-PS-006/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Enable/disable pipeline primary success path
**Given:** The app is configured and dependencies for F-PS-006 are available.
**When:** The user completes the main Enable/disable pipeline action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Enable/disable pipeline rejects invalid or missing required input
**Given:** The user is on the Enable/disable pipeline surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-PS-006 handles error:update-failed
**Given:** The feature can be forced into error:update-failed.
**When:** The triggering failure occurs.
**Then:** The error:update-failed state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-004: F-PS-006 edge case: Disabled pipelines skip schedule.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Disabled pipelines skip schedule.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-PS-006 edge case: Manual trigger remains available.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Manual trigger remains available.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-PS-006 edge case: Re-enable resumes schedule and recalculates next run.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Re-enable resumes schedule and recalculates next run.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-007: Disable pipeline stops scheduled runs.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Disable pipeline stops scheduled runs.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-008: Manual run still works while disabled.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Manual run still works while disabled.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: Re-enable restores next run.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Re-enable restores next run.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Status visible in pipeline list.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Status visible in pipeline list.
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
