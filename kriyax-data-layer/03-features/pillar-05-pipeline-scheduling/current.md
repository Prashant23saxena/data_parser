# Features — Pipeline & Scheduling

**Version:** v2
**Status:** FROZEN
**Last updated:** 2026-05-02
**Pillar:** pillar-05-pipeline-scheduling, from `02-pillars/current.md`

## Feature index

| ID | Name | Priority | Depends on |
|---|---|---|---|
| F-PS-001 | Create pipeline | must | F-CW-006 |
| F-PS-002 | Schedule pipeline | must | F-PS-001 |
| F-PS-003 | Manual trigger | must | F-PS-001 |
| F-PS-004 | Run history & status | must | F-PS-001 |
| F-PS-005 | Error notifications | should | F-PS-004 |
| F-PS-006 | Enable/disable pipeline | must | F-PS-001 |

## Features

### F-PS-001: Create pipeline

**Description:** Define a pipeline by selecting a saved Python script (from Pillar 3) as the execution step. Optionally add a connector sync step before it (e.g., refresh Odoo data, then run the cleaning script). Give the pipeline a name.

**Priority:** must

**Dependencies:** F-CW-006 (Code Workspace: Save & re-run scripts)

**Definition of done:** User can create a named pipeline, attach a saved script as the main step, optionally add a connector sync as a pre-step. Pipeline is saved and appears in a pipeline list.

**Cross-pillar links:** Pillar 3 (Code Workspace) — references saved scripts. Pillar 1 (Data Connectors) — optionally triggers a connector sync as pre-step.

---

### F-PS-002: Schedule pipeline

**Description:** Set a recurring schedule for a pipeline using cron expressions or simple presets (every hour, every day at 6am, every Monday). System runs the pipeline automatically at the scheduled time.

**Priority:** must

**Dependencies:** F-PS-001

**Definition of done:** User can set a schedule on any pipeline. Pipeline runs automatically at the configured times. Next scheduled run time is visible in the UI.

**Cross-pillar links:** none

---

### F-PS-003: Manual trigger

**Description:** Run any pipeline immediately on demand with a "Run now" button, regardless of its schedule. Useful for testing or one-off refreshes.

**Priority:** must

**Dependencies:** F-PS-001

**Definition of done:** User clicks "Run now" on any pipeline and it executes immediately. Run appears in history (F-PS-004) with status.

**Cross-pillar links:** none

---

### F-PS-004: Run history & status

**Description:** For each pipeline, show a list of past runs with timestamp, duration, status (success/failure), and error logs for failed runs. Most recent runs first.

**Priority:** must

**Dependencies:** F-PS-001

**Definition of done:** User clicks a pipeline and sees its run history. Each run shows start time, duration, and pass/fail status. Failed runs show the error traceback. History persists across sessions.

**Cross-pillar links:** none

---

### F-PS-005: Error notifications

**Description:** When a scheduled pipeline fails, surface it clearly — badge on the pipeline list, alert on the dashboard, and log the error. User doesn't have to check manually.

**Priority:** must

**Dependencies:** F-PS-004

**Definition of done:** Failed pipeline runs show a visual indicator (red badge, alert icon) in the pipeline list. User can see at a glance which pipelines have recent failures.

**Cross-pillar links:** none

---

### F-PS-006: Enable/disable pipeline

**Description:** Pause a scheduled pipeline without deleting its configuration. Disabled pipelines skip their schedule but can still be triggered manually.

**Priority:** should

**Dependencies:** F-PS-001

**Definition of done:** User can toggle a pipeline between enabled (running on schedule) and disabled (paused). Disabled pipelines are visually distinct. Re-enabling resumes the schedule.

**Cross-pillar links:** none

---

## Coverage map

| Pillar in-scope item | Covered by |
|---|---|
| Define pipeline steps (connector sync → transform → save) | F-PS-001 |
| Schedule runs (cron, interval) | F-PS-002 |
| Incremental/delta update support | Handled by Pillar 1 (F-DC-007) — pipeline triggers the sync which uses delta mode |
| Run history and status | F-PS-004 |
| Manual trigger option | F-PS-003 |
| Basic error notification | F-PS-005 |

---

*Frozen on: 2026-05-02*
