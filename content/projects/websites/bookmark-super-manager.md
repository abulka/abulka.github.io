---
title: "Bookmark Super Manager"
date: 2026-09-04
type: docs
draft: false
aliases: ["/blog/2026/09/04/bookmark-super-manager/"]
tags: ["Web App", "Chrome Extension", "TypeScript", "Local-first", "Software Product"]
---

## Bookmark Super Manager — local-first bookmark manager & Chrome extension

A fast, local-first browser bookmark viewer and manager: sidebar tree, search, drag &
drop, duplicate detection, a link checker, and multiple bookmark files open as tabs.

![Bookmark Super Manager](/projects/websites/images/bookmark-super-manager.png)

**Nothing is uploaded.** Everything runs locally in your browser — bookmarks live in
your browser's own IndexedDB and never leave your machine.

### Two ways to use it, one manager

The same manager UI powers both modes — the only difference is *where* bookmarks come
from and *how* changes leave:

| | Standalone web app | Chrome extension |
| --- | --- | --- |
| What it is | A website you open in any browser | An MV3 extension for your live Chrome bookmarks |
| Bookmarks | Exported **files** (import → organise → export) | **Live** `chrome.bookmarks`, edited in place |
| Touches your real bookmarks? | **No** | **Yes** — that's the point |

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

### Search that actually understands you

Press **⌘F** / **Ctrl+F** and type in the omnibox to search names, URLs and folder names.
Results are grouped by their location in the tree. Smart term matching applies to every
search box:

- **Space-separated terms match everything** — `pi code` finds items matching *both* `pi`
  *and* `code`.
- **Terms match the title as a substring** — `wik` matches `Wikipedia` (names only;
  buried-in-URL terms don't create scan-noise).
- **Double-quoted terms are exact whole words** — `"pi"` matches the word `pi` only, and
  whole-word terms also look in the URL.

So `git "branch"` finds an item whose name contains `git` (anywhere) and that somewhere
contains the whole word `branch` (name or URL).

### The Chrome extension, done safely

Editing real Chrome bookmarks in place needs more respect than a normal app, so the
extension plays it safe:

- **Mobile bookmarks** get their own root section, exactly as in Chrome's Bookmark Manager.
- The live tab is never persisted; **Apply** shows a reviewable diff and confirms deletes,
  refuses to run if Chrome changed elsewhere since the tab loaded, and re-diffs after
  writing. Chrome's permanent top-level folders (Bookmarks bar / Other bookmarks /
  Mobile bookmarks) are never deleted.
- Sideloaded extensions can't silently self-update on branded Chrome, so the extension
  checks the GitHub releases API on startup (and hourly) and nags once per version with a
  "Get vX.Y.Z" link straight to the latest release. That version check is the only network
  call it makes.

### A note on link checking

A browser only sees cross-origin network failures, not HTTP status codes. For real statuses
the app uses a small local proxy during development. On static hosting the proxy is absent
and link-checking falls back to network-level (DNS/TLS/connectivity) checks only — a
pragmatic trade-off of running the whole thing on static hosting with nothing server-side.

Code: [github.com/abulka/bookmarks-super-manager](https://github.com/abulka/bookmarks-super-manager) · MIT
Deployment: [bookmarks-super-manager.netlify.app](https://bookmarks-super-manager.netlify.app/) · Releases: [github.com/abulka/bookmarks-super-manager/releases](https://github.com/abulka/bookmarks-super-manager/releases)
