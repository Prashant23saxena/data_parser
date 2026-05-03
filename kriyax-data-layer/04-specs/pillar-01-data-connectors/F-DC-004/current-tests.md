# Test Scenarios — F-DC-004: Configure Odoo connection

**Spec version:** v2  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 16  
**Spec file:** 04-specs/pillar-01-data-connectors/F-DC-004/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Configure Odoo connection primary success path
**Given:** The app is configured and dependencies for F-DC-004 are available.
**When:** The user completes the main Configure Odoo connection action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Configure Odoo connection rejects invalid or missing required input
**Given:** The user is on the Configure Odoo connection surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-DC-004 handles error:unreachable
**Given:** The feature can be forced into error:unreachable.
**When:** The triggering failure occurs.
**Then:** The error:unreachable state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-004: F-DC-004 handles error:auth-failed
**Given:** The feature can be forced into error:auth-failed.
**When:** The triggering failure occurs.
**Then:** The error:auth-failed state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-005: F-DC-004 handles error:invalid-db
**Given:** The feature can be forced into error:invalid-db.
**When:** The triggering failure occurs.
**Then:** The error:invalid-db state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-006: F-DC-004 edge case: URL with trailing slash → strip it
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: URL with trailing slash → strip it
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-DC-004 edge case: URL without protocol → prepend https://
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: URL without protocol → prepend https://
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-008: F-DC-004 edge case: Self-signed SSL certificate → show warning, allow proceed
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Self-signed SSL certificate → show warning, allow proceed
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-009: F-DC-004 edge case: API key with leading/trailing spaces → trim
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: API key with leading/trailing spaces → trim
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-010: F-DC-004 edge case: Connection name already exists → error: "A connection with this name a
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Connection name already exists → error: "A connection with this name already exists"
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-011: Valid Odoo credentials → test succeeds, save works
**Given:** The feature and dependencies are available.
**When:** Tester performs: Valid Odoo credentials → test succeeds, save works
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-012: Wrong API key → error:auth-failed
**Given:** The feature and dependencies are available.
**When:** Tester performs: Wrong API key → error:auth-failed
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-013: Wrong URL → error:unreachable
**Given:** The feature and dependencies are available.
**When:** Tester performs: Wrong URL → error:unreachable
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-014: Wrong DB name → error:invalid-db
**Given:** The feature and dependencies are available.
**When:** Tester performs: Wrong DB name → error:invalid-db
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-015: Saved connection appears in connection list (F-DC-008)
**Given:** The feature and dependencies are available.
**When:** Tester performs: Saved connection appears in connection list (F-DC-008)
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-016: Saved connection can be reused by model browsing, record fetch, incremental sync, and pipeline steps
**Given:** The feature and dependencies are available.
**When:** Tester performs: Saved connection can be reused by model browsing, record fetch, incremental sync, and pipeline steps
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
