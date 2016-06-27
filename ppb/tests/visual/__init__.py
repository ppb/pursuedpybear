"""
A series of visual tests to confirm a complete hardware library.

Below is a basic tree of approximate order a new library should be built in.
Indent level signifies requiring at least one of the the tests one level up
to pass.

Such dependencies will be documented in the individual files.

window.py
    keys.py
    mouse.py
    draw_square.py

"""

import logging

import ppb.engine as engine
import ppb.hw as hardware

from ppb.components.controls import Publisher
from ppb.components.view import View


logging.basicConfig(level=logging.INFO)


class Runner(Publisher):

    def __init__(self, lib):
        super(Runner, self).__init__()
        hardware.choose(lib)
        hardware.init((200, 200), "Test")
#         self.view = View() # TODO

    def set_events(self, commands):
        for command in commands:
            self.subscribe(*command)

    def run(self):
        engine.run(self)