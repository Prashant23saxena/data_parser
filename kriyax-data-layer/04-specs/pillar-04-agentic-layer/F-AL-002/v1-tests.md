# Test Scenarios — F-AL-002: Schema-aware context loading

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 11  
**Spec file:** 04-specs/pillar-04-agentic-layer/F-AL-002/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Schema-aware context loading primary success path
**Given:** The app is configured and dependencies for F-AL-002 are available.
**When:** The user completes the main Schema-aware context loading action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Schema-aware context loading rejects invalid or missing required input
**Given:** The user is on the Schema-aware context loading surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-AL-002 handles error:catalog-unavailable
**Given:** The feature can be forced into error:catalog-unavailable.
**When:** The triggering failure occurs.
**Then:** The error:catalog-unavailable state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-004: F-AL-002 edge case: Large catalogs require relevance selection and summaries.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Large catalogs require relevance selection and summaries.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-AL-002 edge case: Missing table names trigger clarification instead of guessing.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Missing table names trigger clarification instead of guessing.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-AL-002 edge case: Metadata refreshed per request or explicit refresh.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Metadata refreshed per request or explicit refresh.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-AL-002 edge case: Sample row context remains gated by F-SC-005 policy.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Sample row context remains gated by F-SC-005 policy.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-008: Prompt context includes table names and columns.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Prompt context includes table names and columns.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: Unavailable catalog returns clear error.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Unavailable catalog returns clear error.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Large catalog is summarized without exceeding limits.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Large catalog is summarized without exceeding limits.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Agent avoids hallucinated table names.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Agent avoids hallucinated table names.
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
