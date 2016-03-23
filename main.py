from __future__ import division

import logging
import time

import ppb.engine as engine
from ppb.event import Tick, Quit
from ppb.utilities import Publisher


logging.basicConfig(level=logging.INFO)


class TestController(object):

    def __init__(self, scene, time):
        self.countdown = time
        scene.subscribe(Tick, id(self), self.tick)

    def tick(self, event):
        self.countdown += -1 * event.sec
        if self.countdown <= 0:
            engine.event_queue.push(Quit())


class TestView(object):

    def __init__(self, scene, target_fps):
        self.target_render_time = 1/target_fps
        self.countdown = self.target_render_time
        self.count = 0
        scene.subscribe(Tick, id(self), self.tick)

    def tick(self, event):
        self.countdown += -1 * event.sec
        if self.countdown <= 0:
            self.countdown = self.target_render_time
            self.count += 1
            print("Frame {} rendered at {}".format(self.count, time.time()))


class Scene(Publisher):
    pass


if __name__ == "__main__":
    scene = Publisher()
    controller = TestController(scene, 1)
    print("Controller created.")
    view = TestView(scene, 60)
    print("View created.")
    engine.run(scene)
