from numbers import Number
from typing import Dict, Iterable, AnyStr, Sequence

from ppb import Vector

TOP = "top"
BOTTOM = "bottom"
LEFT = "left"
RIGHT = "right"

error_message = "'{klass}' object does not have attribute '{attribute}'"
side_attribute_error_message = error_message.format


class Side(object):
    sides = {
        LEFT: ('x', -1),
        RIGHT: ('x', 1),
        TOP: ('y', -1),
        BOTTOM: ('y', 1)
    }

    def __init__(self, parent: 'BaseSprite', side: AnyStr):
        self.side = side
        self.parent = parent

    def __repr__(self):
        return "Side({}, {})".format(self.value, self.parent)

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return other + self.value

    def __eq__(self, other):
        return self.value == other

    @property
    def value(self):
        coordinate, multiplier = self.sides[self.side]
        offset = self.parent.offset_value
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


class BaseSprite(object):
    """
    The base object for sprites.
    Tracks the size, position, and direction of the sprite.
    """

    def __init__(self, size: int=1, pos: Iterable=(0, 0), blackboard: Dict=None, facing: Vector=Vector(0, -1)):
        """
        Pass in the size of the sprite, the position of the sprite, the
        blackboard, and the facing direction of the sprite.

        :param size: the size of the sprite
        :param pos: the position of the sprite
        :param blackboard: the sprite's blackboard dictionary
        :param facing: the direction the sprite is facing as a Vector
        :return: BaseSprite
        """
        super().__init__()
        self.position = Vector(*pos)
        self.offset_value = size / 2
        self.game_unit_size = size
        self.facing = facing
        self.blackboard = blackboard or {}

    @property
    def center(self) -> Vector:
        """

        :return: a Vector position of the sprite's center
        """
        return self.position

    @center.setter
    def center(self, value: Sequence[float]):
        """

        :param value: a 2-value (x,y) float sequence for the sprite's new
        center position
        :return:
        """
        x = value[0]
        y = value[1]
        self.position.x = x
        self.position.y = y

    @property
    def left(self) -> Side:
        """

        :return: the left Side of this sprite
        """
        return Side(self, LEFT)

    @left.setter
    def left(self, value: float):
        """

        :param value: a value for the new left Side position of this sprite
        :return:
        """
        self.position.x = value + self.offset_value

    @property
    def right(self) -> Side:
        """

        :return: the right Side of this sprite
        """
        return Side(self, RIGHT)

    @right.setter
    def right(self, value):
        """

        :param value: a value for the new right Side position of this sprite
        :return:
        """
        self.position.x = value - self.offset_value

    @property
    def top(self):
        """

        :return: the top Side of this sprite
        """
        return Side(self, TOP)

    @top.setter
    def top(self, value):
        """

        :param value: a value for the new top Side position of this sprite
        :return:
        """
        self.position.y = value + self.offset_value

    @property
    def bottom(self):
        """

        :return: the bottom Side of this sprite
        """
        return Side(self, BOTTOM)

    @bottom.setter
    def bottom(self, value):
        """

        :param value: a value for the new bottom position Side of this sprite
        :return:
        """
        self.position.y = value - self.offset_value

    def rotate(self, degrees: Number):
        """
        Rotates the sprite a certain amount of degrees

        :param degrees: a number of degrees to rotate the sprite's direction
        :return:
        """
        self.facing.rotate(degrees)
