---
title: "Trigger to Gate Script for EuroPi"
linkTitle: "Trigger to Gate Script for EuroPi"
type: docs
weight: 20
tags: ["Software Product", "Python", "Eurorack", "Raspberry Pi"]
---

### Trigger to Gate Script for EuroPi

This script allows you to trigger a gate signal from a trigger.

### What is a EuroPi?

The EuroPi Module is a Eurorack module that allows you to control your modular synthesizer with a Raspberry Pi. 

![EuroPi Module](/projects/libraries/images/europi-built.jpg)

You build it yourself using the information at https://github.com/Allen-Synthesis/EuroPi

### Trigger to Gate

Generates a gate on cv1 in response to a trigger on din.

Control the outgoing pulse width with k1. Control the delay between the trigger and the gate starting with k2. Handy for converting short triggers (e.g. 1ms) into longer gates (e.g. 10ms) as some Eurorack modules don't like short
triggers.

Code: https://github.com/abulka/EuroPi/blob/a1841b0a294aa189dc96dc4d6bcbeaa1caec539d/software/contrib/trigger_to_gate.py

Issue: https://github.com/Allen-Synthesis/EuroPi/pull/260 


#### Installation

Since the EuroPi `software/contrib` does not have this
script already bundled, you will need to manually install it by copying it
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

Incoming trigger is blue (DIN) and outgoing gate is purple (CV1).

![Script at work](/projects/libraries/images/europi-trigger.jpg)

In this screenshot we see the outgoing gate is `226ms` - you can change this by turning the knob 1.

The delay is `0ms` meaning there is no delay between the incoming trigger and the outgoing gate. You can change this by turning knob 2.

**Result**

![Oscilloscope](/projects/libraries/images/trigger-gate-oscilloscope.jpg)

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


