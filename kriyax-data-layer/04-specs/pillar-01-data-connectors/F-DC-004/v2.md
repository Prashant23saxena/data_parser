# Spec — F-DC-004: Configure Odoo connection

**Version:** v2
**Status:** FROZEN
**Last updated:** 2026-05-02
**Pillar:** pillar-01-data-connectors
**Feature ref:** F-DC-004
**Dependencies:** none

## Summary
User enters Odoo instance URL, database name, and API key (or username/password). System tests the connection via XML-RPC and reports success/failure.

This connector should cover the broad Odoo surface needed for real client data work, not only a narrow demo path. Connection setup must support the downstream needs of model browsing, field browsing, full fetch, incremental sync, and scheduled pipelines.

## Inputs
| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| connection_name | string | yes | — | max 64 chars, unique among saved connections |
| odoo_url | string | yes | — | valid URL, must start with http:// or https:// |
| db_name | string | yes | — | non-empty |
| username | string | yes | — | non-empty |
| api_key | string | yes | — | non-empty, masked in UI |

## States

### form-empty
Empty form with fields for all inputs. "Test Connection" button disabled until all fields filled.

### testing
User clicked "Test Connection". Spinner: "Connecting to Odoo…"

### success
Connection verified. Shows: Odoo version, server info. "Save Connection" button enabled. Message: "Connected successfully to {{odoo_url}} (Odoo {{version}})."

### error:unreachable
Server not reachable (DNS, timeout, network).
Message: "Cannot reach {{odoo_url}}. Check the URL and your network connection."

### error:auth-failed
Authentication failed (wrong credentials).
Message: "Authentication failed. Check your username and API key."

### error:invalid-db
Database name not found on the Odoo instance.
Message: "Database '{{db_name}}' not found on this Odoo instance."

### saved
User clicked Save. Connection persisted. Message: "Connection '{{connection_name}}' saved."

## Transitions
| From | To | Trigger | Side effects |
|---|---|---|---|
| form-empty | testing | user clicks Test Connection (all fields filled) | XML-RPC call to /xmlrpc/2/common |
| testing | success | authenticate() returns uid | none |
| testing | error:unreachable | connection timeout/DNS failure | none |
| testing | error:auth-failed | authenticate() returns false | none |
| testing | error:invalid-db | DB not found error | none |
| success | saved | user clicks Save Connection | credentials persisted (encrypted at rest) |
| error:* | form-empty | user edits any field | none |

## Edge cases
- URL with trailing slash → strip it
- URL without protocol → prepend https://
- Self-signed SSL certificate → show warning, allow proceed
- API key with leading/trailing spaces → trim
- Connection name already exists → error: "A connection with this name already exists"

## Acceptance checklist
- [ ] Valid Odoo credentials → test succeeds, save works
- [ ] Wrong API key → error:auth-failed
- [ ] Wrong URL → error:unreachable
- [ ] Wrong DB name → error:invalid-db
- [ ] Saved connection appears in connection list (F-DC-008)
- [ ] Saved connection can be reused by model browsing, record fetch, incremental sync, and pipeline steps

---
*Frozen on: 2026-05-02*
