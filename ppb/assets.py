from typing import Tuple

from pygame import Surface
from pygame import draw

from ppb.assetlib import AbstractAsset

__all__ = (
    "Square",
    "Triangle"
)

BLACK = 0, 0, 0
MAGENTA = 255, 71, 182
DEFAULT_SPRITE_SIZE = 64
DEFAULT_SPRITE_RESOLUTION = DEFAULT_SPRITE_SIZE, DEFAULT_SPRITE_SIZE


def _create_surface(color):
    """
    Creates a surface for assets and sets the color key.
    """
    surface = Surface(DEFAULT_SPRITE_RESOLUTION)
    color_key = BLACK if color != BLACK else MAGENTA
    surface.set_colorkey(color_key)
    surface.fill(color_key)
    return surface


class Shape(AbstractAsset):
    """Shapes are drawing primitives that are good for rapid prototyping."""

    def __init__(self, red: int, green: int, blue: int):
        color = red, green, blue
        self._surface = _create_surface(color)
        self.modify_surface(color)

    def load(self) -> Surface:
        """Return the underlying asset."""
        return self._surface

    def modify_surface(self, color: Tuple[int, int, int]) -> None:
        """
        Modify the raw asset to match the intended shape.

        Must modify in place.
        """


class Square(Shape):
    """
    A square image of a single color.
    """

    def modify_surface(self, color):
        self._surface.fill(color)


class Triangle(Shape):
    """
    A triangle image of a single color.
    """

    def modify_surface(self, color):
        draw.polygon(self._surface, color,
                     [
                         (0, DEFAULT_SPRITE_SIZE),
                         (DEFAULT_SPRITE_SIZE / 2, 0),
                         (DEFAULT_SPRITE_SIZE, DEFAULT_SPRITE_SIZE)
                     ])


class Circle(Shape):
    """
    A circle image of a single color.
    """

    def modify_surface(self, color):
        half = int(DEFAULT_SPRITE_SIZE / 2)
        draw.circle(self._surface, color, (half, half), half)
