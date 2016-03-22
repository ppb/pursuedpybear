from __future__ import division

import logging
import time

import ppb.engine as engine
from ppb.event import Tick, Quit
from ppb.utilities import Publisher


logging.basicConfig(level=logging.DEBUG)


class TestController(object):

    def __init__(self, time):
        self.countdown = time
        engine.publisher.subscribe(Tick, id(self), self.tick)

    def tick(self, event):
        self.countdown += -1 * event.sec
        if self.countdown <= 0:
            engine.event_queue.push(Quit())


class TestView(object):

    def __init__(self, target_fps):
        self.target_render_time = 1/target_fps
        self.countdown = self.target_render_time
        self.count = 0
        engine.publisher.subscribe(Tick, id(self), self.tick)

    def tick(self, event):
        self.countdown += -1 * event.sec
        if self.countdown <= 0:
            self.countdown = self.target_render_time
            self.count += 1
            print("Frame {} rendered at {}".format(self.count, time.time()))


class Scene(Publisher):
    pass


if __name__ == "__main__":
    controller = TestController(1)
    print("Controller created.")
    view = TestView(60)
    print("View created.")
    engine.run(Scene())
