---
title: "Bookmark Super Manager"
date: 2026-09-04
type: docs
draft: false
tags: ["Web App", "Chrome Extension", "TypeScript", "Local-first", "Software Product"]
---

## Bookmark Super Manager — local-first bookmark manager & Chrome extension

A fast, local-first browser bookmark viewer and manager: sidebar tree, search, drag &
drop, duplicate detection, a link checker, and multiple bookmark files open as tabs.

![Bookmark Super Manager](/projects/websites/images/bookmark-super-manager.png)

**Nothing is uploaded.** Everything runs locally in your browser — bookmarks live in
your browser's own IndexedDB and never leave your machine.

There are two ways to use the same manager:

- **Standalone web app** — deployed automatically at
  [bookmarks-super-manager.netlify.app](https://bookmarks-super-manager.netlify.app/).
  Open it and drop in a bookmark `.html`/`.json` export. Your live bookmarks are never
  touched.
- **Chrome extension** — edit your **real** Chrome bookmarks in a manager tab, then push
  changes back with one **Apply to Chrome** button. Grab the latest release zip from the
  **[Releases page](https://github.com/abulka/bookmarks-super-manager/releases)**: unzip it,
  then `chrome://extensions` → Developer mode → **Load unpacked** → the extracted folder.
  No compile needed.

### Features

- Netscape-HTML import (Chrome / Safari / Edge / Firefox) and Firefox JSON import
- Chrome-compatible HTML export
- Sidebar tree with drag & drop, cut / copy / paste, multi-select
- Full-text and folder search with smart term matching
- Duplicate detection with an interactive "keep newest" view
- Link checker and dead-bookmark finding, per-folder link/dead counts
- Tabs — open, merge, and switch between bookmark files
- Undo across reorganisation actions

### The Chrome extension, done safely

The live tab is never persisted; Apply shows a reviewable diff and confirms deletes,
refuses to run if Chrome changed elsewhere since the tab loaded, and re-diffs after
writing. Chrome's permanent top-level folders are never deleted. Sideloaded extensions
can't silently self-update on branded Chrome, so the extension checks the GitHub releases
API on startup (and hourly) and nags once per version with a "Get vX.Y.Z" link straight
to the latest release.

Code: [github.com/abulka/bookmarks-super-manager](https://github.com/abulka/bookmarks-super-manager) · MIT
Deployment: [bookmarks-super-manager.netlify.app](https://bookmarks-super-manager.netlify.app/) · Releases: [github.com/abulka/bookmarks-super-manager/releases](https://github.com/abulka/bookmarks-super-manager/releases)