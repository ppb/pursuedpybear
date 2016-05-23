"""
Keys Visual Test Module

Expected behaviors:

KeyDown events should print "Key {} pressed." to console.

KeyUp events should print "Key {} released." to console.

A pressed key should print "Key {} held." to console each tick.

Quit should work.
"""

import logging
import string

import ppb.engine
from ppb.event import KeyDown, KeyUp, Tick
from ppb.components.controls import Publisher
import ppb.hw as hardware

hardware.choose("sdl2")
logging.basicConfig(level=logging.INFO)
hardware.init((200, 200), "Test")

publisher = Publisher(hardware)


def get_events(*_):
    hardware.update_input()


publisher.subscribe(Tick, get_events)


def key_down(key_event):
    print("Key {} pressed.".format(key_event.name))

publisher.subscribe(KeyDown, key_down)


def key_up(key_event):
    print("Key {} released.".format(key_event.name))


publisher.subscribe(KeyUp, key_up)


def tick(_):
    for char in string.printable:
        code = ord(char)
        if hardware.keys[code]:
            print("Key {} held.".format(char))


publisher.subscribe(Tick, tick)

ppb.engine.run(publisher)