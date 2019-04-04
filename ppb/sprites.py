from inspect import getfile
from numbers import Number
from os.path import realpath
from pathlib import Path
from typing import Dict, Iterable, Sequence
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

    def __init__(self, parent: 'BaseSprite', side: str):
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

    def _lookup_side(self, side):
        dimension, sign = self.sides[side]
        return dimension, sign * self.parent._offset_value

    @property
    def value(self):
        dimension, offset = self._lookup_side(self.side)
        return self.parent.position[dimension] + offset

    @property
    def top(self):
        self._attribute_gate(TOP, [TOP, BOTTOM])
        return Vector(self.value, self.parent.top.value)

    @top.setter
    def top(self, value):
        self._attribute_gate(TOP, [TOP, BOTTOM])
        self.parent.position = self._mk_update_vector_side(TOP, value)

    @property
    def bottom(self):
        self._attribute_gate(BOTTOM, [TOP, BOTTOM])
        return Vector(self.value, self.parent.bottom.value)

    @bottom.setter
    def bottom(self, value):
        self._attribute_gate(BOTTOM, [TOP, BOTTOM])
        self.parent.position = self._mk_update_vector_side(BOTTOM, value)

    @property
    def left(self):
        self._attribute_gate(LEFT, [LEFT, RIGHT])
        return Vector(self.parent.left.value, self.value)

    @left.setter
    def left(self, value):
        self._attribute_gate(LEFT, [LEFT, RIGHT])
        self.parent.position = self._mk_update_vector_side(LEFT, value)

    @property
    def right(self):
        self._attribute_gate(RIGHT, [LEFT, RIGHT])
        return Vector(self.parent.right.value, self.value)

    @right.setter
    def right(self, value):
        self._attribute_gate(RIGHT, [LEFT, RIGHT])
        self.parent.position = self._mk_update_vector_side(RIGHT, value)

    @property
    def center(self):
        if self.side in (TOP, BOTTOM):
            return Vector(self.parent.center.x, self.value)
        else:
            return Vector(self.value, self.parent.center.y)

    @center.setter
    def center(self, value):
        self.parent.position = self._mk_update_vector_center(value)

    def _mk_update_vector_side(self, attribute, value):
        value = Vector(value)
        assert attribute != 'center'
        # Does a bunch of dynamc resolution:
        # Sprite.top.left
        #        ^   ^ attribute
        #        self.side
        self_dimension, self_offset = self._lookup_side(self.side)

        attr_dimension, attr_offset = self._lookup_side(attribute)

        assert self_dimension != attr_dimension

        fields = {
            self_dimension: value[self_dimension] - self_offset,
            attr_dimension: value[attr_dimension] - attr_offset,
        }
        return Vector(**fields)

    def _mk_update_vector_center(self, value):
        value = Vector(value)
        # Pretty similar to ._mk_update_vector_side()
        self_dimension, self_offset = self._lookup_side(self.side)

        attr_dimension = 'y' if self_dimension == 'x' else 'x'

        fields = {
            self_dimension: value[self_dimension] - self_offset,
            attr_dimension: value[attr_dimension]
        }

        return Vector(**fields)

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
        self.position = Vector(self.position)
        self.facing = Vector(self.facing)

        # Initialize things
        for k, v in kwargs.items():
            # Abbreviations
            if k == 'pos':
                k = 'position'
            # Castings
            if k in ('position', 'facing'):
                v = Vector.convert(v)
            setattr(self, k, v)

        # Trigger some calculations
        self.size = self.size

    @property
    def center(self) -> Vector:
        return self.position

    @center.setter
    def center(self, value: Sequence[float]):
        self.position = Vector.convert(value)

    @property
    def left(self) -> Side:
        return Side(self, LEFT)

    @left.setter
    def left(self, value: float):
        self.position = Vector(value + self._offset_value, self.position.y)

    @property
    def right(self) -> Side:
        return Side(self, RIGHT)

    @right.setter
    def right(self, value):
        self.position = Vector(value - self._offset_value, self.position.y)

    @property
    def top(self):
        return Side(self, TOP)

    @top.setter
    def top(self, value):
        self.position = Vector(self.position.x, value + self._offset_value)

    @property
    def bottom(self):
        return Side(self, BOTTOM)

    @bottom.setter
    def bottom(self, value):
        self.position = Vector(self.position.x, value - self._offset_value)

    @property
    def _offset_value(self):
        return self.size / 2

    def rotate(self, degrees: Number):
        self.facing = self.facing.rotate(degrees)

    def __image__(self):
        if self.image is None:
            self.image = f"{type(self).__name__.lower()}.png"
        return self.image

    def __resource_path__(self):
        if self.resource_path is None:
            self.resource_path = Path(realpath(getfile(type(self)))).absolute().parent
        return self.resource_path
