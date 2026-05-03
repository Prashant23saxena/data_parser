# Test Scenarios — F-AL-001: Chat interface

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 11  
**Spec file:** 04-specs/pillar-04-agentic-layer/F-AL-001/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Chat interface primary success path
**Given:** The app is configured and dependencies for F-AL-001 are available.
**When:** The user completes the main Chat interface action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Chat interface rejects invalid or missing required input
**Given:** The user is on the Chat interface surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-AL-001 handles error:llm-unavailable
**Given:** The feature can be forced into error:llm-unavailable.
**When:** The triggering failure occurs.
**Then:** The error:llm-unavailable state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-004: F-AL-001 edge case: Disable send on empty message.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Disable send on empty message.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-AL-001 edge case: Preserve chat history within session.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Preserve chat history within session.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-AL-001 edge case: Show model/provider error without losing user input.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Show model/provider error without losing user input.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-AL-001 edge case: Do not auto-run code from chat.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Do not auto-run code from chat.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-008: Send a plain-English request.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Send a plain-English request.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: See agent response in history.
**Given:** The feature and dependencies are available.
**When:** Tester performs: See agent response in history.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: LLM error is recoverable.
**Given:** The feature and dependencies are available.
**When:** Tester performs: LLM error is recoverable.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Starting new chat clears context.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Starting new chat clears context.
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
