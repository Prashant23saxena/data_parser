# Spec — F-DC-005: Browse Odoo models & fields

**Version:** v2
**Status:** FROZEN
**Last updated:** 2026-05-02
**Pillar:** pillar-01-data-connectors
**Feature ref:** F-DC-005
**Dependencies:** F-DC-004

## Summary
After connecting to Odoo, user browses available models (res.partner, sale.order, etc.) and sees their fields with types. Uses Odoo's fields_get API.

The browser should expose as much Odoo structure as practical for v1: technical model names, human labels, field names, field labels, field types, required flags, read-only/computed hints when available, relation target models, and access errors. This is important because Kriya needs to understand unfamiliar client Odoo schemas before fetching data.

## Inputs
| Field | Type | Required | Default | Validation |
|---|---|---|---|---|
| connection | saved connection | yes | — | must be a valid, tested Odoo connection |
| search_query | string | no | — | filters model list by name |

## States

### loading-models
Fetching model list from Odoo. Spinner: "Loading Odoo models…"

### model-list
Searchable list of Odoo models. Each shows: technical name (e.g., res.partner), display name (e.g., Contacts), field count.

### model-detail
User clicked a model. Shows field list: field name, type (char, integer, many2one, etc.), required flag, description. "Select fields for import" checkboxes.

### error:connection-lost
Odoo connection dropped during browsing.
Message: "Lost connection to Odoo. Reconnect and try again."

## Transitions
| From | To | Trigger | Side effects |
|---|---|---|---|
| loading-models | model-list | models fetched | model list cached |
| model-list | model-detail | user clicks a model | fields_get call for that model |
| model-detail | (hand off to F-DC-006) | user selects fields and clicks Fetch | selected model + fields passed |
| * | error:connection-lost | XML-RPC call fails | none |

## Edge cases
- Odoo instance with 500+ models → paginated/virtual-scroll list, search is essential
- Model with 100+ fields → scrollable field list
- Relational fields (many2one, one2many, many2many) → show related model name and clearly mark how each relation can be fetched/imported
- Computed/read-only fields → show when Odoo metadata exposes this
- Required fields and field labels → show alongside technical names so both humans and the agent can understand the model
- User has no access to a model → Odoo returns permission error, show: "You don't have access to this model"
- Search with no results → "No models matching '{{query}}'"

## Acceptance checklist
- [ ] Connect to Odoo → model list loads
- [ ] Search "sale" → filters to sale.order, sale.order.line, etc.
- [ ] Click model → fields displayed with types
- [ ] Relational fields show target model information
- [ ] Field labels, technical names, required flags, and available read-only/computed hints are visible
- [ ] Select fields and click Fetch → hands off to F-DC-006

---
*Frozen on: 2026-05-02*
