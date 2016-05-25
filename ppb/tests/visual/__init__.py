import logging

import ppb.engine as engine
import ppb.hw as hardware

from ppb.components.controls import Publisher


logging.basicConfig(level=logging.INFO)


class Runner(Publisher):

    def __init__(self, lib):
        super(Runner, self).__init__()
        hardware.choose(lib)
        hardware.init((200, 200), "Test")

    def set_events(self, commands):
        for command in commands:
            self.subscribe(*command)

    def run(self):
        engine.run(self)