# Test Scenarios — F-AL-006: Conversational follow-ups

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 10  
**Spec file:** 04-specs/pillar-04-agentic-layer/F-AL-006/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Conversational follow-ups primary success path
**Given:** The app is configured and dependencies for F-AL-006 are available.
**When:** The user completes the main Conversational follow-ups action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Conversational follow-ups rejects invalid or missing required input
**Given:** The user is on the Conversational follow-ups surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-AL-006 handles error:generation-failed
**Given:** The feature can be forced into error:generation-failed.
**When:** The triggering failure occurs.
**Then:** The error:generation-failed state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-004: F-AL-006 edge case: New chat resets context.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: New chat resets context.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-AL-006 edge case: Follow-up should preserve prior code unless user asks to start over.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Follow-up should preserve prior code unless user asks to start over.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-AL-006 edge case: If previous code was edited manually, user may need to include latest 
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: If previous code was edited manually, user may need to include latest editor content.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-007: Follow-up filter modifies previous code.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Follow-up filter modifies previous code.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-008: Follow-up aggregation builds on prior load_table calls.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Follow-up aggregation builds on prior load_table calls.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: Context reset starts fresh.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Context reset starts fresh.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Ambiguous follow-up asks clarification.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Ambiguous follow-up asks clarification.
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
