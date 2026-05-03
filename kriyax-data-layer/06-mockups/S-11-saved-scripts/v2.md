# Mockup — S-11: Saved Scripts

**Version:** v2
**Status:** FROZEN
**Last updated:** 2026-05-02
**Fidelity:** detailed low / ASCII wireframe
**Files:**
- `v2-primary.txt` — script list with selected detail

## Purpose

Let users find saved Python scripts, reopen them in the editor, rename or duplicate them, and use them as pipeline inputs.

## Backend behavior assumption

Each saved script maps to a physical `.py` file under the workspace `scripts/` folder plus metadata such as display name, last run, output table, and pipeline usage.

## Primary layout elements

- Searchable saved script table.
- Selected script metadata.
- Code preview.
- Open in workspace and create pipeline actions.
- Rename conflict state.

## Feature coverage

| Feature | Visible treatment |
|---|---|
| F-CW-006 | Saved scripts list, open, rename, duplicate. |
| F-PS-001 | Create pipeline from selected script. |

## Revision flags raised

- None.

---
*Frozen on: 2026-05-02*
