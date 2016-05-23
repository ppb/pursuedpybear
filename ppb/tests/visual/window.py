"""
Window Visual Test Module

This test passes if your hardware module instantiates a window, updates to
a default screen, and closes after five seconds. It must also close in
response to a quit event handled by hitting the close button on the
window.
"""


# TODO: Turn into function to be used inside a test suite.
# TODO: Figure out how to make this test automated in a general way.

import logging

import ppb.engine
from ppb.event import Quit, Tick
from ppb.components.models import GameObject
from ppb.components.controls import Publisher
import ppb.hw as hardware

hardware.choose("pygame")
logging.basicConfig(level=logging.INFO)
hardware.init((200, 200), "Test")

publisher = Publisher(hardware)


def get_events(*_):
    hardware.update_input()


publisher.subscribe(Tick, get_events)


def quit_timer(time):
    def callback(_, event, count=[time]):
        count[0] += -1 * event.sec
        if count[0] <= 0:
            ppb.engine.message(Quit())
    return callback

clock = GameObject(behaviors=[(Tick, quit_timer(5))])

ppb.engine.run(publisher)
