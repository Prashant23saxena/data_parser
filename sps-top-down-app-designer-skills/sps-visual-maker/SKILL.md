---
name: sps-visual-maker
description: Generate ASCII, HTML, or image visuals on demand for app design work — pillar trees, feature dependency graphs, state diagrams, sitemaps, user flow charts, screen mockups, and story-style freeze-gate summaries. Use when the user asks for a visual, diagram, flowchart, tree, mind-map, sitemap, or mockup, or when a vertical layer skill (sps-vision-definer, sps-pillar-mapper, sps-feature-lister, sps-feature-detailer, sps-screen-planner, sps-mockup-painter, sps-build-planner) needs to produce a visual artifact at a freeze gate. Asks the user which format (ASCII, HTML, image) before generating, with sensible defaults per visual type. Saves output to the project's visuals/ folder. Horizontal utility — callable standalone or embedded in other skills.
---

# Visual Maker

A horizontal utility skill that produces visuals for the top-down app-design workflow. Saves output into the project's `visuals/` folder.

## When this skill runs

**Standalone** — user asks "make me a tree of these pillars" or "show this as a flowchart".

**Embedded** — a vertical skill (e.g. `sps-pillar-mapper`) calls it after producing a spec, to generate the visual that accompanies that layer's freeze gate.

## Visual types supported

Each type has a default format suggestion. The skill always asks the user to confirm or change.

| Type | Used at layer | Default format | Alternate formats |
|---|---|---|---|
| `pitch-box` | L1 vision | ASCII | HTML |
| `pillar-tree` | L2 pillars | ASCII | HTML, image |
| `feature-dep-graph` | L3 features | ASCII | HTML |
| `state-diagram` | L4 specs | ASCII | HTML, image |
| `sitemap` | L5 screens | ASCII | HTML |
| `flow-chart` | L5/L6 user flows | ASCII | HTML, image |
| `mockup` | L6 mockups | image | HTML |
| `story-summary` | any freeze gate | ASCII | HTML |
| `build-timeline` | L7 build plan | ASCII | HTML |

## Format choice prompt

Before generating, ask:

> Which format? (ASCII / HTML / image / skip) — default for {type} is **{default}**.

If embedded, the calling skill may pre-specify the format and skip this prompt.

## Inputs

- `type` — one of the visual types above
- `format` — ascii / html / image / ask
- `content` — structured data describing what to visualize (varies by type, see below)
- `output_path` — where to save (defaults to `visuals/{layer}-{type}-v{N}.{ext}`)
- `title` — display title

## Content shape per type

### pitch-box

```
{
  "name": "App name",
  "promise": "One-line pitch",
  "user": "Who uses it",
  "non_goals": ["...", "..."]
}
```

ASCII rendering:
```
+------------------------------------------+
| {name}                                   |
+------------------------------------------+
| For: {user}                              |
| Promise: {promise}                       |
| Not: {non_goals joined by ", "}          |
+------------------------------------------+
```

### pillar-tree

```
{
  "app": "App name",
  "pillars": [
    {"name": "Onboarding", "purpose": "..."},
    {"name": "Content", "purpose": "..."}
  ]
}
```

ASCII rendering:
```
{app}
├── Pillar 1: Onboarding
│   └── {purpose}
├── Pillar 2: Content
│   └── {purpose}
└── Pillar 3: ...
```

### feature-dep-graph

```
{
  "pillar": "Pillar name",
  "features": [
    {"id": "F-001", "name": "Sign up", "depends_on": []},
    {"id": "F-002", "name": "Verify email", "depends_on": ["F-001"]}
  ]
}
```

ASCII rendering: list each feature, show arrows for dependencies.

```
[F-001] Sign up
   └─→ [F-002] Verify email
        └─→ [F-003] Complete profile

[F-004] Forgot password (independent)
```

### state-diagram

```
{
  "feature": "Feature name",
  "states": ["empty", "loading", "loaded", "error"],
  "transitions": [
    {"from": "empty", "to": "loading", "trigger": "fetch"},
    {"from": "loading", "to": "loaded", "trigger": "success"},
    {"from": "loading", "to": "error", "trigger": "failure"}
  ]
}
```

ASCII rendering:
```
[empty] --fetch--> [loading] --success--> [loaded]
                       |
                    failure
                       v
                    [error]
```

### sitemap

```
{
  "screens": [
    {"id": "S-01", "name": "Home", "children": ["S-02", "S-03"]},
    {"id": "S-02", "name": "Detail", "children": []}
  ]
}
```

ASCII tree of screens.

### flow-chart

```
{
  "title": "Sign-up flow",
  "steps": [
    {"id": 1, "label": "Land on home"},
    {"id": 2, "label": "Click sign up"},
    {"id": 3, "label": "Enter email"},
    {"id": 4, "label": "Verify", "branches": [
      {"label": "success", "to": 5},
      {"label": "fail", "to": 3}
    ]}
  ]
}
```

ASCII boxes-and-arrows.

### mockup

For mockups (L6), default is **image**. Generate via image generation if available; otherwise produce HTML wireframes.

```
{
  "screen_name": "Home",
  "elements": [
    {"type": "header", "text": "Welcome"},
    {"type": "button", "text": "Get started"},
    {"type": "list", "items": ["..."]}
  ],
  "style_notes": "Minimal, dark mode"
}
```

If image: use the image-search or image-generation tools available.
If HTML: produce a self-contained HTML file with simple CSS.
If ASCII: produce a wireframe like:
```
+--------------------------------+
| [Welcome]                      |
|                                |
|     [ Get started ]            |
|                                |
| - Item 1                       |
| - Item 2                       |
+--------------------------------+
```

### story-summary

A freeze-gate visual: tells the story of what was just defined. Used at the end of every layer.

```
{
  "layer": "L2 Pillars",
  "headline": "Defined 4 pillars for the app",
  "items": ["Onboarding", "Content creation", "Discovery", "Settings"],
  "next": "Move to L3: feature lists per pillar"
}
```

ASCII rendering:
```
=================================================
  FREEZE GATE — L2 Pillars
=================================================

  ✓ Defined 4 pillars for the app

    1. Onboarding
    2. Content creation
    3. Discovery
    4. Settings

  → Next: L3, feature lists per pillar

=================================================
```

### build-timeline

```
{
  "phases": [
    {"name": "Phase 1: Core", "items": ["F-001", "F-002"], "estimate": "2 weeks"},
    {"name": "Phase 2: Discovery", "items": ["F-010", "F-011"], "estimate": "1 week"}
  ]
}
```

ASCII Gantt-ish or numbered list.

## Process

1. Receive inputs (type, content, format preference).
2. If format is `ask`, prompt user.
3. Generate the visual in the chosen format.
4. Determine output path: if not provided, derive from layer + type + version. Use `visuals/{NN}-{type}-v{N}.{ext}` where NN is the layer number (01, 02, ...) and ext is `txt`, `html`, or `png`.
5. If a previous version exists at the same path, increment the version number.
6. Write the file.
7. Show the visual inline to the user (for ASCII), or for HTML/image confirm the path and offer to open it.
8. Return the file path.

## Output paths convention

```
project-root/visuals/
├── 01-pitch-box-v1.txt
├── 02-pillar-tree-v1.txt
├── 02-pillar-tree-v2.txt          (if revised)
├── 03-feature-dep-pillar-01-v1.txt
├── 04-state-feature-001-v1.txt
├── 05-sitemap-v1.txt
├── 06-mockup-screen-01-home-v1.png
├── 07-build-timeline-v1.txt
├── freeze-L1-story-v1.txt
├── freeze-L2-story-v1.txt
└── ...
```

## HTML rendering notes

When generating HTML, produce a single self-contained file (inline CSS, no external dependencies). Style should be clean and minimal — black/white with subtle accent. The user will view it in a browser.

## Image rendering notes

When the user picks `image`:
- For mockups (L6): use image generation if available with a wireframe-style prompt.
- For diagrams: try mermaid-based rendering (HTML with a mermaid CDN), or recommend the user accept HTML/ASCII.

## Critical rules

- **Always save to disk** — never just print the visual without saving. The artifact is the point.
- **Always version** — never overwrite an existing visual; create v2, v3, etc.
- **Ask format unless caller specified** — ASCII is the default but user may want HTML for sharing.
- **Stay within the project's `visuals/` folder** — don't scatter files.
