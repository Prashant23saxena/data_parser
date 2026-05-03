# Test Scenarios — F-AL-004: Insert code into editor

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 10  
**Spec file:** 04-specs/pillar-04-agentic-layer/F-AL-004/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Insert code into editor primary success path
**Given:** The app is configured and dependencies for F-AL-004 are available.
**When:** The user completes the main Insert code into editor action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Insert code into editor rejects invalid or missing required input
**Given:** The user is on the Insert code into editor surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-AL-004 handles error:editor-unavailable
**Given:** The feature can be forced into error:editor-unavailable.
**When:** The triggering failure occurs.
**Then:** The error:editor-unavailable state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-004: F-AL-004 edge case: Never auto-execute inserted code.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Never auto-execute inserted code.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-AL-004 edge case: If editor has unsaved edits, confirm replace/append behavior.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: If editor has unsaved edits, confirm replace/append behavior.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-AL-004 edge case: Preserve generated code block formatting.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Preserve generated code block formatting.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-007: Insert generated code into empty editor.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Insert generated code into empty editor.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-008: Warn before replacing unsaved editor content.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Warn before replacing unsaved editor content.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: Inserted code remains editable.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Inserted code remains editable.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Run still requires user click.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Run still requires user click.
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
