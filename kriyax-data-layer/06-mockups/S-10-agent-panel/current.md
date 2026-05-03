# Mockup — S-10: Agent Panel

**Version:** v2
**Status:** FROZEN
**Last updated:** 2026-05-02
**Fidelity:** detailed low / ASCII wireframe
**Files:**
- `v2-primary.txt` — generated-code and self-correction state

## Purpose

Show how the schema-aware agent works beside the Python editor: chat, context, code generation, insert actions, follow-ups, and error self-correction.

## Primary layout elements

- Docked panel inside Code Workspace.
- Context summary and manage-context control.
- User prompt and agent response.
- Generated code block.
- Insert/replace controls.
- Self-correction card using traceback from the editor output.
- Follow-up input.

## Feature coverage

| Feature | Visible treatment |
|---|---|
| F-AL-001 | Chat interface. |
| F-AL-002 | Loaded schema context. |
| F-AL-003 | Generated Python/pandas code. |
| F-AL-004 | Insert and replace actions. |
| F-AL-005 | Error self-correction panel. |
| F-AL-006 | Follow-up input. |
| F-CW-005 | Traceback used as correction input. |

## Revision flags raised

- None.

---
*Frozen on: 2026-05-02*
