"""
A simple test script to make sure the ppb.engine is behaving as expected.

At logging.INFO the primary output is a string:

"Frame # rendered at #"
"""

from __future__ import division
# float division is the expected.

import logging
import time
# logging is primarily to set the logging level. Can also be inserted into
# the sample model and view.
# time is used by the view to print the unix time stamp.

import ppb.engine as engine
from ppb.event import Tick, Quit
from ppb.utilities import Publisher
# import ppb.engine is the primary import.
# ppb.event to grab any events you plan to listen to.
# ppb.utilities has multiple base classes used throughout the library.
# in this case we'll be using a Publisher as a scene.


logging.basicConfig(level=logging.INFO)
# Set the logging level


class TestController(object):
    """
    A controller that raises a Quit event after the given time.
    """

    def __init__(self, scene, length):
        """
        Pass in the scene and the number of seconds to run the
        script.

        :param scene: Publisher
        :param length: number
        :return: TestController
        """
        self.countdown = length
        # need to keep track of how much time is left.
        # Alternatively could keep the time to run and accumulate.

        scene.subscribe(Tick, id(self), self.tick)
        # subscribe to Tick events with the scene.

    def tick(self, event):
        """
        Advance the countdown and raise a Quit event when complete.

        :param event: Tick
        :return:
        """
        self.countdown += -1 * event.sec
        # Advance countdown. Use -1 * time to be compatible with Python2

        if self.countdown <= 0:
            engine.message(Quit())
            # Raise the quit event.


class TestView(object):
    """
    A view that prints a test line in place of rendering frames.
    """

    def __init__(self, scene, target_fps):
        """

        :param scene: Publisher
        :param target_fps: number of frames per second to render
        :return:
        """
        self.target_render_time = 1/target_fps
        # Get amount of time between render calls.

        self.countdown = self.target_render_time
        # A countdown to control render speed.
        self.count = 0
        # A simple accumulator to count frames.
        scene.subscribe(Tick, id(self), self.tick)
        # Subscribe to the scene.

    def tick(self, event):
        """
        Advance render countdown, render, and reset counter.

        :param event: Tick
        :return:
        """
        self.countdown += -1 * event.sec
        # Advance countdown. Use -1 * time to be compatible with Python2

        if self.countdown <= 0:
            self.countdown = self.target_render_time
            # Reset the countdown.
            self.count += 1
            # Advance frame count.
            print("Frame {} rendered at {}".format(self.count, event.run_time))
            # Render information


if __name__ == "__main__":
    _scene = Publisher()
    # We need a publisher.
    _controller = TestController(_scene, 1)
    # Set up a controller. The sample runs for one second.
    logging.info("Controller created.")
    _view = TestView(_scene, 60)
    # Set up a view. The view runs at 60 FPS.
    logging.info("View created.")
    engine.run(_scene)
    # Run the engine, giving it the first scene.
