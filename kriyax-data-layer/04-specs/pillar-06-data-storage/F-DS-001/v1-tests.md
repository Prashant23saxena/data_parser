# Test Scenarios — F-DS-001: Backing database setup

**Spec version:** v1  
**Generated:** 2026-05-02  
**Status:** FROZEN  
**Total scenarios:** 11  
**Spec file:** 04-specs/pillar-06-data-storage/F-DS-001/current.md

## How to use

Each scenario uses Given/When/Then and observable checks. These tests are version-locked to the frozen L4 spec.

## Happy path

### TS-001: Backing database setup primary success path
**Given:** The app is configured and dependencies for F-DS-001 are available.
**When:** The user completes the main Backing database setup action with valid inputs.
**Then:** The feature reaches its success/loaded state and shows the expected result.

**Verify:**
- [ ] Expected success message or visible result appears.
- [ ] No error state is shown.
- [ ] Related side effects in the spec occur.

## Validation

### TS-002: Backing database setup rejects invalid or missing required input
**Given:** The user is on the Backing database setup surface.
**When:** A required or invalid input is submitted.
**Then:** The action is blocked with a clear validation message.

**Verify:**
- [ ] No database/external mutation occurs.
- [ ] The user can correct the input and retry.

## Error states

### TS-003: F-DS-001 handles error:connection
**Given:** The feature can be forced into error:connection.
**When:** The triggering failure occurs.
**Then:** The error:connection state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

### TS-004: F-DS-001 handles error:migration
**Given:** The feature can be forced into error:migration.
**When:** The triggering failure occurs.
**Then:** The error:migration state is visible and recoverable.

**Verify:**
- [ ] Exact error copy is visible where specified.
- [ ] User input/configuration is preserved where practical.

## Edge cases

### TS-005: F-DS-001 edge case: DuckDB is simplest local default; Postgres remains option if multi-pro
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: DuckDB is simplest local default; Postgres remains option if multi-process/server needs demand it.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-006: F-DS-001 edge case: Database must be available whenever app is running.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Database must be available whenever app is running.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

### TS-007: F-DS-001 edge case: Schema migrations are idempotent.
**Given:** The system is in a state where this edge case can happen.
**When:** The edge case occurs: Schema migrations are idempotent.
**Then:** The feature handles it according to the spec.

**Verify:**
- [ ] No crash or corrupt state.
- [ ] A clear warning/error/result is displayed.

## Acceptance

### TS-008: App starts with DB ready.
**Given:** The feature and dependencies are available.
**When:** Tester performs: App starts with DB ready.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-009: Catalog can read metadata.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Catalog can read metadata.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-010: Connector can create table.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Connector can create table.
**Then:** The observable result matches the acceptance item.

**Verify:**
- [ ] Result is visible to user.
- [ ] Any persisted state can be verified after refresh.

### TS-011: Failure shows actionable setup error.
**Given:** The feature and dependencies are available.
**When:** Tester performs: Failure shows actionable setup error.
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
