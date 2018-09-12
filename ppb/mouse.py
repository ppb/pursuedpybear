from functools import partial
from typing import Callable

from ppb.vector import Vector

PRESS_ERROR = "Your hardware library did not include a Mouse.press function."
MOVE_ERROR = "Your hardware library did not include a Mouse.move function."
MOVE_TO_ERROR = "Your hardware library did not include a Mouse.move_to function."

class Mouse:
    """
    Object interface to the hardware mouse.

    """
    def __init__(self, press_function: Callable[[int], None]=None,
                 move_function: Callable[[Vector], None]=None,
                 move_to_function: Callable[[Vector], None]=None):
        self.position = Vector(0, 0)
        self.screen_position = Vector(0, 0)
        self.buttons = [False, False, False]

        self.press = press_function or partial(_not_implemented, PRESS_ERROR)
        self.move = move_function or partial(_not_implemented, MOVE_ERROR)
        self.move_to = move_to_function or partial(_not_implemented, MOVE_TO_ERROR)

    @property
    def left_button(self) -> bool:
        return self.buttons[0]

    @property
    def right_button(self) -> bool:
        return self.buttons[2]


class FeatureNotProvided(NotImplementedError):
    """The hardware library being depended on does not include some functionality."""
    pass


def _not_implemented(message, *_):
    raise FeatureNotProvided(message)
