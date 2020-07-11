"""
Sprites are game objects.

To use a sprite you use :meth:`BaseScene.add <ppb.BaseScene.add>` to add it
to a scene. When contained in an active scene, the engine will call the various
:mod:`event <ppb.events>` handlers on the sprite.

When defining your own custom sprites, we suggest you start with
:class:`~ppb.Sprite`. By subclassing :class:`~ppb.Sprite`, you get a number of
features automatically. You then define your event handlers as methods on your
new class to produce behaviors.

All sprites in ppb are built from composition via mixins or subclassing via
traditional Python inheritance.

If you don't need the built in features of :class:`~ppb.Sprite` see
:class:`BaseSprite`.
"""
from inspect import getfile
from pathlib import Path
from typing import Union

from ppb_vector import Vector, VectorLike

import ppb
import ppb.gomlib

__all__ = (
    "BaseSprite",
    "Sprite",
    "RotatableMixin",
    "SquareShapeMixin",
    "RectangleShapeMixin",
    "RectangleSprite",
    "RenderableMixin",
)


class BaseSprite(ppb.gomlib.GameObject):
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

    def __init__(self, *, pos=None, **props):
        """
        :class:`BaseSprite` does not accept any positional arguments, and uses
        keyword arguments to set arbitrary state to the :class:`BaseSprite`
        instance. This allows rapid prototyping.

        Example: ::

           sprite = BaseSprite(speed=6)
           print(sprite.speed)

        This sample will print the numeral 6.

        You may add any arbitrary data values in this fashion. Alternatively,
        it is considered best practice to subclass :class:`BaseSprite` and set
        the default values of any required attributes as class attributes.

        Example: ::

           class Rocket(ppb.sprites.BaseSprite):
              velocity = Vector(0, 1)

              def on_update(self, update_event, signal):
                  self.position += self.velocity * update_event.time_delta
        """
        # Appreviations
        if pos is not None:
            if 'position' in props:
                raise TypeError("pos and position were both given to Sprite")
            props['position'] = pos

        super().__init__(**props)

        # Type coercion
        self.position = Vector(self.position)


class RenderableMixin:
    """
    A class implementing the API expected by ppb.systems.renderer.Renderer.

    The render expects a width and height (see :class:`RectangleMixin`) and will
    skip rendering if a sprite has no shape. You can use
    :class:`RectangleMixin`, :class:`SquareMixin`, or set the values yourself.

    Additionally, if :attr:`~RenderableMixin.image` is ``None``, the sprite will not
    be rendered. If you just want a basic shape to be rendered, see
    :mod:`ppb.assets`.
    """
    #: (:py:class:`ppb.Image`): The image asset
    image = ...  # TODO: Type hint appropriately
    size = 1
    blend_mode: 'ppb.flags.BlendMode' # One of four blending modes
    opacity: int # An opacity value from 0-255
    color: 'ppb.utils.Color' # A 3-tuple color with values 0-255

    def __image__(self):
        """
        Returns the sprite's image attribute if provided, or sets a default
        one.
        """
        if self.image is ...:
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
    A rotation mixin. Can be included with sprites.

    .. warning:: rotation does not affect underlying shape (the corners are still in the same place), it only rotates
       the sprites image and provides a facing.
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
        The direction the "front" is facing.

        Can be set to an arbitrary facing by providing a facing vector.
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

    Classes derived from RectangleShapeMixin default to the same size and
    shape as all ppb Sprites: A 1 game unit by 1 game unit square. Just set
    the width and height in your constructor (Or as
    :class:`class attributes <BaseSprite>`) to change this default.

    .. note:: The concrete class using :class:`RectangleShapeMixin` must have a
       ``position`` attribute.
    """
    #: The width of the sprite.
    width: int = 1
    #: The height of the sprite.
    height: int = 1
    # Following class properties for type hinting only. Your concrete sprite
    # should already have one.
    position: Vector

    @property
    def left(self) -> float:
        """
        The x-axis position of the left side of the object.

        Can be set to a number.
        """
        return self.position.x - self.width / 2

    @left.setter
    def left(self, value: Union[float, int]):
        self.position = Vector(value + (self.width / 2), self.position.y)

    @property
    def right(self) -> float:
        """
        The x-axis position of the right side of the object.

        Can be set to a number.
        """
        return self.position.x + self.width / 2

    @right.setter
    def right(self, value: Union[float, int]):
        self.position = Vector(value - (self.width / 2), self.position.y)

    @property
    def top(self) -> float:
        """
        The y-axis position of the top of the object.

        Can be set to a number.
        """
        return self.position.y + self.height / 2

    @top.setter
    def top(self, value: Union[int, float]):
        self.position = Vector(self.position.x, value - (self.height / 2))

    @property
    def bottom(self) -> float:
        """
        The y-axis position of the bottom of the object.

        Can be set to a number.
        """
        return self.position.y - self.height / 2

    @bottom.setter
    def bottom(self, value: Union[float, int]):
        self.position = Vector(self.position.x, value + (self.height / 2))

    @property
    def top_left(self) -> Vector:
        """
        The coordinates of the top left corner of the object.

        Can be set to a :class:`ppb_vector.Vector`.
        """
        return Vector(self.left, self.top)

    @top_left.setter
    def top_left(self, vector: Vector):
        vector = Vector(vector)
        x = vector.x + (self.width / 2)
        y = vector.y - (self.height / 2)
        self.position = Vector(x, y)

    @property
    def top_right(self) -> Vector:
        """
        The coordinates of the top right corner of the object.

        Can be set to a :class:`ppb_vector.Vector`.
        """
        return Vector(self.right, self.top)

    @top_right.setter
    def top_right(self, vector: Vector):
        vector = Vector(vector)
        x = vector.x - (self.width / 2)
        y = vector.y - (self.height / 2)
        self.position = Vector(x, y)

    @property
    def bottom_left(self) -> Vector:
        """
        The coordinates of the bottom left corner of the object.

        Can be set to a :class:`ppb_vector.Vector`.
        """
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
        """
        The coordinates of the bottom right corner of the object.

        Can be set to a :class:`ppb_vector.Vector`.
        """
        vector = Vector(vector)
        x = vector.x - (self.width / 2)
        y = vector.y + (self.height / 2)
        self.position = Vector(x, y)

    @property
    def bottom_middle(self) -> Vector:
        """
        The coordinates of the midpoint of the bottom of the object.

        Can be set to a :class:`ppb_vector.Vector`.
        """
        return Vector(self.position.x, self.bottom)

    @bottom_middle.setter
    def bottom_middle(self, value: VectorLike):
        value = Vector(value)
        self.position = Vector(value.x, value.y + self.height / 2)

    @property
    def left_middle(self) -> Vector:
        """
        The coordinates of the midpoint of the left side of the object.

        Can be set to a :class:`ppb_vector.Vector`.
        """
        return Vector(self.left, self.position.y)

    @left_middle.setter
    def left_middle(self, value: VectorLike):
        value = Vector(value)
        self.position = Vector(value.x + self.width / 2, value.y)

    @property
    def right_middle(self) -> Vector:
        """
        The coordinates of the midpoint of the right side of the object.

        Can be set to a :class:`ppb_vector.Vector`.
        """
        return Vector(self.right, self.position.y)

    @right_middle.setter
    def right_middle(self, value: VectorLike):
        value = Vector(value)
        self.position = Vector(value.x - self.width / 2, value.y)

    @property
    def top_middle(self) -> Vector:
        """
        The coordinates of the midpoint of the top of the object.

        Can be set to a :class:`ppb_vector.Vector`.
        """
        return Vector(self.position.x, self.top)

    @top_middle.setter
    def top_middle(self, value: VectorLike):
        value = Vector(value)
        self.position = Vector(value.x, value.y - self.height / 2)

    @property
    def center(self) -> Vector:
        """
        The coordinates of the center point of the object. Equivalent to the
        :attr:`~BaseSprite.position`.

        Can be set to a :class:`ppb_vector.Vector`.
        """
        return self.position

    @center.setter
    def center(self, vector: Vector):
        self.position = Vector(vector)


class SquareShapeMixin(RectangleShapeMixin):
    """
    A Mixin that provides a square area to sprites.

    Extends the interface of :class:`RectangleShapeMixin` by using the
    :attr:`~SquareShapeMixin.size` attribute to determine
    :meth:`~SquareShapeMixin.width` and :meth:`~SquareShapeMixin.height`.
    Setting either :meth:`~SquareShapeMixin.width` or
    :meth:`~SquareShapeMixin.height` sets the
    :attr:`~SquareShapeMixin.size` and maintains the square shape at the new
    size.

    The default size of :class:`SquareShapeMixin` is 1 game unit.

    Please see :class:`RectangleShapeMixin` for additional details.
    """
    #: The width and height of the object. Setting size changes the
    #: :meth:`height` and :meth:`width` of the sprite.
    size = 1

    @property
    def width(self):
        """
        The width of the sprite.

        Setting the width of the sprite changes :attr:`size` and :meth:`height`.
        """
        return self.size

    @width.setter
    def width(self, value: Union[float, int]):
        self.size = value

    @property
    def height(self):
        """
        The height of the sprite.

        Setting the height of the sprite changes the :attr:`size` and
        :meth:`width`.
        """
        return self.size

    @height.setter
    def height(self, value: Union[float, int]):
        self.size = value


class Sprite(SquareShapeMixin, RenderableMixin, RotatableMixin, BaseSprite):
    """
    The default Sprite class.

    Sprite defines no additional methods or attributes, but is made up of
    :class:`BaseSprite` with the mixins :class:`~ppb.sprites.RotatableMixin`,
    :class:`~ppb.sprites.RenderableMixin`, and
    :class:`~ppb.sprites.SquareShapeMixin`.

    For most use cases, this is probably the class you want to subclass to make
    your game objects.

    If you need rectangular sprites instead of squares, see
    :class:`RectangleSprite`.
    """


class RectangleSprite(RectangleShapeMixin, RenderableMixin, RotatableMixin, BaseSprite):
    """
    A rectangle sprite.

    Similarly to :class:`~ppb.Sprite`, :class:`RectangleSprite` does not
    introduce any new methods or attributes. It's made up of :class:`BaseSprite`
    with the mixins :class:`RotatableMixin`, :class:`RenderableMixin`, and
    :class:`RectangleShapeMixin`.
    """
