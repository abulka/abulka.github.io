---
title: "Unjazz"
date: 2026-08-15
type: docs
draft: false
tags: ["Music", "React", "Software Product", "Javascript"]
---

## Unjazz — My Music Streaming Platform

To host my musical compositions, I built a React-based music streaming platform. It features a
SoundCloud-inspired UI, high-quality audio playback with Howler.js, and a neat trick: the audio
itself is hosted on **GitHub Releases**, which gives unlimited bandwidth for public repos and
bypasses Git LFS size limits entirely. The whole site runs on GitHub Pages — low cost and easy
to maintain.

![Unjazz player](/projects/websites/images/unjazz-1.png)

Try it at [abulka.github.io/unjazz](https://abulka.github.io/unjazz)

### Features

- **SoundCloud-style UI** with waveform visualizations.
- **High-quality audio playback** using Howler.js.
- **Media Session API** integration — lock screen controls, AirPlay, CarPlay.
- **Responsive design** for desktop and mobile.
- **Fast loading** with pre-generated waveforms (rendered at build time, so there is no 2–5
  second wait on playback start).
- **Album organization** with automatic metadata extraction from ID3 tags.
- **Playlist support** with continuous playback.
- **Keyboard shortcuts** for playback control.

### How it's built

- **Audio files** are uploaded as GitHub Release assets — no Git LFS bandwidth limits, 2 GB per
  file, unlimited bandwidth for public repos.
- **The website** is a static React application (Vite build) deployed to GitHub Pages, with
  track metadata (`tracks.json`) and waveform data committed to the repo.
- **A metadata generator** script reads the ID3 tags from your MP3s and produces the track
  listing, handles album reorganization (renaming assets, cleaning up orphans on the release),
  and can upload new audio straight to a release.

### Safari compatibility (CORS proxy)

Safari has strict requirements for audio streaming (CORS and Range headers) that GitHub
Releases doesn't always satisfy by default — without help you can hit "Media cannot be played"
or be unable to seek. The fix is a tiny **Cloudflare Worker** that forwards the request to
GitHub with the correct CORS/partial-content headers, keeping playback smooth on iPhones and in
Safari on the Mac.

### Keyboard shortcuts

| Key | Action |
| --- | --- |
| `Space` | Play / Pause |
| `←`/`→` | Seek backward / forward |
| `↑`/`↓` | Volume up / down |
| `N` | Next track |
| `P` | Previous track |

### Tech stack

React + Vite, Howler.js for audio, WaveSurfer-style waveform rendering, Tailwind CSS for
styling, a Cloudflare Worker for the Safari CORS proxy, and GitHub Pages + GitHub Releases for
deployment.

Code: [github.com/abulka/unjazz](https://github.com/abulka/unjazz)
