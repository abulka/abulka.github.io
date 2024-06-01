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

Source code: [trigger_to_gate.py](https://github.com/abulka/EuroPi/blob/a1841b0a294aa189dc96dc4d6bcbeaa1caec539d/software/contrib/trigger_to_gate.py)

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

The EuriPi installation is bundled with a `gates_and_triggers.py` script which also generates a gate from a trigger but 
- does not have a delay feature (like e.g. many hardware modules implementing 'trigger to gate' functionality have)
- does not have a clock mode
- no knob pass through behaviour
- less choices on output gate lengths

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


### Documentation on Utility Functions

The script also includes some utility functions that are useful for other EuroPi scripts:

- KnobWithHysteresis
- KnobWithPassThrough
- Scheduler

#### KnobWithHysteresis

This is a class to cure the hysteresis problem with the rotary encoder.

You can set any value within the `lock_delay` time period and it will be
accepted but once the `lock_delay` time period expires the value returned will
be locked and you have to move the knob by at least `tolerance` to change the value,
at which point the time period before re-locking is extended by `lock_delay`
time (defaults to 1s).

Starts locked on the first value it sees, to avoid jittery beginning values.

##### Usage

```python
k1 = KnobWithHysteresis(k1)  # backwards compatible, no hyteresis mitigation
k1 = KnobWithHysteresis(k1, tolerance=2)  # set tolerance to 2, hysteresis mitigation
```


##### Code:

You can include this class in your EuroPi script to cure the hysteresis problem with the rotary encoder.
You can put the code in a separate file and import it into your script. e.g. `from knob_with_hysteresis import KnobWithHysteresis` where your `knob_with_hysteresis.py` file contains the following code:

```python
import utime


class KnobWithHysteresis:
    """
    This is a class to cure the hysteresis problem with the rotary encoder.
    Documentation in tigger_to_gate.md
    """
    def __init__(self, knob, tolerance=0, lock_delay=1000, name=None) -> None:
        self.knob = knob
        self.tolerance = tolerance
        self.lock_delay = lock_delay
        self.lock_time = utime.ticks_ms() # initially locked
        self.name = name if name else "unnamed" # for debugging
        self.value = None  # cached value when locked, when None the first reading is used even when locked

    @property
    def locked(self):
        now = utime.ticks_ms()
        time_left = utime.ticks_diff(self.lock_time, now) # lock_time - now
        _time_expired = time_left <= 0
        return _time_expired

    def _update_value_if_allowed(self, new_value):
        if self.value is None or self._allow(self.value, new_value):
            self.value = new_value
        return self.value

    def _allow(self, old_value, new_value):
        if self.tolerance == 0:
            return True  # backwards compatibility
        if not self.locked:
            return True  # allow any value to get in

        # at this point the lock_time has expired
        big_enough_change = abs(old_value - new_value) >= self.tolerance
        if big_enough_change:
            now = utime.ticks_ms()
            self.lock_time = now + self.lock_delay
            self.locked_msg_shown_debug = False
            return True

        return False

    def choice(self, *args):
        new_value = self.knob.choice(*args)
        return self._update_value_if_allowed(new_value)

    # TODO Wraps an instance of Knob, so need to expose all Knob methods
    # and the methods of its superclass AnalogueReader.
```

#### KnobWithPassThrough

Disable changing value till knob is moved and "passes-through" the current cached value.
Useful for when you have a knob that is used in two different modes and you don't want
the value to jump when you switch modes (think recalling presets on a hardware synth).

Pass through requirement is initially turned off, and only activated when you have 
"switched modes" and need the same knob to drive different values. You switch modes by
calling `mode_changed()` on the (KnobWithPassThrough) knob instance you are switching to.

The knob value will initiallly lock to the initial_value parameter, which defaults to 50.
Moving the underlying knob by any amount will overwrite that initial_value. If pass-through
is enabled, then you will have to move the underlying knob "through" the initial value to
begin changing it.

Its actually easier to use than to explain!

##### Usage

Simplest usage is to wrap a knob with this class, passing the initial value e.g.

```python    
choices = list(range(0, 200))

k = KnobWithPassThrough(k1, initial=50)
val = k.choice(choices)  # val will remain 50 until k1 is moved
```

If you want k1 to control two different values depending on a mode, you need to 
create two instances of this class, wrapping the same knob e.g.

```python
k_mode1 = KnobWithPassThrough(k1, initial=50)
k_mode2 = KnobWithPassThrough(k1, initial=100)
```

When you switch modes e.g. as a result of a button press, you need to call `mode_changed()` on the
mode you are switching to, in order to tell it to use its cached value until physical knob 
pass-through has ocurred e.g.

```python
@b2.handler_falling
def button_click():
    mode = 2 if mode == 1 else 1
    if mode == 1:
        k_mode1.mode_changed()
    elif mode == 2:
        k_mode2.mode_changed()

# Read from the correct (KnobWithPassThrough) knob depending on mode
# Reading from the other modes's KnobWithPassThrough knob is undefined
if mode == 1:
    val = k_mode1.choice(choices)
elif mode == 2:
    val = k_mode2.choice(choices)
```

##### Code:

You can include this class in your EuroPi script to cure the knob pass-through problem with the rotary encoder.
You can put the code in a separate file and import it into your script. e.g. `from knob_with_pass_through import KnobWithPassThrough` where your `knob_with_pass_through.py` file contains the following code:

```python
class KnobWithPassThrough:
    """
    Disable changing value till knob is moved and "passes-through" the current cached value.
    Documentation in tigger_to_gate.md
    """
    def __init__(self, knob, initial_value=50) -> None:
        self.knob = knob
        self.value = initial_value # cached value when locked
        self.locked = False # stay on value until the knob meets unlock condition
        self.unlock_condition = 'any change'  # '<' or '>' or 'any change'
        self.locked_on_knob_value = None # remember knob value we initially locked on when setting to 'any change'
        self.recalc_pending = False # unlock_condition needs recalculating

    def mode_changed(self):
        # call this when switching to a new mode that uses the same underlying knob
        self.recalc_pending = True

    def _recalc_pass_through_condition(self, current_knob_value):
        self.locked = True
        self.unlock_condition = '<' if current_knob_value > self.value else '>'

    def _has_passed_through(self, value):
        if self.unlock_condition == '<':
            return value <= self.value
        elif self.unlock_condition == '>':
            return value >= self.value
        elif self.unlock_condition == 'any change':
            return value != self.locked_on_knob_value

    def _update_pass_through(self, new_value):
        if self.recalc_pending:
            self._recalc_pass_through_condition(new_value)
            self.recalc_pending = False
        if self.locked_on_knob_value is None:
            self.locked_on_knob_value = new_value
            self.locked = True
            return self.value
        if self.locked and self._has_passed_through(new_value):
            self.locked = False

        if self.locked:
            # return the cached value
            return self.value
        else:
            # pass through underlying knob new value, update cache
            self.value = new_value
            return self.value

    def choice(self, *args, **kwargs):
        new_value = self.knob.choice(*args)
        return self._update_pass_through(new_value)
```

#### Scheduler

A simple scheduler for running tasks at a given time in the future.

##### Usage

```python
s = Scheduler()

s.schedule_task(some_function, ms=1000)  # run some_function in 1 second
s.schedule_task(some_other_function, ms=2000)  # run some_other_function in 2 seconds

while s.enabled:
    s.run_once()
    utime.sleep_ms(10) # the lower this is, the more accurate the schedule will be

def some_function():
    print("some_function called")
    s.schedule_task(some_function, ms=1000)  # reschedule some_function to run in 1 second
```

You can stop your loop using s.stop() which sets s.enabled to False,
or just interrupt it with Ctrl-C. Its really up to you how you implement the loop.

Callbacks can be any callable object, e.g. a function, a method, a lambda, etc.
No support for passing arguments to callbacks yet.

Implementation Note: MicroPython does not support methods having reference
equality (regular functions are ok) so we have to compare callbacks using the
callback's function name string rather than by the callback function object
itself.

##### Code:

You can include this class in your EuroPi script to run tasks at a given time in the future.
You can put the code in a separate file and import it into your script. e.g. `from scheduler import Scheduler` where your `scheduler.py` file contains the following code:

```python
import utime


class Scheduler:
    """
    A simple scheduler for running tasks at a given time in the future.
    Documentation in tigger_to_gate.md
    """

    def __init__(self):
        self.enabled = True
        self.schedule = [] # list of tuples (time, callback, callback_func_name)

    def add_task(self, callback, ms:int=0):
        self.schedule.append((utime.ticks_add(utime.ticks_ms(), ms), callback, callback.__name__))

    def remove_task(self, callback, must_be_found=False):
        to_remove = []
        found = False
        for scheduled_time, cb, callback_func_name in self.schedule:
            if callback_func_name == callback.__name__:
                to_remove.append((scheduled_time, cb, callback_func_name))
                found = True
        for item in to_remove:
            self.schedule.remove(item)
        if not found and must_be_found:
            print(f"cannot remove task {callback} viz. {callback.__name__} from schedule", len(self.schedule), "tasks in schedule")
            self.print_schedule()

    def run_once(self):
        now = utime.ticks_ms()
        for scheduled_time, callback, _ in self.schedule:
            if utime.ticks_diff(scheduled_time, now) <= 0:
                self.schedule.remove((scheduled_time, callback, _))
                callback()

    def stop(self):
        self.enabled = False

    def print_schedule(self):
        print('  Schedule:')
        for scheduled_time, callback, callback_func_name in self.schedule:
            print(f"  {callback_func_name} {scheduled_time}")
```

### Simpler Script - 'Trigger Gate Delay'

This script is a simpler version of the above script, without the clock mode functionality, which makes the script more understandable and shorter. It just offers the basic 'trigger to gate' functionality.

I've named it 'Trigger Gate Delay' (instead of 'Trigger to Gate') to differentiate it from the more complex script.

- [trigger_gate_delay.py](/projects/libraries/code/trigger_gate_delay.py)

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

For those wanting to conserve disk space on their EuroPi, the script with hysteresis mitigation only (no knob pass-through mitigation) is a good compromise between script length and functionality.

- [trigger_gate_delay.py - hysteresis](/projects/libraries/code/trigger_gate_delay_HYSTERESIS.py) - hysteresis mitigation only
