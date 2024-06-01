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