from typing import Callable

from ppb.vector import Vector


class Mouse:
    """
    Object interface to the hardware mouse.

    """
    def __init__(self, press_function: Callable=None,
                 move_function: Callable=None, move_to_function: Callable=None):
        self.position = Vector(0, 0)
        self.screen_position = Vector(0, 0)
        self.buttons = [False, False, False]

        self.press_function = press_function or _not_implemented
        self.move_function = move_function or _not_implemented
        self.move_to_function = move_to_function or _not_implemented

    @property
    def left_button(self) -> bool:
        return self.buttons[0]

    @property
    def right_button(self) -> bool:
        return self.buttons[2]

    def press(self, button: int) -> None:
        try:
            self.press_function(button)
        except NotImplementedError:
            raise FeatureNotProvided("Your hardware library did not include a Mouse.press function.")

    def move(self, vector: Vector) -> None:
        try:
            self.move_function(vector)
        except NotImplementedError:
            raise FeatureNotProvided("Your hardware library did not include a Mouse.move function.")

    def move_to(self, position: Vector) -> None:
        try:
            self.move_to_function(position)
        except NotImplementedError:
            raise FeatureNotProvided("Your hardware library did not include a Mouse.move_to function.")


class FeatureNotProvided(Exception):
    pass


def _not_implemented(*_):
    raise NotImplementedError
