---
title: "EuroPi - Trigger to Gate"
linkTitle: "EuroPi - Trigger to Gate"
type: docs
weight: 20
tags: ["Software Product", "Python", "Eurorack", "Raspberry Pi"]
---

### Trigger to Gate Script for EuroPi

This script allows you to convert trigger into a gate signal.

I originally wrote this script because my [2hp MIDI](https://www.twohp.com/modules/midi) module clock outputs 6ms triggers, which are too short to inter-operate with most of my Eurorack modules, which require longer gates e.g. 200ms. 

Using my disting module or buying a [Doepfer A-162-2 Dual Trigger Delay](https://doepfer.de/a100_man/A162_man.pdf) module just for this seemed overkill, so I wrote this script for my existing EuroPi module, which at the time, did not have a trigger to gate script.

<!-- ![Oscilloscope](https://cdn.shopify.com/s/files/1/0552/0923/0485/files/gates_and_trigs.png?v=1628550175) -->

<img src="https://cdn.shopify.com/s/files/1/0552/0923/0485/files/gates_and_trigs.png?v=1628550175" alt="Oscilloscope" width="30%">

<br>
<br>

See [this explanation](https://noiseengineering.us/blogs/loquelic-literitas-the-blog/getting-started-gates-vs-triggers) on the difference between gates and triggers.

> This `trigger_to_gate.py` script is different to the `gates_and_triggers.py` script now bundled with current (2024) versions of the EuroPi. The differences in features are explained below.

### What is a EuroPi?

The EuroPi Module is a Eurorack module that allows you to control your modular synthesizer with a Raspberry Pi. 
You build it yourself using the information at https://github.com/Allen-Synthesis/EuroPi

<img src="/projects/libraries/images/europi-built.jpg" alt="EuroPi Module" width="20%">


### Trigger to Gate

Generates a gate on cv1 in response to a trigger on din.

Control the outgoing pulse width with knob k1. Control the delay between the trigger and the gate starting with knob k2. Handy for converting short triggers (e.g. 1ms) into longer gates (e.g. 10ms) as some Eurorack modules don't like short
triggers.

> See my stripped down, alternative [Trigger Gate Delay](#trigger-gate-delay) script below, which is a simpler version of this script without the clock mode functionality.


#### Installation

Since the EuroPi `software/contrib` does not have this
script already bundled (see [pull request](https://github.com/Allen-Synthesis/EuroPi/pull/260)), you will need to manually install it by copying it
onto the EuroPi using [Thonny IDE](https://thonny.org/).

1. Copy the file [trigger_to_gate.py](https://github.com/abulka/EuroPi/blob/a1841b0a294aa189dc96dc4d6bcbeaa1caec539d/software/contrib/trigger_to_gate.py) to `/lib/contrib/trigger_to_gate.py` on your EuroPi.

2. Edit `main.py` in the EuroPi `/` directory to include the Trigger to Gate script in the menu:

```python
["TriggerToGate",    "contrib.trigger_to_gate.TriggerToGate"],  # <-- add this line
```


#### Documentation:

**Trigger to Gate**

- author: Andy Bulka (tcab) (github.com/abulka)
- date: 2023-05-16
- labels: trigger, gate, clock

**Trigger to Gate** mode: Generates a gate on cv1 in response to a trigger on din.
Control the outgoing pulse width with k1. Control the delay between the trigger
and the gate starting with k2. Handy for converting short triggers (e.g. 1ms)
into longer gates (e.g. 10ms) as some eurorack modules don't like short
triggers.

    din = trigger input
    cv1 = gate output
    b1 = toggle gate output on/off
    k1 = length of gate (1-1500ms)
    k2 = delay of gate (0-1500ms)

**Clock** mode: Generates an independent (unrelated to din or gate output),
internally driven clock output on cv2. Handy for when you need a simple clock with variable gate length.

    cv2 = clock output
    b1 = toggle clock output on/off
    k1 = length of clock pulse (1-1500ms)
    k2 = period of clock (1-1500ms) - how fast the clock pulses



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

#### Example

- Incoming trigger is blue (DIN)
- Outgoing gate is purple (CV1).
- The internally driven clock outgoing gate (CV2) is not wired in this example.

<img src="/projects/libraries/images/europi-trigger.jpg" alt="Script at work" width="20%">
<br>
<br>

- In this screenshot we see the outgoing gate is `226ms` - you can change this by turning knob 1.

- The delay is `0ms` meaning there is no delay between the incoming trigger and the outgoing gate. You can change the delay ms by turning knob 2.

Result:

![Oscilloscope](/projects/libraries/images/trigger-gate-oscilloscope.png)

#### Why not use the bundled `gates_and_triggers.py` script?

The 2024 and later EuroPi installation is now already bundled with a `gates_and_triggers.py` script which also generates a gate from a trigger but 
- does not have a delay feature like many hardware modules implementing 'trigger to gate' functionality have e.g. disting [H6 algorithm](https://synthmodes.com/modules/disting_mk4/#p-H6%20Dual%20Delayed%20Pulse%20Generator) and the [Doepfer A-162-2 Dual Trigger Delay](https://doepfer.de/a100_man/A162_man.pdf) module.
- does not have a clock mode
- no knob pass through behaviour
- less choices on output gate lengths

My `trigger_to_gate.py` script also handles all possible edge cases like turning up the delay to more than gate length, or turning up the gate size past the trigger period etc. It also lets you choose from a larger variety of output gate lengths, using an easy to use exponential turn of the knob.

The knob passthrough feature is useful for when you want to toggle between gate and clock modes, and not have the knob jump to the previous value when you switch modes.  

The knob passthrough feature is also useful when you turn on your hardware module and you want the knob value to be in the same position as when you turned it off, and the knob has physically moved slightly, so your sound is different.

The bundled `gates_and_triggers.py` script on the other hand:
- has has more cv outputs for rising and falling edges etc. if you need that
- is shorter, so if you don't need the extra features of my script (like gate delay, knob pass though), you might prefer the bundled script. 

<!-- > **2024 update**: See my alternative [Trigger Gate Delay](#trigger-gate-delay) script below, which is a simpler version of this script without the clock mode functionality. If you choose to install the script without the knob pass-through mitigation, it is only 15% longer than the bundled `gates_and_triggers.py` script. -->

> See also: my stripped down, alternative [Trigger Gate Delay](#trigger-gate-delay) script below, which is a simpler version of this script without the clock mode functionality.

> See also: [Documentation](/projects/libraries/europi-script-utils) on my Scheduler, Hysteresis Mitigation and Knob Pass Through Utility Functions, which you can use in your own EuroPi scripts.


### Trigger Gate Delay {#trigger-gate-delay}

This script is a simpler, shorter version of the above script, without the *clock mode* functionality, which makes the script more understandable (if you are interested in reading the code) and shorter in length. It just offers the basic 'trigger to gate' functionality, with optional gate delay.

I've named it 'Trigger Gate Delay' (instead of 'Trigger to Gate') to differentiate it from the more complex script.

#### Installation

1. Copy the file [trigger_gate_delay.py](/projects/libraries/code/trigger_gate_delay.py) to `/lib/contrib/trigger_gate_delay.py` on your EuroPi.
2. Edit `main.py` in the EuroPi `/` directory to include the script in the menu:

```python
["TriggerGateDelay",    "contrib.trigger_gate_delay.TriggerGateDelay"],  # <-- add this line
```

If you want an even shorter script, eliminate either or both the `KnobWithPassThrough` and `KnobWithHysteresis` classes and  delete the following lines:

```python
# Wrap knobs in KnobWithHysteresis to avoid jitter.
self.k1_gate_length = KnobWithHysteresis(k1, tolerance=2, name="k1_gate_length")
self.k2_gate_delay = KnobWithHysteresis(k2, tolerance=2, name="k2_gate_delay")

# Wrap knobs in KnobWithPassThrough to prevent values jumping when toggling modes.
self.k1_gate_length = KnobWithPassThrough(self.k1_gate_length, initial_value=_.gate_length)
self.k2_gate_delay = KnobWithPassThrough(self.k2_gate_delay, initial_value=_.gate_delay)
```

This will make the script shorter, but you will lose the benefits of the hysteresis and pass-through logic.

- [trigger_gate_delay.py - tiny](/projects/libraries/code/trigger_gate_delay_TINY.py) - no hysteresis or pass-through mitigation 

For those wanting to conserve disk space on their EuroPi, the script with hysteresis mitigation only (no knob pass-through mitigation) is a good compromise between script length and functionality. Also, "pass-through" mitigation is not as important as "hysteresis" mitigation, especially since we aren't switching 'modes' with this simplified 'Trigger Gate Delay' script.

- [trigger_gate_delay.py - hysteresis](/projects/libraries/code/trigger_gate_delay_HYSTERESIS.py) - hysteresis mitigation only
