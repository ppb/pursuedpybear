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

    def __init__(self, parent, side):
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
        return self.parent.pos[coordinate] + (offset * multiplier)

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
        return Vector(self.value, self.parent.bottom)

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
        if self.side == TOP:
            return Vector(self.parent.center.x, self.value)
        else:
            return Vector(self.value, self.parent.center.y)

    @center.setter
    def center(self, value):
        if self.side == TOP:
            setattr(self.parent, self.side, value[1])
            self.parent.center.x = value[0]
        else:
            setattr(self.parent, self.side, value[0])
            self.parent.pos.y = value[1]

    def _attribute_gate(self, attribute, bad_sides):
        if self.side in bad_sides:
            name = type(self).__name__
            message = side_attribute_error_message(klass=name,
                                                   attribute=attribute)
            raise AttributeError(message)


class BaseSprite(object):

    def __init__(self, size=1, pos=(0, 0)):
        super().__init__()
        self.pos = Vector(*pos)
        self.offset_value = size / 2
        self.game_unit_size = size

    @property
    def center(self):
        return self.pos

    @center.setter
    def center(self, value):
        x = value[0]
        y = value[1]
        self.pos.x = x
        self.pos.y = y

    @property
    def left(self):
        return Side(self, LEFT)

    @left.setter
    def left(self, value):
        self.pos.x = value + self.offset_value

    @property
    def right(self):
        return Side(self, RIGHT)

    @right.setter
    def right(self, value):
        self.pos.x = value - self.offset_value

    @property
    def top(self):
        return Side(self, TOP)

    @top.setter
    def top(self, value):
        self.pos.y = value + self.offset_value

    @property
    def bottom(self):
        return self.pos.y + self.offset_value

    @bottom.setter
    def bottom(self, value):
        self.pos.y = value - self.offset_value
