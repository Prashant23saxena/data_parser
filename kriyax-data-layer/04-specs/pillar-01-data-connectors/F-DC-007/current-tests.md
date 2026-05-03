# Test Scenarios — F-DC-007: Incremental/delta sync

**Spec version:** v2  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 11  
**Spec file:** 04-specs/pillar-01-data-connectors/F-DC-007/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Incremental/delta sync primary success path
**Given:** The app is configured and dependencies for F-DC-007 are available.
**When:** The user completes the main Incremental/delta sync action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Incremental/delta sync rejects invalid or missing required input
**Given:** The user is on the Incremental/delta sync surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-DC-007 handles error:sync-failed
**Given:** The feature can be forced into error:sync-failed.
**When:** The triggering failure occurs.
**Then:** The error:sync-failed state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-004: F-DC-007 edge case: First sync on a table that was full-refreshed → cursor starts from tab
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: First sync on a table that was full-refreshed → cursor starts from table's last fetch timestamp
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-DC-007 edge case: Odoo record deleted at source → NOT detected by incremental (known lim
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Odoo record deleted at source → NOT detected by incremental (known limitation, document it)
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-DC-007 edge case: Clock skew between Odoo server and local → use Odoo's server time, not
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Clock skew between Odoo server and local → use Odoo's server time, not local time
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-DC-007 edge case: Cursor field doesn't exist on model → error before sync: "Field '{{cur
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Cursor field doesn't exist on model → error before sync: "Field '{{cursor_field}}' not found"
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-008: Modify a record in Odoo → sync picks it up, updates in local table
**Given:** The feature and dependencies are available.
**When:** Tester performs: Modify a record in Odoo → sync picks it up, updates in local table
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: Add a record in Odoo → sync inserts it
**Given:** The feature and dependencies are available.
**When:** Tester performs: Add a record in Odoo → sync inserts it
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: No changes → "Already up to date" message
**Given:** The feature and dependencies are available.
**When:** Tester performs: No changes → "Already up to date" message
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Pipeline triggers sync → works without manual interaction
**Given:** The feature and dependencies are available.
**When:** Tester performs: Pipeline triggers sync → works without manual interaction
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
