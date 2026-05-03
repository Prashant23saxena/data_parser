# Mockup — S-01: Home / Operations Overview

**Version:** v2
**Status:** FROZEN
**Last updated:** 2026-05-02
**Fidelity:** detailed low / ASCII wireframe
**Files:**
- `v2-primary.txt` — primary operational state

## Screen ref

Linked to `05-screens/current.md` → S-01

## Purpose

Make the home screen feel like an operations control panel for the Python-only data layer. The screen should let a user immediately answer:

- What needs my attention?
- What data work did I touch recently?
- Where do I start importing, transforming, scheduling, or debugging?

## Primary layout elements

- Persistent left sidebar with top-level destinations.
- Quick actions for the four likely entry tasks: file import, Odoo setup, code workspace, and catalog browsing.
- Pipeline health cards for running, successful, and failed runs.
- Active failure alert with direct review and acknowledge actions.
- Recent pipeline run table with status, time, duration, source/script, and action.
- Recent tables and recent scripts panels.
- Storage status strip with a link to storage settings.

## Feature coverage

| Feature | Visible treatment |
|---|---|
| F-PS-004 Run history & status | Pipeline health cards and recent pipeline runs table show running/success/failure status, timestamps, duration, source/script, and detail actions. |
| F-PS-005 Error notifications | Active failure alert and failed-count card surface scheduled run failures; acknowledge action is visible without deleting history. |

## State coverage

- **Primary:** Active workspace with one running pipeline, recent successes, and an active failure alert.
- **Empty workspace:** Quick actions remain; recent tables, scripts, and runs use first-use empty states.
- **Healthy:** Failure alert collapses into "No active failures"; failed count is zero.
- **Loading:** Health and recent work sections use skeleton rows; navigation and quick actions remain visible.
- **History unavailable:** Pipeline health section shows inline recoverable error with retry.

## Flow notes

- `Start file import` opens S-03.
- `Open Odoo setup` opens S-04.
- `Write Python` opens S-09.
- `Open catalog` opens S-05.
- `Review run` opens S-13.
- `Open saved scripts` opens S-11.
- `Open storage settings` opens S-14.

## Revision flags raised

- None. This mockup uses existing L5 screen paths and existing L4 feature states.

## Review questions for user

- Is this level of detail enough to imagine the screen?
- Should Home be more operational/status-heavy, or more shortcut/task-heavy?
- Should the active failure alert be this prominent on the landing screen?

---
*Frozen on: 2026-05-02*
