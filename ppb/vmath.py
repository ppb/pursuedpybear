from __future__ import division

from math import cos, hypot, radians, sin
from numbers import Number


# TODO: WRITE TESTS


class Vector2(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = hypot(x, y)

    def __add__(self, other):
        t = type(other)
        if isinstance(other, Vector2):
            return type(self)(self.x + other.x, self.y + other.y)
        elif isinstance(other, (list, tuple)) and len(other) == 2:
            return Vector2(self.x + other[0], self.y + other[1])
        elif isinstance(other, (dict, set)) and 'x' in other and 'y' in other and len(other) == 2:
            return Vector2(self.x + other['x'], self.y + other['y'])
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other, (list, tuple)) and len(other) == 2:
            return Vector2(self.x - other[0], self.y - other[1])
        elif isinstance(other, dict) and 'x' in other and 'y' in other and len(other) == 2:
            return Vector2(self.x - other['x'], self.y - other['y'])
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, Number):
            return Vector2(self.x * other, self.y * other)
        else:
            return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, Number):
            return Vector2(self.x * other, self.y * other)

    def __len__(self):
        return self.length

    def __getitem__(self, item):
        item_type = type(item)

        if item_type is str:
            if item == 'x':
                return self.x
            elif item == 'y':
                return self.y
            else:
                raise KeyError
        elif item_type is int:
            if item == 0:
                return self.x
            elif item == 1:
                return self.y
            else:
                raise IndexError
        else:
            raise TypeError

    def __repr__(self):
        return "Vector2({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, Vector2):
            return self.x != other.x or self.y != other.y

    def rotate(self, degrees):
        r = radians(degrees)
        r_cos = cos(r)
        r_sin = sin(r)
        x = round(self.x * r_cos - self.y * r_sin, 5)
        y = round(self.x * r_sin + self.y * r_cos, 5)
        return Vector2(x, y)

    def normalize(self):
        return self.scale(1)

    def truncate(self, max_length):
        if self.length > max_length:
            return self.scale(max_length)
        return self

    def scale(self, length):
        try:
            scale = length / self.length
        except ZeroDivisionError:
            scale = 1
        return self * scale
