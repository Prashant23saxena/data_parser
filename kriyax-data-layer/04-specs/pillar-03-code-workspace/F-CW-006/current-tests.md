# Test Scenarios — F-CW-006: Save & re-run scripts

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 12  
**Spec file:** 04-specs/pillar-03-code-workspace/F-CW-006/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Save & re-run scripts primary success path
**Given:** The app is configured and dependencies for F-CW-006 are available.
**When:** The user completes the main Save & re-run scripts action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Save & re-run scripts rejects invalid or missing required input
**Given:** The user is on the Save & re-run scripts surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-CW-006 handles error:name-conflict
**Given:** The feature can be forced into error:name-conflict.
**When:** The triggering failure occurs.
**Then:** The error:name-conflict state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-004: F-CW-006 handles error:save-failed
**Given:** The feature can be forced into error:save-failed.
**When:** The triggering failure occurs.
**Then:** The error:save-failed state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-005: F-CW-006 edge case: Renaming existing script requires unique name.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Renaming existing script requires unique name.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-CW-006 edge case: Saved script persists across sessions.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Saved script persists across sessions.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-CW-006 edge case: Manual re-run uses current saved content.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Manual re-run uses current saved content.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-008: F-CW-006 edge case: Pipeline references stable script id, not just name.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Pipeline references stable script id, not just name.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-009: Save current code as named script.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Save current code as named script.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Open saved script into editor.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Open saved script into editor.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Re-run saved script manually.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Re-run saved script manually.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-012: Saved script appears as pipeline candidate.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Saved script appears as pipeline candidate.
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
