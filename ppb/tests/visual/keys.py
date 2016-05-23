"""
Keys visual test module

On KeyDown:
        Print "Key {name} pressed."

On KeyUp:
    Print "Key {name} released."

On Tick:
    Print ""Key {name} held."
"""

import logging
import string

from ppb.event import KeyDown, KeyUp, Tick
import ppb.hw as hardware
from ppb.tests.visual import Runner

logging.basicConfig(level=logging.INFO)


def key_down(key_event):
    print("Key {} pressed.".format(key_event.name))


def key_up(key_event):
    print("Key {} released.".format(key_event.name))


def tick(_):
    for char in string.printable:
        code = ord(char)
        if hardware.keys[code]:
            print("Key {} held.".format(char))


test_runner = Runner("sdl2")
test_runner.set_events([(KeyDown, key_down), (KeyUp, key_up), (Tick, tick)])
test_runner.run()
