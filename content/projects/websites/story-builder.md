---
title: "Story Builder"
date: 2026-08-15
type: docs
draft: false
tags: ["AI", "Writing", "Vue", "Software Product", "Javascript"]
---

## Story Builder — Planning & Drafting Stories at Any Scale

Story Builder is a browser-based writing tool for planning and drafting stories at any scale —
a single sentence, a paragraph, a scene, a chapter, a full novel.

The app is built around a simple but powerful insight: **the principles of good storytelling
apply at every level of granularity**. Beats, structure, scene/sequel, character arc — you
should be able to apply a five-beat structure to a single sentence just as easily as to a
100,000-word novel, and zoom in and out between the two within a single project.

![Story Builder](/projects/websites/images/story-builder-1.png)

### The story tree

Your project is a **story tree** of container and leaf nodes. Each leaf can hold free-form
prose and/or a beat sheet, and container nodes hold structure. Multiple project types ship with
sensible default trees: Novel, Short Story, Flash Fiction (< 1000 words), Flash Fiction 2
(< 2000 words), and Series.

### Beat frameworks that nest

Beat frameworks can be applied at any node, at any scale:

- **Leaf frameworks** (apply to a single node):
  - **Micro-Cat (5-beat)** — Status Quo → Disruption → Escalation → Turn → New Normal
  - **3-Beat Paragraph** — Physical Action → Observation / Setting → Internal Reaction
  - **Snowflake (guided)** — Hook → Setup → Complication → Pressure / Choice → Reversal → Resolution
- **Structure frameworks** (generate a subtree of child leaves):
  - **Save the Cat (15 beats)** — book-level structure
  - **Hero's Journey (11 stages)** — book-level structure

The same framework can scaffold a single paragraph or an entire book — which is the whole point.

### Slot-based templating and the phrase pool

Every text slot in a beat framework is a `{{key}}` placeholder that resolves to the slot's value
at assembly time. On top of that, every slot has a **curated pool of evocative prose fragments**
behind a 🎲 randomize button, so hitting "random" repeatedly hands you fresh, well-written
phrasings to nudge in your own direction.

Entity slots resolve from your project itself: `{{protagonist}}`, `{{character}}`,
`{{location}}`, `{{next_location}}`. Pronoun tags (`{{pronoun}}`, `{{him}}`, `{{her}}`,
`{{his}}`, …) resolve to the grammatical form matching the protagonist's pronoun — so your
templates stay character-gender agnostic, and swapping the protagonist's pronoun updates the
whole assembled story.

### Characters, world building, and the Chapter Grid

- **Character management** — name, role (protagonist/antagonist/supporting/ai/other), pronoun,
  motivation, goal, conflict, epiphany, ghost, notes.
- **World building** — locations and factions.
- **Chapter Grid** — POV, location, plot event, subtext, and red-herring fields per node.

### Assembling the story

The assembled-story output renders the whole tree into flowing prose, with toggles for
headers, beat labels, plan meta, meta markers (`<!-- [META: Label] -->` become styled badges),
compact beats, and pronoun substitution. Templates are validated loosely: an unrecognised
`{{tag}}` passes through literally rather than silently breaking your custom template.

### Projects, persistence, and sharing

Multiple projects live in `localStorage` (with Pinia persistence), switchable from the toolbar.
Project JSON can be **exported / imported** for backup or sharing, and the app is fully
client-side.

### Tech stack

Vue 3 (Composition API) + TypeScript, Pinia with `pinia-plugin-persistedstate`, markdown-it
for story rendering, md-editor-v3 for prose editing, nanoid for stable IDs, Tailwind CSS for
styling, and Vite for build. There are no tests yet (on the roadmap).

### Status

An **AI settings panel** exists in the UI but no provider is wired in yet — so far this is a
human-powered writing tool. Build-and-run-yourself for now; hosted builds / GitHub Releases are
a TODO for the future. The roadmap also covers Chapter Grid enhancements and cross-project
templates/phrase pools.

Code: [github.com/abulka/story-builder](https://github.com/abulka/story-builder) (private for now)
