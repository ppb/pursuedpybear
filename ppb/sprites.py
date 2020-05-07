"""
Sprites are game objects.

In ppb all sprites are built from composition via mixins or subclassing via
traditional Python inheritance. Sprite is provided as a default expectation
used in ppb.

If you intend to build your own set of expectation, see BaseSprite.
"""
from inspect import getfile
from pathlib import Path
from typing import Union

from ppb_vector import Vector, VectorLike

import ppb

__all__ = (
    "BaseSprite",
    "Sprite",
    "RotatableMixin",
    "SquareShapeMixin",
    "RectangleShapeMixin",
    "RectangleSprite",
    "RenderableMixin",
)


class BaseSprite:
    """
    The base Sprite class. All sprites should inherit from this (directly or
    indirectly).

    The things that define a BaseSprite:

    * A position vector
    * A layer

    BaseSprite provides an :py:meth:`__init__()` method that sets attributes
    based on kwargs to make rapid prototyping easier.
    """
    #: (:py:class:`ppb.Vector`): Location of the sprite
    position: Vector = Vector(0, 0)
    #: The layer a sprite exists on.
    layer: int = 0

    def __init__(self, **kwargs):
        super().__init__()

        self.position = Vector(self.position)

        # Initialize things
        for k, v in kwargs.items():
            # Abbreviations
            if k == 'pos':
                k = 'position'
            # Castings
            if k == 'position':
                v = Vector(v)
            setattr(self, k, v)


class RenderableMixin:
    """
    A class implementing the API expected by ppb.systems.renderer.Renderer.

    You should include RenderableMixin before BaseSprite in your parent
    class definitions.
    """
    #: (:py:class:`ppb.Image`): The image asset
    image = None  # TODO: Type hint appropriately
    size = 1

    def __image__(self):
        """
        Returns the sprite's image attribute if provided, or sets a default
        one.
        """
        if self.image is None:
            klass = type(self)
            prefix = Path(klass.__module__.replace('.', '/'))
            try:
                klassfile = getfile(klass)
            except TypeError:
                prefix = Path('.')
            else:
                if Path(klassfile).name != '__init__.py':
                    prefix = prefix.parent
            if prefix == Path('.'):
                self.image = ppb.Image(f"{klass.__name__.lower()}.png")
            else:
                self.image = ppb.Image(f"{prefix!s}/{klass.__name__.lower()}.png")
        return self.image


class RotatableMixin:
    """
    A simple rotation mixin. Can be included with sprites.
    """
    _rotation = 0
    # This is necessary to make facing do the thing while also being adjustable.
    #: The baseline vector, representing the "front" of the sprite
    basis = Vector(0, -1)
    # Considered making basis private, the only reason to do so is to
    # discourage people from relying on it as data.

    @property
    def facing(self):
        """
        The direction the "front" is facing
        """
        return Vector(*self.basis).rotate(self.rotation).normalize()

    @facing.setter
    def facing(self, value):
        self.rotation = self.basis.angle(value)

    @property
    def rotation(self):
        """
        The amount the sprite is rotated, in degrees
        """
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value % 360

    def rotate(self, degrees):
        """
        Rotate the sprite by a given angle (in degrees).
        """
        self.rotation += degrees


class RectangleShapeMixin:
    """
    A Mixin that provides a rectangular area to sprites.

    You should include RectangleShapeMixin before your BaseSprite in your
    parent classes.

    Classes derived from RectangleShapeMixin default to the same size and
    shape as all ppb Sprites: A 1 game unit by 1 game unit square. Just set
    the width and height in your constructor (Or as class attributes) to
    change this default.
    """
    width: int = 1
    height: int = 1
    # Following class properties for type hinting only. Your concrete sprite
    # should already have one.
    position: Vector

    @property
    def left(self) -> float:
        return self.position.x - self.width / 2

    @left.setter
    def left(self, value: Union[float, int]):
        self.position = Vector(value + (self.width / 2), self.position.y)

    @property
    def right(self) -> float:
        return self.position.x + self.width / 2

    @right.setter
    def right(self, value: Union[float, int]):
        self.position = Vector(value - (self.width / 2), self.position.y)

    @property
    def top(self) -> float:
        return self.position.y + self.height / 2

    @top.setter
    def top(self, value: Union[int, float]):
        self.position = Vector(self.position.x, value - (self.height / 2))

    @property
    def bottom(self) -> float:
        return self.position.y - self.height / 2

    @bottom.setter
    def bottom(self, value: Union[float, int]):
        self.position = Vector(self.position.x, value + (self.height / 2))

    @property
    def top_left(self) -> Vector:
        return Vector(self.left, self.top)

    @top_left.setter
    def top_left(self, vector: Vector):
        vector = Vector(vector)
        x = vector.x + (self.width / 2)
        y = vector.y - (self.height / 2)
        self.position = Vector(x, y)

    @property
    def top_right(self) -> Vector:
        return Vector(self.right, self.top)

    @top_right.setter
    def top_right(self, vector: Vector):
        vector = Vector(vector)
        x = vector.x - (self.width / 2)
        y = vector.y - (self.height / 2)
        self.position = Vector(x, y)

    @property
    def bottom_left(self) -> Vector:
        return Vector(self.left, self.bottom)

    @bottom_left.setter
    def bottom_left(self, vector: Vector):
        vector = Vector(vector)
        x = vector.x + (self.width / 2)
        y = vector.y + (self.height / 2)
        self.position = Vector(x, y)

    @property
    def bottom_right(self) -> Vector:
        return Vector(self.right, self.bottom)

    @bottom_right.setter
    def bottom_right(self, vector: Vector):
        vector = Vector(vector)
        x = vector.x - (self.width / 2)
        y = vector.y + (self.height / 2)
        self.position = Vector(x, y)

    @property
    def bottom_middle(self) -> Vector:
        return Vector(self.position.x, self.bottom)

    @bottom_middle.setter
    def bottom_middle(self, value: VectorLike):
        value = Vector(value)
        self.position = Vector(value.x, value.y + self.height / 2)

    @property
    def left_middle(self) -> Vector:
        return Vector(self.left, self.position.y)

    @left_middle.setter
    def left_middle(self, value: VectorLike):
        value = Vector(value)
        self.position = Vector(value.x + self.width / 2, value.y)

    @property
    def right_middle(self) -> Vector:
        return Vector(self.right, self.position.y)

    @right_middle.setter
    def right_middle(self, value: VectorLike):
        value = Vector(value)
        self.position = Vector(value.x - self.width / 2, value.y)

    @property
    def top_middle(self) -> Vector:
        return Vector(self.position.x, self.top)

    @top_middle.setter
    def top_middle(self, value: VectorLike):
        value = Vector(value)
        self.position = Vector(value.x, value.y - self.height / 2)

    @property
    def center(self) -> Vector:
        return self.position

    @center.setter
    def center(self, vector: Vector):
        self.position = Vector(vector)


class SquareShapeMixin(RectangleShapeMixin):
    """
    A Mixin that provides a square area to sprites.

    Extends the interface of :class:`RectangleShapeMixin` by using the ``size``
    attribute to determine width and height. Setting either ``width`` or
    ``height`` sets the ``size`` and maintains the square shape at the new size.

    The default size of :class:`SquareShapeMixin` is 1 game unit.
    """
    size = 1

    @property
    def width(self):
        return self.size

    @width.setter
    def width(self, value: Union[float, int]):
        self.size = value

    @property
    def height(self):
        return self.size

    @height.setter
    def height(self, value: Union[float, int]):
        self.size = value


class Sprite(SquareShapeMixin, RenderableMixin, RotatableMixin, BaseSprite):
    """
    The default Sprite class.

    Sprite includes:

    * BaseSprite
    * SquareShapeMixin
    * RenderableMixin
    * RotatableMixin

    New in 0.7.0: Use this in place of BaseSprite in your games.
    """


class RectangleSprite(RectangleShapeMixin, RenderableMixin, RotatableMixin, BaseSprite):
    """
    A rectangle sprite.

    Sprite includes:

    * BaseSprite
    * RectangleShapeMixin
    * RenderableMixin
    * RotatableMixin
    """
