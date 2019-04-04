import time
from typing import Callable

from hypothesis import strategies as st

from ppb import Vector
from ppb.engine import GameEngine
from ppb.events import Quit
from ppb.systems import System


def integer_vectors(min_value=None, max_value=None):
    return st.builds(
        Vector,
        st.integers(min_value=min_value, max_value=max_value),
        st.integers(min_value=min_value, max_value=max_value),
    )

def vectors(max_magnitude=1e75):
    return st.builds(
        Vector,
        st.floats(min_value=-max_magnitude, max_value=max_magnitude),
        st.floats(min_value=-max_magnitude, max_value=max_magnitude),
    )


class Failer(System):

    def __init__(self, *, fail: Callable[[GameEngine], bool], message: str,
                 run_time: float=1, **kwargs):
        super().__init__(**kwargs)
        self.fail = fail
        self.message = message
        self.start = time.monotonic()
        self.run_time = run_time

    def activate(self, engine):
        if time.monotonic() - self.start > self.run_time:
            raise AssertionError("Test ran too long.")
        if self.fail(engine):
            raise AssertionError(self.message)
        return ()



class Quitter(System):
    """
    System for running test. Limits the engine to a single loop.
    """

    def __init__(self, loop_count=1, **kwargs):
        super().__init__(**kwargs)
        self.counter = 0
        self.loop_count = loop_count

    def activate(self, engine):
        self.counter += 1
        if self.counter >= self.loop_count:
            yield Quit()
