---
title: "SongBlend"
date: 2026-08-15
type: docs
draft: false
tags: ["AI", "Music", "Audio", "Python", "React", "Software Product"]
---

## SongBlend — AI Music Region Blending Workstation

SongBlend is a full-stack, browser-based audio workstation for decomposing AI-generated songs
into musical regions and blending them into seamless new compositions. AI song generators
(Suno and friends) are great at *generating* but lousy at *editing* — you cannot tell them to
drop the second chorus, swap the bridge for a different one, or remix the intro and outro. That
is exactly the gap SongBlend fills.

![SongBlend](/projects/websites/images/songblend-1.png)

SongBlend handles all the audio science — BPM detection, key analysis, phrase segmentation,
tempo stretching, and intelligent crossfading — so you can focus on creative curation.

### Features

- **Smart Region Detection** — automatically segments songs into musical phrases, with BPM,
  key, and energy analysis.
- **Visual Canvas** — drag-and-drop interface for arranging regions into new compositions.
- **Intelligent Joins** — auto-selected blend modes (hard cut, crossfade, tempo stretch, pitch
  shift) based on compatibility scores, with manual override.
- **Live Preview** — in-browser playback with caching for instant re-preview.
- **Compatibility Scoring** — BPM, key, and timbre analysis to score region transitions, so the
  best join is usually the one the tool picks.
- **Project Management** — save and load multi-canvas projects with all settings preserved.
- **Professional Export** — high-quality WAV rendering with beat-matched joins.

### How it works

1. Upload WAV files — AI-generated songs from Suno work great.
2. The app automatically analyzes and segments regions (verse, chorus, bridge), each with its
   detected BPM, key, and energy.
3. Drag regions onto the canvas to build your new song.
4. Preview joins and adjust blend settings.
5. Export your final composition.

### Blend modes

SongBlend automatically selects the best blend mode based on region compatibility:

- **Hard Cut** — clean cut at zero-crossing (for similar BPM/key).
- **Crossfade** — equal-power crossfade (for smooth transitions).
- **Beat Match** — tempo-stretched join (for BPM differences).
- **Pitch Shift** — key-adjusted crossfade (for key mismatches).
- **Silence Gap** — brief silence (for dramatic transitions).

All modes can be manually overridden in the join settings panel.

### Tech stack

- **Frontend**: React 18 + Vite + TypeScript, shadcn/ui, Zustand, WaveSurfer.js, Tone.js,
  dnd-kit.
- **Backend**: FastAPI (Python 3.11+), librosa for audio analysis (BPM, key, spectral
  features), pyrubberband for time-stretching and pitch-shifting, pydub for mixing and export.

All audio processing happens server-side for accuracy, and rendered previews are cached
in-memory so replaying a join is instant.

### Status

**Deployment is pending.** The app is dockerized and ready to deploy (Nginx serving the
pre-built frontend and proxying `/api/*` to the FastAPI backend with a named volume for data
persistence); a deployment target is being finalized.

Code: [github.com/abulka/songblend](https://github.com/abulka/songblend) (private for now)
