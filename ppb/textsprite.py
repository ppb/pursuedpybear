from functools import wraps
from typing import Tuple, Union

from ppb_vector import Vector

from ppb.events import PreRender
from ppb.sprites import BaseSprite, RenderableMixin
from ppb.systems.text import Font, Text


def realized_read(func):

    @wraps(func)
    def wrapper(self: 'TextSprite'):
        if not self.realized:
            self.realize()
        return func(self)

    return wrapper


def realized_write(func):

    @wraps(func)
    def wrapper(self: 'TextSprite', value):
        if self.realized:
            return func(self, value)
        self._commands.append((func.__name__, value))
    return wrapper


class TextSprite(RenderableMixin, BaseSprite):
    """
    A sprite for working with text.

    TextSprite is more magical than most sprites because it tries to maintain
    its aspect ratio to the rendered text associated with it. Otherwise, it
    should fit the same API as a Renderable Rectangle Sprite.
    """
    _text: str = ""
    color: Tuple[int, int, int] = (255, 229, 0)
    font: Font = None
    realized: bool = False
    _rendered_text: str = None
    _half_height = 0
    _half_width = 0
    _image_width_pixels: int = None
    _image_height_pixels: int = None
    _target_height = 1
    _target_width = None
    _pixel_ratio = 0
    rotation = 0
    size = 1

    def __init__(self, text="", **kwargs):
        self._commands = []
        super().__init__(**kwargs)
        if self.font is None:
            raise ValueError("A Font is required.")
        self.text = text

    def on_pre_render(self, event: PreRender, signal):
        # Attempt to realize sprite.
        self.realize()

    def render(self):
        if self._rendered_text != self.text:
            assert self.font is not None
            self.image = Text(self.text, font=self.font, color=self.color)
            self._rendered_text = self.text
            self.realized = False

    def set_dimensions(self):
        if self._target_height is not None:
            self._pixel_ratio = self._target_height / self._image_height_pixels
        elif self._target_width is not None:
            self._pixel_ratio = self._target_width / self._image_width_pixels

        self._half_width = self._image_width_pixels * self._pixel_ratio
        self._half_height = self._image_height_pixels * self._pixel_ratio

    def realize(self):
        if self.realized:
            return
        self._image_width_pixels, self._image_height_pixels = self.image.resolution()
        self.set_dimensions()

        self.realized = True

        for attr, value in self._commands:
            setattr(self, attr, value)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
        self.render()

    @property
    @realized_read
    def top(self):
        return self.position.y + self._half_height

    @top.setter
    @realized_write
    def top(self, value: Union[int, float]):
        self.position = Vector(self.position.x, value - self._half_height)


    @property
    @realized_read
    def bottom(self):
        return self.position.y - self._half_height

    @bottom.setter
    @realized_write
    def bottom(self, value: Union[int, float]):
        self.position = Vector(self.position.x, value + self._half_height)

    @property
    @realized_read
    def left(self):
        return self.position.x - self._half_width

    @left.setter
    @realized_write
    def left(self, value: Union[int, float]):
        self.position = Vector(value + self._half_width, self.position.y)

    @property
    @realized_read
    def right(self):
        return self.position.x + self._half_width

    @right.setter
    @realized_write
    def right(self, value: Union[int, float]):
        self.position = Vector(value - self._half_width, self.position.y)

    @property
    @realized_read
    def width(self):
        return self._half_width * 2

    @width.setter
    @realized_write
    def width(self, value):
        self._target_width = value
        self._target_height = None
        self.set_dimensions()

    @property
    @realized_read
    def height(self):
        return self._half_height * 2

    @height.setter
    @realized_write
    def height(self, value):
        self._target_width = None
        self._target_height = value
        self.set_dimensions()
