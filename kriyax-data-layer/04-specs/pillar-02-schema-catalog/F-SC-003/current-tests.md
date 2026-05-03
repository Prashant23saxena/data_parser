# Test Scenarios — F-SC-003: Auto-register on ingest

**Spec version:** v2  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 9  
**Spec file:** 04-specs/pillar-02-schema-catalog/F-SC-003/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Auto-register on ingest primary success path
**Given:** The app is configured and dependencies for F-SC-003 are available.
**When:** The user completes the main Auto-register on ingest action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Error states

### TS-002: F-SC-003 handles error:registration-failed
**Given:** The feature can be forced into error:registration-failed.
**When:** The triggering failure occurs.
**Then:** The error:registration-failed state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-003: F-SC-003 edge case: Connector imports are new-table-only in v1 → create a new catalog entr
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Connector imports are new-table-only in v1 → create a new catalog entry only after the new table is created
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-004: F-SC-003 edge case: Derived table replacement from save_table(), if approved later, → upda
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Derived table replacement from save_table(), if approved later, → update catalog entry, don't create duplicate
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-005: F-SC-003 edge case: Table created by external tool (direct SQL) → not auto-registered. Dis
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Table created by external tool (direct SQL) → not auto-registered. Discovered on next catalog page load via information_schema scan.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-006: Import CSV → table appears in catalog automatically
**Given:** The feature and dependencies are available.
**When:** Tester performs: Import CSV → table appears in catalog automatically
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-007: save_table() from code → table appears in catalog
**Given:** The feature and dependencies are available.
**When:** Tester performs: save_table() from code → table appears in catalog
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-008: Connector import creates a new table → new catalog entry created
**Given:** The feature and dependencies are available.
**When:** Tester performs: Connector import creates a new table → new catalog entry created
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: Derived table replacement, if approved later → catalog entry updated, not duplicated
**Given:** The feature and dependencies are available.
**When:** Tester performs: Derived table replacement, if approved later → catalog entry updated, not duplicated
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
