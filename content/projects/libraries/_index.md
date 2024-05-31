---
title: "Libraries & Tools"
linkTitle: "Libraries & Tools"
type: docs
weight: 20
tags: ["Software Product", "Vscode", "Electron", "Flask", "SQL"]
---

## Snippet Creator

This extension helps to automate snippet creation. Select the code you want to create snippet from and use command `Create Snippet` from the command palette or your custom keybind.

[https://github.com/abulka/vscode-snippet-creator](https://github.com/abulka/vscode-snippet-creator)

## Snippets Explorer

Visual Studio Code extension which displays all available language snippets in a TreeView

[https://github.com/abulka/vscode-snippets-explorer](https://github.com/abulka/vscode-snippets-explorer/issues)

![demo](https://raw.githubusercontent.com/abulka/vscode-snippets-explorer/master/images/videos/demo1.gif)

## Electron-Flask App Generator

Yoeman project generator to create an Electron app running a Flask server inside itself. Deployable via PyInstaller and Electron Forge packager.

Create an Electron App project that auto-starts a Flask server the electron app can call for services. Deployable as a single App that users can double click on and run.

https://github.com/abulka/generator-electron-flask


         _-----_     ╭──────────────────────────╮
        |       |    │  Welcome to the amazing  │
        |--(o)--|    │ generator-electron-flask │
       `---------´   │        generator!        │
        ( _´U`_ )    ╰──────────────────────────╯
        /___A___\   /
         |  ~  |     
       __'.___.'__   
     ´   `  |° ´ Y ` 

    ? App Name myapp
    ? Description My Electron application description
    ? Author's Name Fred Smith
    ? Author's Email fred@example.com
    ? license: Apache 2.0
    ? Package keywords (comma to split) python, js, great-app
    ? Run flask on port number? 5000
    ? Initial flask url (e.g. /hello or /hello-vue) to display? / hello
    ? Choose from misc options (Press <space> to select, <a> to toggle all, <i> to invert selection)
    ❯◉ Electron logging
    ◯ Print current working directory on startup
    ◯ Print node and electron versions on starrtup
    ◉ Fully quit on Mac on exit (without needing CMD-Q)
    ◉ Open Electron/Chrome DevTools in final app

Example of generated app:

![app running](https://github.com/abulka/generator-electron-flask/raw/main/doco/electron-flask-demo1.gif)

## Dedent for Dart

Dedent - Remove any common leading whitespace from every line in text. Ported from Python.

https://pub.dev/packages/dedent

## Relationship Manager

 A lightweight Object Database (no SQL used) class for Python 3

https://pypi.org/project/relationship-manager/

## Image Presenter

An image presentation tool, where you can click and zoom into various parts of a single image.

![](/projects/libraries/images/image-presenter.png)

Relevant text notes associated with each sub-area would appear when zoomed in.  Arrow keys/buttons allow you to step through a narrated sequence of zooms, so that you get can be carefully guided through an art image, or diagram.

Two demo prototype versions, using different underlying technologies:
- https://atug.com/image_presenter/layerjs/
- https://atug.com/image_presenter/zoomooz/

Source code currently unreleased.


## Jupyter Notebook Tools

A way of implementing complex calculators incl. scrolling text area UI widgets within Jupyter & Colaboratory Notebooks. 

### Scrolling Textareas for Jupyter Notebooks

Scrolling Textareas in a Python Jupyter Notebook, allows building a kind of "Calculator Playground".

![](/projects/websites/images/jupyter-calc-pi.gif)

Various Jupyter Notebooks at https://bitbucket.org/abulka/jupyter_play/src/master/ (private)

Gist of the scrolling textarea technique: https://gist.github.com/abulka/3043e8a4d78d2e26f872542524a0aa3e (public)


### Google Colaboratory

A way of implementing UI scrolling regions within Google Colaboratory Notebooks. 
Google Colaboratory, or "Colab" for short, is a version of Jupyter Notebooks, and allows you to write and execute Python in your browser.

This [Colab project](https://colab.research.google.com/drive/1_R4DAqhVgfPc4113N5VxHVeUJ9oxDMKM#scrollTo=bz9ue7M7cRPq) is a simpler version of the scrolling text area idea above, and needs to be fleshed out a little more fully to match the native Jupyter notebook functionality above.

![jupyter-google-colab-1](/projects/websites/images/jupyter-google-colab-1.gif)

### Trigger to Gate Script for EuroPi

The EuroPi Module is a Eurorack module that allows you to control your modular synthesizer with a Raspberry Pi. This script allows you to trigger a gate signal from a trigger.

Issue: https://github.com/Allen-Synthesis/EuroPi/pull/260 

Generates a gate on cv1 in response to a trigger on din.

Control the outgoing pulse width with k1. Control the delay between the trigger and the gate starting with k2. Handy for converting short triggers (e.g. 1ms) into longer gates (e.g. 10ms) as some Eurorack modules don't like short
triggers.

Code: https://github.com/abulka/EuroPi/blob/a1841b0a294aa189dc96dc4d6bcbeaa1caec539d/software/contrib/trigger_to_gate.py

#### Documentation:

**Trigger to Gate**

- author: Andy Bulka (tcab) (github.com/abulka)
- date: 2023-05-16
- labels: trigger, gate, clock

Trigger to Gate: Generates a gate on cv1 in response to a trigger on din.
Control the outgoing pulse width with k1. Control the delay between the trigger
and the gate starting with k2. Handy for converting short triggers (e.g. 1ms)
into longer gates (e.g. 10ms) as some eurorack modules don't like short
triggers.

    din = trigger input
    cv1 = gate output
    b1 = toggle gate output on/off
    k1 = length of gate (1-1500ms)
    k2 = delay of gate (0-1500ms)

Clock: Generates an independent (unrelated to din or gate output),
internally driven clock output on cv2. Handy for when you need a simple clock.

    cv2 = clock output
    b1 = toggle clock output on/off
    k1 = length of clock pulse (1-1500ms)
    k2 = period of clock (1-1500ms) - how fast the clock pulses


#### Installation

Since the EuroPi `software/contrib` does not have this
script already bundled, you will need to manually install it by copying it
onto the EuroPi using [Thonny IDE](https://thonny.org/).

1. Copy the file [trigger_to_gate.py](https://github.com/abulka/EuroPi/blob/a1841b0a294aa189dc96dc4d6bcbeaa1caec539d/software/contrib/trigger_to_gate.py) to `/lib/contrib/trigger_to_gate.py` on your EuroPi.

2. Edit `main.py` in the EuroPi `/` directory to include the Trigger to Gate script in the menu:

```python
    ["TriggerToGate",    "contrib.trigger_to_gate.TriggerToGate"],  # <-- add this line
```



#### Usage

You can have both the gate and clock outputs running at the same time. There are
two configuration screens, gate and clock. The screen mode is toggled by pressing b2.

    b2 = toggle between gate/clock screen

This is what the screens look like:

```
                       Trigger to Gate Screen                                           
         ┌─────────────────────────────────────────────┐                                
         │ Incoming din pulse length    din period   . │ ◀────── . symbol means that    
         │                                             │         that gate output is on 
(knob 1) │ Length of Gate                              │                                
         │                                             │         (b1 toggles)           
(knob 2) │ Gate Delay                                  │                                
         └─────────────────────────────────────────────┘                                
                                                                                        
                           Clock Screen                                                 
         ┌─────────────────────────────────────────────┐                                
         │ Clock bpm                                 . │ ◀────── . symbol means that    
         │                                             │         that clock output is on
(knob 1) │ Clock pulse length                          │                                
         │                                             │         (b1 toggles)           
(knob 2) │ Clock period (speed)                        │                                
         └─────────────────────────────────────────────┘                                                             
```
#### Why not use the bundled `gates_and_triggers.py` script?

The bundled `gates_and_triggers.py` script also generates a gate from a trigger but 
- does not have a delay feature (like e.g. many hardware modules implementing trigger to gate have)
- does not have a clock mode
- no knob pass through behaviour

My `trigger_to_gate.py` script also handles all possible edge cases like turning up the delay to more than gate length, or turning up the gate size past the trigger period etc. It also lets you choose from a larger variety of output gate lengths, using an easy to use exponential turn of the knob.

The bundled `gates_and_triggers.py` script on the other hand has has more cv outputs for rising and falling edges etc. if you need that.

#### Note on changing knob values:

**Pass-through knob values**

Because the knobs are used in two different modes, we run into the problem of the physical
knob position not matching the value when you switch between modes. To solve this, the knobs
use "pass-through" logic, which you may be familiar with when loading presets into a hardware
synthesiser.

The term "pass-through" refers to the technique of enabling a parameter's value
only when the knob physical position passes through the existing value, which
prevents sudden jumps in values when you switch screen modes.

If turning a knob doesn't change the value, it's because the knob is not yet
"passed-through" the current value. Simply turn the knob until it does change. For example,
if the existing value is 0 and your physical knob position is at "5 o'clock" then you need to
turn the physical knob counter-clockwise until it passes through 0 and then clockwise again
to your required value.

**Hysteresis Mitigation**

The knobs also use hysteresis mitigation which prevents the values flickering,
even though you are not turning the knob. There is a 1 second timeout when you
can dial in the exact value you want, then the knob value will "lock". To unlock
the knob value, turn the knob past the threshold again.

