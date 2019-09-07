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
    asset = Surface(DEFAULT_SPRITE_RESOLUTION)
    color_key = BLACK if color != BLACK else MAGENTA
    asset.set_colorkey(color_key)
    asset.fill(color_key)
    return asset


class Shape(AbstractAsset):
    """Shapes are drawing primitives that are good for rapid prototyping."""

    def __init__(self, red, green, blue):
        color = red, green, blue
        self._asset = _create_surface(color)
        self.modify_asset(color)

    def load(self):
        """Return the underlying asset."""
        return self._asset

    def modify_asset(self, color):
        """To be handled by subclasses."""


class Square(Shape):
    """
    A square image of a single color.
    """

    def modify_asset(self, color):
        self._asset.fill(color)


class Triangle(Shape):
    """
    A triangle image of a single color.
    """

    def modify_asset(self, color):
        draw.polygon(self._asset, color,
                     [
                         (0, DEFAULT_SPRITE_SIZE),
                         (DEFAULT_SPRITE_SIZE / 2, 0),
                         (DEFAULT_SPRITE_SIZE, DEFAULT_SPRITE_SIZE)
                     ])


class Circle(Shape):
    """
    A circle image of a single color.
    """

    def modify_asset(self, color):
        half = int(DEFAULT_SPRITE_SIZE / 2)
        draw.circle(self._asset, color, (half, half), half)
