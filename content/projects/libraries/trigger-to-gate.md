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

This script is a simpler version of the above script, without the clock mode functionality, which makes the script more understandable and shorter. It just offers the basic trigger to gate functionality.

I've named it 'Trigger Gate Delay' (instead of 'Trigger to Gate') to differentiate it from the more complex script.

#### Installation

1. Copy the file [trigger_gate_delay.py] to `/lib/contrib/trigger_gate_delay.py` on your EuroPi.
2. Edit `main.py` in the EuroPi `/` directory to include the script in the menu:

```python
["TriggerGateDelay",    "contrib.trigger_gate_delay.TriggerGateDelay"],  # <-- add this line
```

#### Source Code

`trigger_gate_delay.py`:

```python
from europi import oled, k1, k2, b1, b2, din, cv1, cv2
from europi_script import EuroPiScript
import machine
import utime

"""
Trigger Gate Delay
author: Andy Bulka (tcab) (github.com/abulka)
date: 2024-06-01
labels: trigger, gate, delay

Generates a gate on cv1 in response to a trigger on din.
Control the outgoing pulse width with k1. Control the delay between the trigger
and the gate starting with k2. Handy for converting short triggers (e.g. 1ms)
into longer gates (e.g. 10ms) as some eurorack modules don't like short
triggers.

See documentation in trigger_to_gate.md for more details.
"""

class Data:
    def __init__(self):
        # the default parameters controlled by the knobs
        self.gate_length = 10 # ms, generated pulse duration
        self.gate_delay = 0 # ms, delay between din trigger and gate start

        # states controlled by the buttons
        self.gate_running = True

        # dynamically calculated values
        self.din_length = 0 # length of incoming trigger pulse (guess, calculated)
        self.din_period = 0 # time between incoming triggers (guess, calculated)

        # screen related
        self.updateUI = True

        # gate related
        self.din_state: bool = False
        self.gate_is_high: bool = False
        self.din_time_of_last_trigger = 0

        # knob choices
        self.knob_values = list(range(1, 201)) + list(range(201, 501, 5)) + list(range(501, 1600, 20)) # approx 315 values
        self.knob_values_gate_length = self.knob_values
        self.knob_values_gate_delay = [0] + self.knob_values

        # refresh rates
        self.frame_rate = 30 # for screen refresh
        self.schedule_resolution_ms = 1 # how often to check the schedule
        self.screen_refresh_rate_ms = 150 # int(1000 / self.frame_rate)
        self.knobs_read_interval_ms = int(1000 / self.frame_rate)

        # other
        self.after_off_settling_ms = 2 # time to wait after turning off gate or clock output, or it doesn't happen cleanly
        self.updateSavedState = False


class Screen:
    """
    Show running status on 128x64 pixels OLED screen (text, x, y, color))
    """
    def __init__(self, data):
        self.data = data

    def draw(self, show=True):
        _ = self.data
        line1 = f"din {_.din_length}ms {_.din_period}ms"
        line2 = f"1 gate_len {_.gate_length}ms"
        line3 = f"1 delay {_.gate_delay}ms"
        line1 += f" {'.' if _.gate_running else ''}"
        oled.fill(0)
        oled.text(line1, 0, 0, 1)
        oled.text(line2, 0, 12, 1)
        oled.text(line3, 0, 24, 1)
        if show:
            oled.show()

    def clear(self):
        oled.fill(0)
        oled.show()


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


class TriggerGateDelay(EuroPiScript):
    def __init__(self):
        super().__init__()
        self.data = Data()
        _ = self.data
        
        state = self.load_state_json()
        _.gate_length = state.get("gate_length", _.gate_length)
        _.gate_delay = state.get("gate_delay", _.gate_delay)
        _.gate_running = state.get("gate_running", _.gate_running)

        # Overclock the Pico for improved performance.
        machine.freq(250_000_000)

        # gate mode
        self.k1_gate_length = k1
        self.k2_gate_delay = k2

        # Wrap knobs in KnobWithHysteresis to avoid jitter.
        self.k1_gate_length = KnobWithHysteresis(k1, tolerance=2, name="k1_gate_length")
        self.k2_gate_delay = KnobWithHysteresis(k2, tolerance=2, name="k2_gate_delay")

        # Wrap knobs in KnobWithPassThrough to prevent values jumping when toggling modes.
        self.k1_gate_length = KnobWithPassThrough(self.k1_gate_length, initial_value=_.gate_length)
        self.k2_gate_delay = KnobWithPassThrough(self.k2_gate_delay, initial_value=_.gate_delay)

        self.scheduler = Scheduler()
        
        self.screen = Screen(self.data)

        @din.handler
        def din_rising():
            _ = self.data
            if not self.scheduler.enabled: return
            _.din_state = True

            now = utime.ticks_ms()
            _.din_period = utime.ticks_diff(now, _.din_time_of_last_trigger)
            _.din_time_of_last_trigger = now

            delay = _.gate_delay
            if _.gate_is_high:
                self.gate_off_task()
                self.scheduler.remove_task(self.gate_off_task, must_be_found=True) # cancel the existing gate_off task
                delay = max(_.gate_delay, _.after_off_settling_ms)
            self.scheduler.remove_task(self.gate_on_task, must_be_found=False) # cancel any existing gate_on task which had a long delay and hasn't run yet
            if _.gate_running:
                self.scheduler.add_task(self.gate_on_task, delay)

        @din.handler_falling
        def din_falling():
            _ = self.data
            _.din_state = False
            now = utime.ticks_ms()
            _.din_length = utime.ticks_diff(now, _.din_time_of_last_trigger)

        @b1.handler_falling
        def button1_click():
            _ = self.data
            _.gate_running = not _.gate_running
            _.updateUI = True

            if _.updateUI:
                _.updateSavedState = True

    def gate_on_task(self):
        _ = self.data
        cv1.on()
        _.gate_is_high = True
        self.scheduler.add_task(self.gate_off_task, _.gate_length)

    def gate_off_task(self):
        _ = self.data
        cv1.off()
        _.gate_is_high = False

    def read_knobs_task(self):
        _ = self.data

        new_value = self.k1_gate_length.choice(_.knob_values_gate_length)
        if new_value != _.gate_length:
            _.gate_length = new_value
            _.updateUI = True

        new_value = self.k2_gate_delay.choice(_.knob_values_gate_delay)
        if new_value != _.gate_delay:
            _.gate_delay = new_value
            _.updateUI = True                

        if _.updateUI:
            _.updateSavedState = True

        self.scheduler.add_task(self.read_knobs_task, _.knobs_read_interval_ms)

    def update_screen_task(self):
        _ = self.data
        if _.updateUI:
            self.screen.draw()
            _.updateUI = False
        self.scheduler.add_task(self.update_screen_task, _.screen_refresh_rate_ms)

    def save_state_task(self):
        _ = self.data
        if _.updateSavedState:
            _.updateSavedState = False
            self.save_state()
        self.scheduler.add_task(self.save_state_task, 5000)

    def stop(self):
        _ = self.data
        self.scheduler.stop()
        self.screen.clear()
        cv1.off()
        _.gate_running = False

    def save_state(self):
        """Save the current state variables as JSON."""
        # Don't save if it has been less than 5 seconds since last save.
        if self.last_saved() < 5000:
            return
        
        _ = self.data
        state = {
            'gate_length': _.gate_length,
            'gate_delay': _.gate_delay,
            'gate_running': _.gate_running,
        }
        self.save_state_json(state)

    def main(self):

        self.scheduler.add_task(self.read_knobs_task)
        self.scheduler.add_task(self.update_screen_task)
        self.scheduler.add_task(self.save_state_task)

        try:
            while self.scheduler.enabled:
                self.scheduler.run_once()
                utime.sleep_ms(self.data.schedule_resolution_ms)
        except KeyboardInterrupt:
            print("Interrupted")
            self.stop()
            print('Shutdown complete')
            raise
            
if __name__ == "__main__":
    TriggerGateDelay().main()

```

If you want an even shorter script, eliminate the `KnobWithPassThrough` and `KnobWithHysteresis` classes and just use the knobs directly by deleting the following lines:

```python
# Wrap knobs in KnobWithHysteresis to avoid jitter.
self.k1_gate_length = KnobWithHysteresis(k1, tolerance=2, name="k1_gate_length")
self.k2_gate_delay = KnobWithHysteresis(k2, tolerance=2, name="k2_gate_delay")

# Wrap knobs in KnobWithPassThrough to prevent values jumping when toggling modes.
self.k1_gate_length = KnobWithPassThrough(self.k1_gate_length, initial_value=_.gate_length)
self.k2_gate_delay = KnobWithPassThrough(self.k2_gate_delay, initial_value=_.gate_delay)
```

This will make the script shorter, but you will lose the benefits of the hysteresis and pass-through logic.

