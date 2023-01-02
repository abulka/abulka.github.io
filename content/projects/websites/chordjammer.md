---
title: "Chord Jammer"
date: 2022-02-14
type: docs
draft: false
tags: ["Music", "Software Product", "Composition", "Chords", "MIDI"]
---

A midi web app that lets you play chords with 1 finger in the left hand
and jam safely in the right hand. 
As you change chords, the rh notes are filtered so you always play good sounding notes.

![screenshot](/projects/websites/images/chord-jammer-2.png)

Try it out at [Chord Jammer](https://chordjammer.web.app/)

Code

    ~/Devel/midi-play/webmidijs-play

### Sample config

```javascript
export let project = {
    chords: {
        'C3': {
            lhchord: Em7Chord,
            rhnotes: EmScaleMelodic,
        },
        'D3': {
            lhchord: AmAdd9Chord,
            rhnotes: EmScaleNatural,
        },
        'E3': {
            lhchord: CM9Chord,
            rhnotes: EmScaleNatural,
        },
        'F3': {
            lhchord: BmAdd11ChordInversion1,
            rhnotes: EmScaleNatural,
            rhnotes2: EmScaleHarmonic,
            rhnotes3: EmBlues,
        }
    }
}
```
### Single finger Chords

With the project config above

- Play C3 to trigger chord `Em7Chord` and jam in default scale `EmScaleMelodic`
- Play D3 to trigger chord `AmAdd9Chord` and jam in default scale `EmScaleNatural`
- Play E3 to trigger chord `CM9Chord` and jam in default scale `EmScaleNatural`
- Play F3 to trigger chord `BmAdd11ChordInversion1` and jam in default scale `EmScaleNatural`

Jamming notes are `G3` to `C5` and are filtered to be in the default scale for that chord.

### Scale Switching whilst playing

You can switch to e.g. the pentatonic scale for the current chord by pressing D#4.  Switch back to the default scale by pressing C#4.  

Here is a list of *modifier keys* and what they do to the rh scale:

- C#4 default scale, `rhnotes` in config
- D#4 `rhnotes2` scale in config
- F#4 `rhnotes3` scale in config
- G#4 transpose rh scale by `options.transposeUpAmount` semitones
- A#4 transpose rh scale down by `options.transposeDownAmount` semitones

You can customise the transposition amounts for a given project via config e.g.

```javascript
export let project = {
    chords: {...},
    options: {
        transposeUpAmount: 4,
        transposeDownAmount: -2,
    }
}
```

Potentially other customisations via config will be supported in the future:
- Being able to specify which scales to switch to, instead of pentatonic and blues.
- Being able to change what the modifier keys actually are (unlikely).

### Left hand black key modifiers

The octave containing the left hand chord trigger notes will have its black keys used as modifiers.
The `C#` acts as a SHIFT, so

  - `C#` hold down to engage SHIFT mode
  - `D#` cmdSetScaleFiltering(false)
  - `F#` cmdSetScaleFiltering(true)
  - `G#` transposeChord down a semitone
  - `A#` transposeChord up a semitone
  - SHIFT `D#` stopAllNotes()
  - SHIFT `F#` scaleFilteringModificationSticky toggle
  - SHIFT `G#` reset chord transpose - todo
  - SHIFT `A#` reset chord transpose - todo

### Config customisations supported

```js
export let project = {
    chords: {...},
    options: {...},

    splitNote: 'C3',         // Where the root note is (see explanation below)
    rhStartOctave: 3,        // To which octave to start mapping notes to
}
```

### Technologies
| Description | Technology |
| --- | --- |
| MIDI | [WebMidi.js](https://webmidijs.org/docs/) |
| GUI | [webaudio-controls](http://g200kg.github.io/webaudio-controls/docs/index.html) |
| Scales and chords | [tonaljs](https://github.com/tonaljs/tonal) - A functional music theory library for Javascript. |

