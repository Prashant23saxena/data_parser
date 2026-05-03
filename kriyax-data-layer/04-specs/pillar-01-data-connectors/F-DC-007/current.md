# Spec — F-DC-007: Incremental/delta sync

**Version:** v2
**Status:** FROZEN
**Last updated:** 2026-05-02
**Pillar:** pillar-01-data-connectors
**Feature ref:** F-DC-007
**Dependencies:** F-DC-006

## Summary
For Odoo connections, fetch only new or modified records since the last sync. Uses a cursor field (e.g., write_date) to detect changes. Upserts into existing table.

## Inputs
| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| connection | saved connection | yes | — | valid Odoo connection |
| table_name | string | yes | — | must be an existing table from a previous F-DC-006 fetch |
| cursor_field | string | no | write_date | must be a date/datetime field on the model |

## States

### ready
Shows last sync timestamp, record count since last sync (estimated). "Sync Now" button.

### syncing
Fetching records where cursor_field > last_sync_timestamp. Progress: "Syncing… {{count}} new/updated records."

### upserting
Writing fetched records to existing table. Upsert on primary key (Odoo's `id` field). New rows inserted, existing rows updated.

### success
Sync complete. Message: "Synced {{count}} records ({{inserted}} new, {{updated}} updated). Last sync: {{timestamp}}."

### error:sync-failed
Fetch or upsert failed.
Message: "Sync failed: {{error}}. Data is unchanged."

### no-changes
No new/modified records since last sync.
Message: "Already up to date. No changes since {{last_sync}}."

## Transitions
| From | To | Trigger | Side effects |
|---|---|---|---|
| ready | syncing | user clicks Sync Now, or pipeline triggers | fetch begins |
| syncing | upserting | records fetched | temp data stored |
| syncing | no-changes | 0 records match cursor filter | none |
| syncing | error:sync-failed | API error | none |
| upserting | success | DB upsert complete | last_sync_timestamp updated |
| upserting | error:sync-failed | DB error | data unchanged |

## Edge cases
- First sync on a table that was full-refreshed → cursor starts from table's last fetch timestamp
- Odoo record deleted at source → NOT detected by incremental (known limitation, document it)
- Clock skew between Odoo server and local → use Odoo's server time, not local time
- Cursor field doesn't exist on model → error before sync: "Field '{{cursor_field}}' not found"

## Acceptance checklist
- [ ] Modify a record in Odoo → sync picks it up, updates in local table
- [ ] Add a record in Odoo → sync inserts it
- [ ] No changes → "Already up to date" message
- [ ] Pipeline triggers sync → works without manual interaction

---
*Frozen on: 2026-05-02*
