---
name: sps-idea-parker
description: Park stray ideas, questions, or features into the right backlog file during top-down app design. Use when the user says things like "park this for later", "add to backlog", "let's not build this now but remember it", "what about X — note it down", or when a tangent comes up while defining vision/pillars/features/specs/screens. Also use to view, promote, or drop backlog items. Operates per-layer: each layer (vision, pillars, features, specs, screens, mockups, build-plan) has its own backlog.md file. Horizontal utility — callable standalone or by other skills (sps-vision-definer, sps-pillar-mapper, sps-feature-lister, sps-feature-detailer, sps-screen-planner, sps-mockup-painter, sps-build-planner) in the sps-app-architect ecosystem.
---

# Idea Parker

A horizontal utility skill that manages per-layer backlogs for app-design projects scaffolded by `sps-project-builder`. Stray thoughts during brainstorming get captured without derailing the current freeze.

## When this skill runs

It runs in two modes:

**Standalone mode** — user explicitly invokes it: "park this idea", "show me the backlog for L3", "promote BL-002 into the active spec".

**Embedded mode** — another skill (a vertical layer skill) calls it during an interview when the user wants to defer something. The calling skill passes the scope (which backlog file).

## Backlog file locations

Every project scaffolded by `sps-project-builder` has these backlog files:

```
project-root/
├── 01-vision/backlog.md
├── 02-pillars/backlog.md
├── 03-features/pillar-XX-{name}/backlog.md       (created per pillar)
├── 04-specs/pillar-XX-{name}/feature-YYY-{name}/backlog.md  (created per feature)
├── 05-screens/backlog.md
├── 06-mockups/backlog.md
└── 07-build/backlog.md
```

If a backlog file does not exist when you need to write to it, create it using the template below.

## Backlog file format

Every backlog file follows this exact structure:

```markdown
# Backlog — {layer name + scope}

> Items parked during design. Active = under consideration. Promoted = pulled into a version. Dropped = decided against.

## Active

<!-- format: BL-XXX | title | type: feature/question/idea/edge-case | priority: parking/maybe/promote-soon | added: YYYY-MM-DD | notes -->

## Promoted

<!-- format: BL-XXX → moved to vN.md on YYYY-MM-DD -->

## Dropped

<!-- format: BL-XXX | reason -->
```

IDs are sequential per file (`BL-001`, `BL-002`, ...). Determine the next ID by reading the file and finding the highest existing number.

## Actions

The skill supports five actions. In standalone mode, ask the user which one. In embedded mode, the calling skill specifies it.

### 1. add

Append a new item to the `## Active` section.

**Required inputs:**
- `scope` — path to the backlog.md file (e.g. `03-features/pillar-02-content/backlog.md`)
- `title` — short description
- `type` — one of: `feature`, `question`, `idea`, `edge-case`
- `priority` — one of: `parking` (low), `maybe` (medium), `promote-soon` (high)
- `notes` — optional context

**Steps:**
1. Verify the file exists; if not, create it from the template.
2. Read existing items, determine next BL-XXX ID.
3. Append a new line under `## Active` in the format shown above.
4. Confirm to user: "Parked as BL-XXX in {scope}."

### 2. view

Display the contents of one backlog file or all of them.

**Inputs:**
- `scope` — either a specific path or the keyword `all`

**Steps:**
1. If specific scope: read that file, render Active / Promoted / Dropped sections clearly.
2. If `all`: walk the project root, find every `backlog.md`, render each grouped by layer. Show counts: "L1: 2 active, L3/pillar-01: 5 active, ..."

### 3. promote

Move an item from `## Active` to `## Promoted` and tell the user to integrate it into the next version of the spec. **This skill does NOT modify the spec file itself** — it only updates the backlog. The user (or the calling vertical skill) is responsible for adding the promoted content to the next `vN.md`.

**Inputs:**
- `scope` — path to the backlog.md file
- `id` — the BL-XXX to promote

**Steps:**
1. Read the file, find the line with that ID under `## Active`.
2. Remove it from Active. Add a line to `## Promoted` in the format `BL-XXX → moved to vN.md on {today}` (ask the user which version it's being promoted into if not provided).
3. Tell the user: "Marked BL-XXX as promoted. Remember to include it in vN+1 of the spec when you create the next version."

### 4. drop

Move an item from `## Active` to `## Dropped` with a reason.

**Inputs:**
- `scope`, `id`, `reason`

**Steps:**
1. Find the line under `## Active`, remove it.
2. Append `BL-XXX | {reason}` under `## Dropped`.
3. Confirm: "Dropped BL-XXX."

### 5. cross-layer-view

Special view: scan every backlog file across the project, list every active item, group by layer. Useful before a major freeze to see if anything parked should now be promoted.

**Steps:**
1. Walk project root, find all `backlog.md`.
2. For each, parse Active items.
3. Render as a single grouped report:
   ```
   ## L1 Vision
   - BL-001 | ... | priority: maybe
   ## L2 Pillars
   (none)
   ## L3 Features / pillar-01-onboarding
   - BL-001 | ... | priority: parking
   ...
   ```

## Standalone-mode interaction

When invoked directly by the user, follow this flow:

1. Detect the project root (look for `00-meta/freeze-status.md`). If none found, ask: "Which project? (provide path)".
2. Ask: "What do you want to do? (1) park a new idea, (2) view backlog, (3) promote an item, (4) drop an item, (5) see everything across all layers."
3. Ask follow-ups based on choice.
4. Execute the action.

## Embedded-mode interaction

When called by another skill (e.g. `sps-feature-lister` while interviewing the user about pillar 2):

1. The calling skill passes scope, plus partial info from the interview.
2. Ask only the missing fields (usually just `priority` and confirmation of `title`).
3. Execute and return a short confirmation that the calling skill can show inline.

## Critical rules

- **Never modify spec files (`vN.md`).** Only modify `backlog.md`.
- **Never delete entries.** Always move between sections (Active → Promoted / Dropped). The history is the value.
- **Always set the date** when promoting or adding (use today's date).
- **One ID space per file** — BL-001 in L1's backlog is unrelated to BL-001 in L3's backlog. They live in different files.
- **If a backlog file doesn't exist**, create it with the template. Don't error out.
