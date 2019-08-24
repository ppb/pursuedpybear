from math import isclose
from unittest import TestCase
from unittest.mock import patch
import warnings

from hypothesis import given
from hypothesis.strategies import floats
from hypothesis.strategies import integers
import pytest

from ppb import BaseSprite as DeprecatedBaseSprite
from ppb.sprites import *
from ppb_vector import Vector


class TestBaseSprite(TestCase):

    def setUp(self):
        self.sprite = Sprite()
        self.wide_sprite = Sprite(size=2, pos=(2, 2))

    def test_left_center(self):
        self.assertEqual(self.sprite.left.center, Vector(-0.5, 0))

        self.sprite.left.center = (1, 1)
        self.assertEqual(self.sprite.left.center, Vector(1, 1))

        self.sprite.left.center += (2, 1)
        self.assertEqual(self.sprite.left.center, Vector(3, 2))

        result = self.sprite.left.center + (2, 3)
        self.assertEqual(result, Vector(5, 5))

        self.assertEqual(self.sprite.position, Vector(3.5, 2))

    def test_right_center(self):
        self.assertEqual(self.sprite.right.center, Vector(0.5, 0))

        self.sprite.right.center = (1, 1)
        self.assertEqual(self.sprite.right.center, Vector(1, 1))

        self.sprite.right.center += (2, 1)
        self.assertEqual(self.sprite.right.center, Vector(3, 2))

        result = self.sprite.right.center + (2, 3)
        self.assertEqual(result, Vector(5, 5))

        self.assertEqual(self.sprite.position, Vector(2.5, 2))

    def test_left_left(self):
        self.assertRaises(AttributeError, getattr, self.sprite.left, "left")
        self.assertRaises(AttributeError, setattr, self.sprite.left, "left", Vector(1, 1))

    def test_left_right(self):
        self.assertRaises(AttributeError, getattr, self.sprite.left, "right")
        self.assertRaises(AttributeError, setattr, self.sprite.left, "right", Vector(1, 1))

    def test_right_right(self):
        self.assertRaises(AttributeError, getattr, self.sprite.right, "right")
        self.assertRaises(AttributeError, setattr, self.sprite.right, "right", Vector(1, 1))

    def test_right_left(self):
        self.assertRaises(AttributeError, getattr, self.sprite.right, "left")
        self.assertRaises(AttributeError, setattr, self.sprite.right, "left", Vector(1, 1))

    def test_top_center(self):
        self.assertEqual(self.sprite.top.center, Vector(0, 0.5))

        self.sprite.top.center = (1, 1)
        self.assertEqual(self.sprite.top.center, Vector(1, 1))

    def test_top_top(self):
        self.assertRaises(AttributeError, getattr, self.sprite.top, "top")
        self.assertRaises(AttributeError, setattr, self.sprite.top, "top", Vector(1, 1))

    def test_top_bottom(self):
        self.assertRaises(AttributeError, getattr, self.sprite.top, "bottom")
        self.assertRaises(AttributeError, setattr, self.sprite.top, "bottom", Vector(1, 1))

    def test_bottom_center(self):
        self.assertEqual(self.sprite.bottom.center, Vector(0, -0.5))

        self.sprite.bottom.center = (1, 1)
        self.assertEqual(self.sprite.bottom.center, Vector(1, 1))

    def test_bottom_top(self):
        self.assertRaises(AttributeError, getattr, self.sprite.bottom, "top")
        self.assertRaises(AttributeError, setattr, self.sprite.bottom, "top", Vector(1, 1))

    def test_bottom_bottom(self):
        self.assertRaises(AttributeError, getattr, self.sprite.bottom, "bottom")
        self.assertRaises(AttributeError, setattr, self.sprite.bottom, "bottom", Vector(1, 1))


def test_class_attrs():
    class TestSprite(BaseSprite):
        position = Vector(4, 2)

    sprite = TestSprite()
    assert sprite.position == Vector(4, 2)

    sprite = TestSprite(position=(2, 4))
    assert sprite.position == Vector(2, 4)


def test_offset():
    class TestSprite(Sprite):
        size = 1.1

    assert TestSprite().left < -0.5


def test_rotatable_instatiation():
    rotatable = RotatableMixin()
    assert rotatable.rotation == 0


def test_rotatable_subclass():

    class TestRotatableMixin(RotatableMixin):
        _rotation = 180
        basis = Vector(0, 1)

    rotatable = TestRotatableMixin()
    assert rotatable.rotation == 180
    assert rotatable.facing == Vector(0, -1)


def test_rotatable_rotation_setter():
    rotatable = RotatableMixin()

    rotatable.rotation = 405
    assert rotatable.rotation == 45


def test_rotatable_rotate():
    rotatable = RotatableMixin()

    assert rotatable.rotation == 0
    rotatable.rotate(180)
    assert rotatable.rotation == 180
    rotatable.rotate(200)
    assert rotatable.rotation == 20
    rotatable.rotate(-300)
    assert rotatable.rotation == 80


def test_rotatable_base_sprite():
    test_sprite = Sprite()

    test_sprite.rotate(1)
    assert test_sprite.rotation == 1


@given(y=floats(allow_nan=False, allow_infinity=False))
def test_sides_bottom(y):
    sprite = Sprite(position=(0, y))
    assert isclose(sprite.bottom, y - 0.5)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@given(y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_bottom_set(y):
    sprite = Sprite()
    sprite.bottom = y
    assert sprite.bottom == y
    assert sprite.position.y == y + 0.5


@given(y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_bottom_plus_equals(y):
    sprite = Sprite()
    sprite.bottom += y
    assert sprite.bottom == y - 0.5
    assert sprite.position.y == sprite.bottom + 0.5


@given(x=floats(allow_nan=False, allow_infinity=False), y=floats(allow_nan=False, allow_infinity=False))
def test_sides_bottom_left(x, y):
    sprite = Sprite(position=(x, y))
    bottom_left = sprite.bottom.left
    left_bottom = sprite.left.bottom
    assert bottom_left == left_bottom
    assert isclose(bottom_left.y, y - 0.5)
    assert isclose(bottom_left.x, x - 0.5)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_bottom_left_set(x, y, vector_type):
    sprite = Sprite()
    sprite.bottom.left = vector_type((x, y))
    bottom_left = sprite.bottom.left
    left_bottom = sprite.left.bottom
    assert bottom_left == left_bottom
    assert bottom_left == Vector(x, y)
    assert sprite.position == bottom_left + Vector(0.5, 0.5)

    # duplicating to prove top.left and left.top are the same.
    sprite = Sprite()
    sprite.left.bottom = vector_type((x, y))
    bottom_left = sprite.bottom.left
    left_bottom = sprite.left.bottom
    assert left_bottom == bottom_left
    assert left_bottom == Vector(x, y)
    assert sprite.position == left_bottom + Vector(0.5, 0.5)


@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_bottom_left_plus_equals(x, y, vector_type):
    sprite = Sprite()
    sprite.bottom.left += vector_type((x, y))
    bottom_left = sprite.bottom.left
    left_bottom = sprite.left.bottom
    assert bottom_left == left_bottom
    assert bottom_left == Vector(x - 0.5, y - 0.5)
    assert sprite.position == bottom_left + Vector(0.5, 0.5)

    # duplicating to prove bottom.left and left.bottom are the same.
    sprite = Sprite()
    sprite.bottom.left += vector_type((x, y))
    bottom_left = sprite.bottom.left
    left_bottom = sprite.left.bottom
    assert left_bottom == bottom_left
    assert left_bottom == Vector(x +- 0.5, y - 0.5)
    assert sprite.position == left_bottom + Vector(0.5, 0.5)


@given(x=floats(allow_nan=False, allow_infinity=False), y=floats(allow_nan=False, allow_infinity=False))
def test_sides_bottom_right(x, y):
    sprite = Sprite(position=(x, y))
    bottom_right = sprite.bottom.right
    right_bottom = sprite.right.bottom
    assert bottom_right == right_bottom
    assert isclose(bottom_right.y, y - 0.5)
    assert isclose(bottom_right.x, x + 0.5)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_bottom_right_set(x, y, vector_type):
    sprite = Sprite()
    sprite.bottom.right = vector_type((x, y))
    bottom_right = sprite.bottom.right
    right_bottom = sprite.right.bottom
    assert bottom_right == right_bottom
    assert bottom_right == Vector(x, y)
    assert sprite.position == bottom_right + Vector(-0.5, 0.5)

    # duplicating to prove top.left and left.top are the same.
    sprite = Sprite()
    sprite.right.bottom = vector_type((x, y))
    bottom_right = sprite.bottom.right
    right_bottom = sprite.right.bottom
    assert right_bottom == bottom_right
    assert right_bottom == Vector(x, y)
    assert sprite.position == right_bottom + Vector(-0.5, 0.5)


@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_bottom_right_plus_equals(x, y, vector_type):
    sprite = Sprite()
    sprite.bottom.right += vector_type((x, y))
    bottom_right = sprite.bottom.right
    right_bottom = sprite.right.bottom
    assert bottom_right == right_bottom
    assert bottom_right == Vector(x + 0.5, y - 0.5)
    assert sprite.position == bottom_right + Vector(-0.5, 0.5)

    # duplicating to prove bottom.left and left.bottom are the same.
    sprite = Sprite()
    sprite.bottom.left += vector_type((x, y))
    bottom_right = sprite.bottom.right
    right_bottom = sprite.right.bottom
    assert right_bottom == bottom_right
    assert right_bottom == Vector(x + 0.5, y - 0.5)
    assert sprite.position == right_bottom + Vector(-0.5, 0.5)


@given(x=floats(allow_nan=False, allow_infinity=False), y=floats(allow_nan=False, allow_infinity=False))
def test_sides_center_equals_position(x, y):
    sprite = Sprite(position=(x, y))
    assert sprite.center == sprite.position


@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=floats(allow_nan=False, allow_infinity=False), y=floats(allow_nan=False, allow_infinity=False))
def test_sides_center_setting(x, y, vector_type):
    sprite = Sprite()
    sprite.center = vector_type((x, y))
    assert sprite.center.x == x
    assert sprite.center.y == y
    assert sprite.position == sprite.center


@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=floats(allow_nan=False, allow_infinity=False),
       y=floats(allow_nan=False, allow_infinity=False),
       delta_x=floats(allow_nan=False, allow_infinity=False),
       delta_y=floats(allow_nan=False, allow_infinity=False))
def test_sides_center_plus_equals(x, y, delta_x, delta_y, vector_type):
    sprite = Sprite(position=(x, y))
    sprite.center += vector_type((delta_x, delta_y))
    assert sprite.position.x == x + delta_x
    assert sprite.position.y == y + delta_y
    assert sprite.position == sprite.center


@given(x=floats(allow_nan=False, allow_infinity=False))
def test_sides_left(x):
    sprite = Sprite(position=(x, 0))
    assert isclose(sprite.left, x - 0.5)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@given(x=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_set_left(x):
    sprite = Sprite()
    sprite.left = x
    print(float(sprite.left))
    assert sprite.left == x
    assert sprite.position.x == x + 0.5


@given(x=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_plus_equals_left(x):
    sprite = Sprite()
    sprite.left += x
    assert sprite.left == x - 0.5
    assert sprite.position.x == sprite.left + 0.5


@given(x=floats(allow_nan=False, allow_infinity=False))
def test_sides_right(x):
    sprite = Sprite(position=(x, 0))
    assert isclose(sprite.right, x + 0.5)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@given(x=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_right_set(x):
    sprite = Sprite()
    sprite.right = x
    print(float(sprite.left))
    assert sprite.right == x
    assert sprite.position.x == x - 0.5


@given(x=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_right_plus_equals(x):
    sprite = Sprite()
    sprite.right += x
    assert sprite.right == x + 0.5
    assert sprite.position.x == sprite.right - 0.5


@given(y=floats(allow_nan=False, allow_infinity=False))
def test_sides_top(y):
    sprite = Sprite(position=(0, y))
    assert isclose(sprite.top, y + 0.5)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@given(y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_top_set(y):
    sprite = Sprite()
    sprite.top = y
    assert sprite.top == y
    assert sprite.position.y == y - 0.5


@given(y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_top_plus_equals(y):
    sprite = Sprite()
    sprite.top += y
    assert sprite.top == y + 0.5
    assert sprite.position.y == sprite.top - 0.5


@given(x=floats(allow_nan=False, allow_infinity=False), y=floats(allow_nan=False, allow_infinity=False))
def test_sides_top_left(x, y):
    sprite = Sprite(position=(x, y))
    top_left = sprite.top.left
    left_top = sprite.left.top
    assert top_left == left_top
    assert isclose(top_left.y, y + 0.5)
    assert isclose(top_left.x, x - 0.5)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_top_left_set(x, y, vector_type):
    sprite = Sprite()
    sprite.top.left = vector_type((x, y))
    top_left = sprite.top.left
    left_top = sprite.left.top
    assert top_left == left_top
    assert top_left == Vector(x, y)
    assert sprite.position == top_left + Vector(0.5, -0.5)

    # duplicating to prove top.left and left.top are the same.
    sprite = Sprite()
    sprite.left.top = vector_type((x, y))
    top_left = sprite.top.left
    left_top = sprite.left.top
    assert left_top == top_left
    assert left_top == Vector(x, y)
    assert sprite.position == left_top + Vector(0.5, -0.5)


@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_top_left_plus_equals(x, y, vector_type):
    sprite = Sprite()
    sprite.top.left += vector_type((x, y))
    top_left = sprite.top.left
    left_top = sprite.left.top
    assert top_left == left_top
    assert top_left == Vector(x - 0.5, y + 0.5)
    assert sprite.position == top_left + Vector(0.5, -0.5)

    # duplicating to prove top.left and left.top are the same.
    sprite = Sprite()
    sprite.top.left += vector_type((x, y))
    top_left = sprite.top.left
    left_top = sprite.left.top
    assert left_top == top_left
    assert left_top == Vector(x - 0.5, y + 0.5)
    assert sprite.position == left_top + Vector(0.5, -0.5)


@given(x=floats(allow_nan=False, allow_infinity=False), y=floats(allow_nan=False, allow_infinity=False))
def test_sides_top_right(x, y):
    sprite = Sprite(position=(x, y))
    top_right = sprite.top.right
    right_top = sprite.right.top
    assert top_right == right_top
    assert isclose(top_right.y, y + 0.5)
    assert isclose(top_right.x, x + 0.5)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_top_right_set(x, y, vector_type):
    sprite = Sprite()
    sprite.top.right = vector_type((x, y))
    top_right = sprite.top.right
    right_top = sprite.right.top
    assert top_right == right_top
    assert top_right == Vector(x, y)
    assert sprite.position == top_right + Vector(-0.5, -0.5)

    # duplicating to prove top.left and left.top are the same.
    sprite = Sprite()
    sprite.right.top = vector_type((x, y))
    top_right = sprite.top.right
    right_top = sprite.right.top
    assert right_top == top_right
    assert right_top == Vector(x, y)
    assert sprite.position == right_top + Vector(-0.5, -0.5)


@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_top_right_plus_equals(x, y, vector_type):
    sprite = Sprite()
    sprite.top.right += vector_type((x, y))
    top_right = sprite.top.right
    right_top = sprite.right.top
    assert top_right == right_top
    assert top_right == Vector(x + 0.5, y + 0.5)
    assert sprite.position == top_right + Vector(-0.5, -0.5)

    # duplicating to prove top.left and left.top are the same.
    sprite = Sprite()
    sprite.top.left += vector_type((x, y))
    top_right = sprite.top.right
    right_top = sprite.right.top
    assert right_top == top_right
    assert right_top == Vector(x + 0.5, y + 0.5)
    assert sprite.position == right_top + Vector(-0.5, -0.5)


def test_sprite_in_main():
    """
    Test that Sprite.__resource_path__ returns a meaningful value inside
    REPLs where __main__ doesn't have a file.
    """
    class TestSprite(Sprite):
        pass

    s = TestSprite()

    with patch("ppb.sprites.getfile", side_effect=TypeError):
        # This patch simulates what happens when TestSprite was defined in the REPL
        assert s.__image__()  # We don't care what it is, as long as it's something


def test_deprecated_base_sprite_warns():
    with warnings.catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")
        # Trigger a warning.
        sprite = DeprecatedBaseSprite()
        # Verify some things
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "deprecated" in str(w[-1].message)
