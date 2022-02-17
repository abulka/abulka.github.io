---
title: "Websites"
linkTitle: "Web Apps"
weight: 20
---

## GitUML

UML visualisation for Git repositories _(website app)_.

Understand code quickly: Automatically generate UML class diagrams from source code residing in git repositories. Diagrams automatically update when you push code using git.

![point and click](https://www.gituml.com/static/home2/images_home/2017-10-19_09-43-34.bf679c329661.gif)

Visit [GitUML](http://www.gituml.com) now, create a free account and begin creating UML diagrams and documentation.


## Python to RPN

Check out [Python to RPN](http://www.pyrpn.atug.com) if you have an old vintage HP Calculator that you want to program in Python!  Impossible?  See also my blog post [How I used the Python AST capabilities to build a Python to Rpn converter](http://www.andypatterns.com/index.php/blog/ast-parsing-python-generate-hp-calculator-rpn/ "AST Parsing with Python to generate HP Calculator RPN").

I am pleased to announce the Python to HP42S RPN converter website is online.  
[www.pyrpn.atug.com](http://www.pyrpn.atug.com)   
  
![[Image: python_rpn_ui_01.png?raw=1]](https://www.dropbox.com/s/nqfq01xaxvi4xnv/python_rpn_ui_01.png?raw=1)  
  
You write code in a high level structured language (which happens to be Python 3 syntax), hit a button and RPN is generated.   
  
![[Image: python_rpn_ui_02small.png?raw=1]](https://www.dropbox.com/s/3xcmxfxraxc6wej/python_rpn_ui_02small.png?raw=1)  
  
You then paste the RPN into Free42 or transfer it to your DM42 (by [creating a raw](https://www.swissmicros.com/dm42/decoder/)) - and it runs.

1.  Examples: [http://www.pyrpn.atug.com/examples](http://www.pyrpn.atug.com/examples)
2.  User Guide: [http://www.pyrpn.atug.com/help](http://www.pyrpn.atug.com/help)
3.  Canvas for 42S Simulator: [http://www.pyrpn.atug.com/canvas](http://www.pyrpn.atug.com/canvas)
4.  List of HP42S Commands Supported Reference: [http://www.pyrpn.atug.com/cmds](http://www.pyrpn.atug.com/cmds)

The converter supports core Python syntax (which is very powerful), but does not implement the built in Python libraries that you would get in desktop Python. You have to rely on the ability to call HP42S commands from Python to do your work - which of course you can do. Specifically, it has the following capabilities:

1.  Variables
2.  Functions, Multiple functions, nested functions
3.  Parameter passing, receiving return values, multiple return values
4.  if elif else
5.  Comparison operators == != > < >= <=
6.  Booleans True, False and operators not or and
7.  for loops, range(), for..in iteration through lists and dictionary keys
8.  while loops, while...else
9.  continue and break operations in for loops and while loops
10.  Lists and Dictionaries (basic operations only).
11.  Matrices, Pythonic matrix element access syntax \[row,col\]
12.  NumPy compatible slicing syntax for sub-matrices
13.  Complex numbers using either 42S or Python native syntax
14.  Expressions involving nested brackets
15.  assert
16.  Testing and clearing of flags
17.  Access most HP42S commands as function calls e.g. FIX(2)
18.  Some enhanced functions to make life easier e.g. varmenu() automates and simplifies the generation of MVAR based code.


## Online Programmable RPN calculators

### Rpn-calc

![rpn-calc-1](/projects/websites/images/rpn-calc-1.png)

Here is the built in Javascript code editor. 

Parameters to Javascript functions are taken off the RPN stack. Return values from Javascript functions are pushed onto the RPN stack.

![rpn-calc-2](/projects/websites/images/rpn-calc-2.png)

https://atug.com/jsrpncalc-web/

### Rpn-calc2

A completely new implementation, also programmable in Javascript. Define interactive UI buttons and sliders.

![rpn-calc2-1](/projects/websites/images/rpn-calc2-1.png)

![rpn-calc2-2](/projects/websites/images/rpn-calc2-2.png)

https://atug.com/jsrpncalc2/

## Jupyter Notebooks

A way of implementing complex calculators incl. scrolling text area UI widgets within Jupyter Notebooks. 

### Scrolling Textareas

Scrolling Textareas in a Python Jupyter Notebook, allows building a kind of "Calculator Playground".

![](/projects/websites/images/jupyter-calc-pi.gif)

Notebook at https://bitbucket.org/abulka/jupyter_play/src/master/



### Google Colaboratory

A way of implementing UI scrolling regions within Google Colaboratory Notebooks. 
Google Colaboratory, or "Colab" for short, is a version of Jupyter Notebooks, and allows you to write and execute Python in your browser.

This [Colab project](https://colab.research.google.com/drive/1_R4DAqhVgfPc4113N5VxHVeUJ9oxDMKM#scrollTo=bz9ue7M7cRPq) is a simpler version of the scrolling text area idea above, and needs to be fleshed out a little more fully to match the native Jupyter notebook functionality above.

![jupyter-google-colab-1](/projects/websites/images/jupyter-google-colab-1.gif)

## Toolback - App Builder

An online programming environment, with low code features.  Drag and drop a UI and add scripts directly to components.  Generate websites and desktop apps (electron based) with a click of a button.

### Toolback

Toolback is the drag and drop UI builder and online, Low Code, app building IDE.

<!-- ![toolback-1](/projects/websites/images/toolback-1.png) -->

![toolback-2](/projects/websites/images/toolback-2.png)

![toolback-7](/projects/websites/images/toolback-7-drag-drop.png)

![toolback-3](/projects/websites/images/toolback-3.png)

![toolback-4](/projects/websites/images/toolback-4.png)

Preview your app with a key press.

![toolback-5](/projects/websites/images/toolback-5-menus.gif)

Export to a website or electron app - one click!

![toolback-6](/projects/websites/images/toolback-6-electron.png)


### Toolback Lite

Toolback-Lite is a lightweight drag and drop UI builder and online app building IDE. The drag and drop is done on a grid rather than using the the complex [grapes-js](https://grapesjs.com/) html builder library, which Toolback uses. 

![toolback-lite-1](/projects/websites/images/toolback-lite-1.gif)


## Chord Jammer

A midi web app that lets you play chords with 1 finger in the left hand
and jam safely in the right hand. 
As you change chords, the rh notes are filtered so you always play good sounding notes.

![screenshot](/projects/websites/images/chord-jammer-1.png)

<p>
    MIDI powered by <a href="https://webmidijs.org/docs/">WebMidi.js</a>
    GUI powered by <a href="http://g200kg.github.io/webaudio-controls/docs/index.html">webaudio-controls</a>
    Scales powered by <a href="https://github.com/tonaljs/tonal">tonaljs</a> - A functional music theory library for
    Javascript.
</p>

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
