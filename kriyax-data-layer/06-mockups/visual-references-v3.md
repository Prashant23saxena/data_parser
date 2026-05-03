# L6 Visual References — v3

**Status:** REFERENCE
**Last updated:** 2026-05-02

## Purpose

These generated images are saved as visual design-language references for the app screens. They are useful for look, density, hierarchy, and overall product feel.

They are **not** pixel-perfect build requirements. The implementation contract remains:

1. `05-screens/current.md` for screen structure and navigation.
2. `06-mockups/{screen}/current.md` and `v2-primary.txt` for approved low-fidelity layout and behavior.
3. `04-specs/**/current.md` for feature states, validations, and edge cases.

## Design language notes

- Bare-bones internal data tool, not marketing UI.
- Desktop-first, dense but readable.
- White background, light gray dividers, compact tables, dark text.
- Subtle blue accents for primary actions.
- Red only for destructive/error states.
- Small-radius controls; avoid decorative gradients and hero-style graphics.
- Treat generated text as approximate; use frozen specs and wireframes for exact copy.

## Screen references

| Screen | Visual reference |
|---|---|
| S-01 Home / Operations Overview | `S-01-home/v3-visual-reference.png` |
| S-02 Connectors | `S-02-connectors/v3-visual-reference.png` |
| S-03 File Import Wizard | `S-03-file-import-wizard/v3-visual-reference.png` |
| S-04 Odoo Import Workspace | `S-04-odoo-import-workspace/v3-visual-reference.png` |
| S-05 Catalog | `S-05-catalog/v3-visual-reference.png` |
| S-06 Table Detail | `S-06-table-detail/v3-visual-reference.png` |
| S-07 Table Management Confirmation | `S-07-table-management-confirmation/v3-visual-reference.png` |
| S-08 Export Table Modal | `S-08-export-table-modal/v3-visual-reference.png` |
| S-09 Code Workspace | `S-09-code-workspace/v3-visual-reference.png` |
| S-10 Agent Panel | `S-10-agent-panel/v3-visual-reference.png` |
| S-11 Saved Scripts | `S-11-saved-scripts/v3-visual-reference.png` |
| S-12 Pipelines | `S-12-pipelines/v3-visual-reference.png` |
| S-13 Pipeline Run Detail | `S-13-pipeline-run-detail/v3-visual-reference.png` |
| S-14 Storage Settings | `S-14-storage-settings/v3-visual-reference.png` |

## Alternate references

- `S-03-file-import-wizard/v3-visual-calibration.png` — first calibration image generated before the full ordered set. Keep only as a secondary visual reference.

## Build guidance

During implementation, use these images to guide visual density, spacing, hierarchy, and component tone. Do not copy generated text blindly. Use the frozen specs and v2 wireframes for exact behavior, labels, validation, and navigation.
