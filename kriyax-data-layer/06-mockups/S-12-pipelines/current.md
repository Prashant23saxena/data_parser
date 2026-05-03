# Mockup — S-12: Pipelines

**Version:** v2
**Status:** FROZEN
**Last updated:** 2026-05-02
**Fidelity:** detailed low / ASCII wireframe
**Files:**
- `v2-primary.txt` — populated pipeline list and selected configuration

## Purpose

Create, schedule, enable/disable, manually trigger, monitor, and diagnose pipelines from one screen.

## Backend behavior assumption

Pipelines do not store a second copy of transformation logic. A pipeline references either a saved `.py` script or an Odoo delta-sync definition, runs it through the scheduler using the same local Python execution wrapper, and stores run metadata/logs.

## Primary layout elements

- Pipeline summary cards.
- Pipeline list with enabled toggle and status.
- Selected pipeline configuration panel.
- Failure notification panel.
- Run history strip.

## Feature coverage

| Feature | Visible treatment |
|---|---|
| F-PS-001 | New pipeline and source selection. |
| F-PS-002 | Schedule configuration. |
| F-PS-003 | Manual run actions. |
| F-PS-004 | Run status and history. |
| F-PS-005 | Failure notifications and acknowledge. |
| F-PS-006 | Enable/disable toggle. |
| F-CW-006 / F-DC-007 | Script and Odoo delta pipeline sources. |

## Revision flags raised

- None.

---
*Frozen on: 2026-05-02*
