from ppb import Vector


class Side(object):
    sides = {
        "left": ('x', -1),
        "right": ('x', 1),
        "top": ('y', -1),
        "bottom": ('y', 1)
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
        return Vector(self.value, self.parent.top)

    @top.setter
    def top(self, value):
        if self.side in ["left", "right"]:
            setattr(self.parent, self.side, value[0])
            self.parent.top = value[1]
        else:
            raise AttributeError()

    @property
    def bottom(self):
        return Vector(self.value, self.parent.bottom)

    @bottom.setter
    def bottom(self, value):
        setattr(self.parent, self.side, value[0])
        self.parent.bottom = value[1]

    @property
    def center(self):
        return Vector(self.value, self.parent.pos.y)

    @center.setter
    def center(self, value):
        setattr(self.parent, self.side, value[0])
        self.parent.pos.y = value[1]


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
        return Side(self, "left")

    @left.setter
    def left(self, value):
        self.pos.x = value + self.offset_value

    @property
    def right(self):
        return Side(self, "right")

    @right.setter
    def right(self, value):
        self.pos.x = value - self.offset_value

    @property
    def top(self):
        return self.pos.y - self.offset_value

    @top.setter
    def top(self, value):
        self.pos.y = value + self.offset_value

    @property
    def bottom(self):
        return self.pos.y + self.offset_value

    @bottom.setter
    def bottom(self, value):
        self.pos.y = value - self.offset_value
