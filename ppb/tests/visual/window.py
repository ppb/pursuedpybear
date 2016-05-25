"""
Window Visual Test Module

This test passes if your hardware module instantiates a window, updates to
a default screen, and closes after five seconds. It must also close in
response to a quit event handled by hitting the close button on the
window.
"""

from ppb.engine import message
from ppb.event import Quit, Tick
from ppb.tests.visual import Runner


def quit_timer(time):
    def callback(tick_event, count=[time]):
        count[0] += -1 * tick_event.sec
        if count[0] <= 0:
            message(Quit())
    return callback

test_runner = Runner("sdl2")
test_runner.set_events([(Tick, quit_timer(5))])
test_runner.run()
