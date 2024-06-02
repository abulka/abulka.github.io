---
title: "EuroPi - Utility Classes"
linkTitle: "EuroPi - Utility Classes"
type: docs
weight: 20
tags: ["Software Product", "Python", "Eurorack", "Raspberry Pi"]
---

### Introduction

My [Trigger to Gate](/projects/libraries/europi-trigger-to-gate) script for [EuroPi](https://github.com/Allen-Synthesis/EuroPi) uses some utility functions I developed, that might be useful for other EuroPi scripts:

- KnobWithHysteresis
- KnobWithPassThrough
- Scheduler

Rather than each EuroPi script inventing its own hyseresis mitigation and knob pass-through logic etc., these utility classes can be used by any EuroPi script that needs them. 

You can install them into the `lib/contrib/experimental` directory of the EuroPi software, or in a separate `lib/contrib/utils` directory. Indeed, you can put them wherever you want - even copy and paste the classes into the body of the EuroPi script you are developing.

#### The problems these utility classes solve

**Hysteresis Mitigation**

The term [hysteresis](https://electronics.stackexchange.com/questions/266608/stable-output-from-a-potentiometer) refers to the problem of the knob value flickering when
the knob is not being turned. This is a common problem with rotary encoders and
can be mitigated by only accepting new values when the knob has been turned by a
certain amount. This is especially useful when you have a knob that is used to
set a value that is displayed on a screen, as in the Trigger to Gate script.

The knobs in my [Trigger to Gate](/projects/libraries/europi-trigger-to-gate)
script use hysteresis mitigation which prevents the values flickering, even
though you are not turning the knob. There is a 1 second timeout when you can
dial in the exact value you want, then the knob value will "lock". To unlock the
knob value, turn the knob past the threshold again.

**Pass-through knob values**

The term "pass-through" refers to the technique of enabling a parameter's value
only when the knob physical position passes through the existing value, which
prevents sudden jumps in values when you switch screen modes.

If knobs are used in two different modes, as they are in my [Trigger to
Gate](/projects/libraries/europi-trigger-to-gate) script, we run into the
problem of the physical knob position not matching the last value of that mode,
when you switch between modes (between trigger to gate mode and clock mode, for
example). To solve this, the knobs use "pass-through" logic, which you may be
familiar with when loading presets into a hardware synthesiser.

If turning a knob doesn't change the value, it's because the knob is not yet
"passed-through" the current value. Simply turn the knob until it does change. For example,
if the existing value is 0 and your physical knob position is at "5 o'clock" then you need to
turn the physical knob counter-clockwise until it passes through 0 and then clockwise again
to your required value.

**Scheduler**

When writing a EuroPi script, you may need to run tasks at a given time in the
future. For example, you may want to turn off a gate after a certain time, or
run a task every second. Most EuroPi scripts will have a simple while loop that
runs continuously, with various ad-hoc flags and variables managing the
behaviour inside the loop. This can get messy and hard to understand.

My scheduler class offers a more organised way of looping and scheduling tasks
to run at a given time in the future. A task is a function that you want to run
at a given time in the future, thus instead of having a while loop and global
variables, you have a function per task and a time to run it.

> Another potentially interesting way of managing tasks is to use a game inspired
**Entity Component System** loop, as I describe in my article [TodoMVC
implemented using a game architecture —
ECS](/blog/2020/05/18/todomvc-implemented-using-a-game-architecture-ecs/). I
leave that as an exercise for the future.

<u>Slow screen updates in EuroPi</u>

Screen updates in EuroPi are a blocking operation and take a long time relative
to the ms activity of signals and interrupts. This means incoming triggers can
easily be missed and interrupts won't fire. The scheduler class can help with
this problem. For example, you can schedule to update the screen at a regular
interval, rather than updating the screen every time you change a value. Even
better, you can use the scheduler to update the screen only when the value has
changed, rather than every time through the loop. This is accomplished by
scheduling the screen update task only when needed, and ensure that the screen
update task function does not reschedule itself.

If you are not using the Scheduler class, you should use a flag to
indicate when the screen needs updating and only update the screen when the flag
is set.

> **NOTE:** MicroPython async is supported on the Raspberry Pi Pico, and can
help with task management. However even when using async, there is only one
thread involved so you still need to be careful with blocking operations like
writing to the screen. There is a second thread available on the Raspberry Pi
Pico but MicroPython support for this feature is unreliable but will hopefully
will improve in the future (we have been hoping for this for a long time though
2022-2024 and it is still a problem).

The utility classes presented here do not use async, nor do they use the second
thread.

Here are the utility classes:

### class KnobWithHysteresis

This is a class to cure the hysteresis problem with the rotary encoder knobs k1
and k2 of the EuroPi.  

It is easy to use because you just wrap the knob in the class and it will
automatically mitigate the hysteresis problem. The knob will only change value
when you turn it by a certain amount, which you can set with the `tolerance`.

##### Usage

```python
from europi import k1, k2

k1 = KnobWithHysteresis(k1)  # backwards compatible, no hyteresis mitigation
k1 = KnobWithHysteresis(k1, tolerance=2)  # set tolerance to 2, hysteresis mitigation
```

You can set any value within the `lock_delay` time period (an additional
constructor parameter that defaults to 1000ms) and it will be accepted but once
the `lock_delay` time period expires the value returned will be locked and you
have to move the knob by at least `tolerance` to change the value, at which
point the time period before re-locking is extended by `lock_delay` time
(defaults to 1s).

Starts locked on the first value it sees, to avoid jittery beginning values.

##### Code:

You can include this class in your EuroPi script to cure the hysteresis problem with the rotary encoder.
You can put the code in a separate file and import it into your script. e.g. `from knob_with_hysteresis import KnobWithHysteresis` where your `knob_with_hysteresis.py` file contains the following code:

```python
import utime


class KnobWithHysteresis:
    """
    This is a class to cure the hysteresis problem with the rotary encoder.
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

### class KnobWithPassThrough

Disable changing value till knob is moved and "passes-through" the current cached value.
Useful for when you have a knob that is used in two different modes and you don't want
the value to jump when you switch modes (think recalling presets on a hardware synth).

The knob passthrough feature is also useful when you turn on your hardware
module and you want the knob value to be in the same position as when you turned
it off, and the knob has physically moved slightly, so your sound is unfortunately, different.

The knob value will initiallly lock to the initial_value parameter, which defaults to 50.
Moving the underlying knob by any amount will overwrite that initial_value. If pass-through
is enabled, then you will have to move the underlying knob "through" the initial value to
begin changing it.

Its actually easier to use than to explain!

##### Usage

Simplest usage is to wrap a knob with this class, passing the initial value e.g.

```python    
from europi import k1, k2

choices = list(range(0, 200))

k = KnobWithPassThrough(k1, initial=50)
val = k.choice(choices)  # val will remain 50 until k1 is moved
```

If you want k1 to control two different values depending on a mode, you need to 
create two instances of this class, wrapping the same knob e.g.

```python
from europi import k1, k2

k_mode1 = KnobWithPassThrough(k1, initial=50)
k_mode2 = KnobWithPassThrough(k1, initial=100)
```

Pass through requirement is initially turned off, and only activated when you have 
"switched modes" and need the same knob to drive different values. You switch modes by
calling `mode_changed()` on the (KnobWithPassThrough) knob instance you are switching to.

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

### class Scheduler

A simple scheduler for running tasks at a given time in the future.

##### Usage

```python
import utime

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

For fuller examples of how to use all these classes together, see my [Trigger to Gate](/projects/libraries/europi-trigger-to-gate) script.
