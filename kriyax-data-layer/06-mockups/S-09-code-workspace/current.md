# Mockup — S-09: Code Workspace

**Version:** v2
**Status:** FROZEN
**Last updated:** 2026-05-02
**Fidelity:** detailed low / ASCII wireframe
**Files:**
- `v2-primary.txt` — Python editing and successful output state

## Purpose

Provide the main Python/pandas transformation surface with table discovery, editor, execution output, DataFrame preview, saved scripts, derived table persistence, and agent access.

## Backend behavior assumption

The editor saves user code as a real `.py` file in the project workspace. Running the script uses the laptop's configured Python through a thin app wrapper that provides helper functions like `load_table()` and `save_table()`. This keeps the first implementation bare-bones: no Jupyter dependency, no custom Python engine, and no hidden transform format.

## Primary layout elements

- Table/sidebar browser with insert-load-code actions.
- Python editor.
- Agent dock entry.
- Output panel.
- DataFrame preview.
- Save script and save-as-table actions.

## Feature coverage

| Feature | Visible treatment |
|---|---|
| F-CW-001 | Python code editor. |
| F-CW-002 / F-CW-003 | Available tables and insert load code. |
| F-CW-004 | Save DataFrame as table. |
| F-CW-005 | Output and traceback area. |
| F-CW-006 | Save script and pipeline creation path. |
| F-SC-001 / F-SC-002 / F-SC-005 | Table registry, columns, and preview. |
| F-DS-003 | Persist derived table success path. |

## Revision flags raised

- None.

---
*Frozen on: 2026-05-02*
