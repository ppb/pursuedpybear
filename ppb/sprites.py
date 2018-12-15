from inspect import getfile
from numbers import Number
from os.path import realpath
from pathlib import Path
from typing import Dict, Iterable, AnyStr, Sequence
from typing import Union

from ppb import Vector
from ppb.events import EventMixin


TOP = "top"
BOTTOM = "bottom"
LEFT = "left"
RIGHT = "right"

error_message = "'{klass}' object does not have attribute '{attribute}'"
side_attribute_error_message = error_message.format


class Side:
    sides = {
        LEFT: ('x', -1),
        RIGHT: ('x', 1),
        TOP: ('y', -1),
        BOTTOM: ('y', 1)
    }

    def __init__(self, parent: 'BaseSprite',side: AnyStr):
        self.side = side
        self.parent = parent

    def __repr__(self):
        return "Side({}, {})".format(self.parent, self.side)

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return other + self.value

    def __sub__(self, other):
        return self.value - other

    def __rsub__(self, other):
        return other - self.value

    def __eq__(self, other):
        return self.value == other

    def __le__(self, other):
        return self.value <= other

    def __ge__(self, other):
        return self.value >= other

    def __ne__(self, other):
        return self.value != other

    def __gt__(self, other):
        return self.value > other

    def __lt__(self, other):
        return self.value < other

    @property
    def value(self):
        coordinate, multiplier = self.sides[self.side]
        offset = self.parent._offset_value
        return self.parent.position[coordinate] + (offset * multiplier)

    @property
    def top(self):
        self._attribute_gate(TOP, [TOP, BOTTOM])
        return Vector(self.value, self.parent.top.value)

    @top.setter
    def top(self, value):
        self._attribute_gate(TOP, [TOP, BOTTOM])
        setattr(self.parent, self.side, value[0])
        self.parent.top = value[1]

    @property
    def bottom(self):
        self._attribute_gate(BOTTOM, [TOP, BOTTOM])
        return Vector(self.value, self.parent.bottom.value)

    @bottom.setter
    def bottom(self, value):
        self._attribute_gate(BOTTOM, [TOP, BOTTOM])
        setattr(self.parent, self.side, value[0])
        self.parent.bottom = value[1]

    @property
    def left(self):
        self._attribute_gate(LEFT, [LEFT, RIGHT])
        return Vector(self.parent.left.value, self.value)

    @left.setter
    def left(self, value):
        self._attribute_gate(LEFT, [LEFT, RIGHT])
        setattr(self.parent, self.side, value[1])
        self.parent.left = value[0]

    @property
    def right(self):
        self._attribute_gate(RIGHT, [LEFT, RIGHT])
        return Vector(self.parent.right.value, self.value)

    @right.setter
    def right(self, value):
        self._attribute_gate(RIGHT, [LEFT, RIGHT])
        setattr(self.parent, self.side, value[1])
        self.parent.right = value[0]

    @property
    def center(self):
        if self.side in (TOP, BOTTOM):
            return Vector(self.parent.center.x, self.value)
        else:
            return Vector(self.value, self.parent.center.y)

    @center.setter
    def center(self, value):
        if self.side in (TOP, BOTTOM):
            setattr(self.parent, self.side, value[1])
            self.parent.center.x = value[0]
        else:
            setattr(self.parent, self.side, value[0])
            self.parent.position.y = value[1]

    def _attribute_gate(self, attribute, bad_sides):
        if self.side in bad_sides:
            name = type(self).__name__
            message = side_attribute_error_message(klass=name,
                                                   attribute=attribute)
            raise AttributeError(message)


class BaseSprite(EventMixin):
    """
    The base Sprite class. All sprites should inherit from this (directly or
    indirectly).

    Attributes:
    * image (str): The image file
    * resource_path (pathlib.Path): The path that image is relative to
    * position: Location of the sprite
    * facing: The direction of the "top" of the sprite (rendering only)
    * size: The width/height of the sprite (sprites are square)
    """
    image = None
    resource_path = None
    position: Vector = Vector(0, 0)
    facing: Vector = Vector(0, -1)
    size: Union[int, float] = 1

    def __init__(self, **kwargs):
        super().__init__()

        # Make these instance properties with fresh instances
        # Don't use Vector.convert() because we need copying
        self.position = Vector(*self.position)
        self.facing = Vector(*self.facing)

        # Initialize things
        for k, v in kwargs.items():
            # Abbreviations
            if k == 'pos':
                k = 'position'
            # Castings
            if k in ('position', 'facing'):
                v = Vector(*v)  # Vector.convert() when that ships.
            setattr(self, k, v)

        # Trigger some calculations
        self.size = self.size

    @property
    def center(self) -> Vector:
        return self.position

    @center.setter
    def center(self, value: Sequence[float]):
        x = value[0]
        y = value[1]
        self.position.x = x
        self.position.y = y

    @property
    def left(self) -> Side:
        return Side(self, LEFT)

    @left.setter
    def left(self, value: float):
        self.position.x = value + self._offset_value

    @property
    def right(self) -> Side:
        return Side(self, RIGHT)

    @right.setter
    def right(self, value):
        self.position.x = value - self._offset_value

    @property
    def top(self):
        return Side(self, TOP)

    @top.setter
    def top(self, value):
        self.position.y = value + self._offset_value

    @property
    def bottom(self):
        return Side(self, BOTTOM)

    @bottom.setter
    def bottom(self, value):
        self.position.y = value - self._offset_value

    @property
    def _offset_value(self):
        return self.size / 2

    def rotate(self, degrees: Number):
        self.facing.rotate(degrees)

    def __image__(self):
        if self.image is None:
            self.image = f"{type(self).__name__.lower()}.png"
        return self.image

    def __resource_path__(self):
        if self.resource_path is None:
            self.resource_path = Path(realpath(getfile(type(self)))).absolute().parent
        return self.resource_path
