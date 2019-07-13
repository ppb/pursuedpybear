import time
import logging

import ppb.eventlib as eventlib
import ppb.events as events

logger = logging.getLogger(__name__)


default_resolution = 800, 600


class System(eventlib.EventMixin):

    def __init__(self, **_):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


from ppb.systems.inputs import EventPoller
from .renderer import Renderer, Image


class Updater(System):

    def __init__(self, time_step=0.016, **kwargs):
        self.accumulated_time = 0
        self.last_tick = None
        self.start_time = None
        self.time_step = time_step

    def __enter__(self):
        self.start_time = time.monotonic()

    def on_idle(self, idle_event: events.Idle, signal):
        if self.last_tick is None:
            self.last_tick = time.monotonic()
        this_tick = time.monotonic()
        self.accumulated_time += this_tick - self.last_tick
        self.last_tick = this_tick
        while self.accumulated_time >= self.time_step:
            # This might need to change for the Idle event system to signal _only_ once per idle event.
            self.accumulated_time += -self.time_step
            signal(events.Update(self.time_step))
