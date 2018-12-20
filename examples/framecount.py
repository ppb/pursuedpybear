"""
A simple test script to make sure the ppb.engine is behaving as expected.

At logging.INFO the primary output is a string:

"Frame # rendered at #"
"""

import logging
import time
import ppb


class TestScene(ppb.BaseScene):
    """
    A view that prints a test line in place of rendering frames.
    """

    duration = 1.0

    def __init__(self, *p, **kw):
        super().__init__(*p, **kw)

        self.frames = 0
        self.start_time = time.monotonic()

    def on_update(self, event, signal):
        """
        Fires at the update rate (~60 times a second)
        """
        t = time.monotonic() - self.start_time
        if t >= self.duration:
            signal(ppb.events.Quit())

    def on_pre_render(self, event, signal):
        """
        Fires each frame.

        The frame rate is variable and different from the update rate.
        """
        t = time.monotonic() - self.start_time
        self.frames += 1
        print(f"Frame {self.frames} rendered at {t}")


if __name__ == "__main__":
    ppb.run(starting_scene=TestScene, log_level=logging.INFO)
