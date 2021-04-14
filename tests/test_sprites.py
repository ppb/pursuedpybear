from math import isclose
from typing import NamedTuple
from typing import Union
from unittest.mock import patch
import warnings

from hypothesis import given
from hypothesis.strategies import floats
from hypothesis.strategies import integers
import pytest

from ppb.sprites import *
from ppb_vector import Vector


class RectangleTestSprite(RectangleShapeMixin, BaseSprite):
    pass


class SquareTestSprite(SquareShapeMixin, BaseSprite):
    pass


RECTANGLE_SPRITE_CLASSES = [RectangleTestSprite, RectangleSprite]
SQUARE_SPRITE_CLASSES = [SquareTestSprite, Sprite]
SPRITE_CLASSES = [*RECTANGLE_SPRITE_CLASSES, *SQUARE_SPRITE_CLASSES]


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
        rotation = 180
        basis = Vector(0, 1)

    rotatable = TestRotatableMixin()
    assert rotatable.rotation == 180
    assert rotatable.facing == Vector(0, -1)


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


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(y=floats(allow_nan=False, allow_infinity=False))
def test_sides_bottom(y, sprite_class):
    sprite = sprite_class(position=(0, y))
    assert isclose(sprite.bottom, y - 0.5)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_bottom_set(y, sprite_class):
    sprite = sprite_class()
    sprite.bottom = y
    assert sprite.bottom == y
    assert sprite.position.y == y + 0.5


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_bottom_plus_equals(y, sprite_class):
    sprite = sprite_class()
    sprite.bottom += y
    assert sprite.bottom == y - 0.5
    assert sprite.position.y == sprite.bottom + 0.5


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(x=floats(allow_nan=False, allow_infinity=False), y=floats(allow_nan=False, allow_infinity=False))
def test_sides_bottom_middle(x, y, sprite_class):
    sprite = sprite_class(position=(x, y))
    bottom_middle = sprite.bottom_middle
    assert isclose(bottom_middle.y, y - 0.5)
    assert isclose(bottom_middle.x, x)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_bottom_middle_set(x, y, vector_type, sprite_class):
    sprite = sprite_class()
    sprite.bottom_middle = vector_type((x, y))
    bottom_middle = sprite.bottom_middle
    assert bottom_middle == Vector(x, y)
    assert sprite.position == bottom_middle + Vector(0, 0.5)


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_bottom_middle_plus_equals(x, y, vector_type, sprite_class):
    sprite = sprite_class()
    sprite.bottom_middle += vector_type((x, y))
    bottom_middle = sprite.bottom_middle
    assert bottom_middle == Vector(x, y - 0.5)
    assert sprite.position == bottom_middle + Vector(0, 0.5)


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(x=floats(allow_nan=False, allow_infinity=False), y=floats(allow_nan=False, allow_infinity=False))
def test_sides_bottom_left(x, y, sprite_class):
    sprite = sprite_class(position=(x, y))
    bottom_left = sprite.bottom_left
    assert isclose(bottom_left.y, y - 0.5)
    assert isclose(bottom_left.x, x - 0.5)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_bottom_left_set(x, y, vector_type, sprite_class):
    sprite = sprite_class()
    sprite.bottom_left = vector_type((x, y))
    bottom_left = sprite.bottom_left
    assert bottom_left == Vector(x, y)
    assert sprite.position == bottom_left + Vector(0.5, 0.5)


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_bottom_left_plus_equals(x, y, vector_type, sprite_class):
    sprite = sprite_class()
    sprite.bottom_left += vector_type((x, y))
    bottom_left = sprite.bottom_left
    assert bottom_left == Vector(x - 0.5, y - 0.5)
    assert sprite.position == bottom_left + Vector(0.5, 0.5)


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(x=floats(allow_nan=False, allow_infinity=False), y=floats(allow_nan=False, allow_infinity=False))
def test_sides_bottom_right(x, y, sprite_class):
    sprite = sprite_class(position=(x, y))
    bottom_right = sprite.bottom_right
    assert isclose(bottom_right.y, y - 0.5)
    assert isclose(bottom_right.x, x + 0.5)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_bottom_right_set(x, y, vector_type, sprite_class):
    sprite = sprite_class()
    sprite.bottom_right = vector_type((x, y))
    bottom_right = sprite.bottom_right
    assert bottom_right == Vector(x, y)
    assert sprite.position == bottom_right + Vector(-0.5, 0.5)


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_bottom_right_plus_equals(x, y, vector_type, sprite_class):
    sprite = sprite_class()
    sprite.bottom_right += vector_type((x, y))
    bottom_right = sprite.bottom_right
    assert bottom_right == Vector(x + 0.5, y - 0.5)
    assert sprite.position == bottom_right + Vector(-0.5, 0.5)


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(x=floats(allow_nan=False, allow_infinity=False), y=floats(allow_nan=False, allow_infinity=False))
def test_sides_center_equals_position(x, y, sprite_class):
    sprite = sprite_class(position=(x, y))
    assert sprite.center == sprite.position


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=floats(allow_nan=False, allow_infinity=False), y=floats(allow_nan=False, allow_infinity=False))
def test_sides_center_setting(x, y, vector_type, sprite_class):
    sprite = sprite_class()
    sprite.center = vector_type((x, y))
    assert sprite.center.x == x
    assert sprite.center.y == y
    assert sprite.position == sprite.center


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=floats(allow_nan=False, allow_infinity=False),
       y=floats(allow_nan=False, allow_infinity=False),
       delta_x=floats(allow_nan=False, allow_infinity=False),
       delta_y=floats(allow_nan=False, allow_infinity=False))
def test_sides_center_plus_equals(x, y, delta_x, delta_y, vector_type, sprite_class):
    sprite = sprite_class(position=(x, y))
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
@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(x=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_left_set(x, sprite_class):
    sprite = sprite_class()
    sprite.left = x
    print(float(sprite.left))
    assert sprite.left == x
    assert sprite.position.x == x + 0.5


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(x=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_left_plus_equals(x, sprite_class):
    sprite = sprite_class()
    sprite.left += x
    assert sprite.left == x - 0.5
    assert sprite.position.x == sprite.left + 0.5


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(x=floats(allow_nan=False, allow_infinity=False), y=floats(allow_nan=False, allow_infinity=False))
def test_sides_left_middle(x, y, sprite_class):
    sprite = sprite_class(position=(x, y))
    left_middle = sprite.left_middle
    assert isclose(left_middle.y, y)
    assert isclose(left_middle.x, x - 0.5)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_left_middle_set(x, y, vector_type, sprite_class):
    sprite = sprite_class()
    sprite.left_middle = vector_type((x, y))
    left_middle = sprite.left_middle
    assert left_middle == Vector(x, y)
    assert sprite.position == left_middle + Vector(0.5, 0)


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_left_middle_plus_equals(x, y, vector_type, sprite_class):
    sprite = sprite_class()
    sprite.left_middle += vector_type((x, y))
    left_middle = sprite.left_middle
    assert left_middle == Vector(x - 0.5, y)
    assert sprite.position == left_middle + Vector(0.5, 0)


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(x=floats(allow_nan=False, allow_infinity=False))
def test_sides_right(x, sprite_class):
    sprite = sprite_class(position=(x, 0))
    assert isclose(sprite.right, x + 0.5)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(x=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_right_set(x, sprite_class):
    sprite = sprite_class()
    sprite.right = x
    assert sprite.right == x
    assert sprite.position.x == x - 0.5


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(x=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_right_plus_equals(x, sprite_class):
    sprite = sprite_class()
    sprite.right += x
    assert sprite.right == x + 0.5
    assert sprite.position.x == sprite.right - 0.5


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(x=floats(allow_nan=False, allow_infinity=False), y=floats(allow_nan=False, allow_infinity=False))
def test_sides_right_middle(x, y, sprite_class):
    sprite = sprite_class(position=(x, y))
    right_middle = sprite.right_middle
    assert isclose(right_middle.y, y)
    assert isclose(right_middle.x, x + 0.5)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_right_middle_set(x, y, vector_type, sprite_class):
    sprite = sprite_class()
    sprite.right_middle = vector_type((x, y))
    right_middle = sprite.right_middle
    assert right_middle == Vector(x, y)
    assert sprite.position == right_middle + Vector(-0.5, 0)


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_right_middle_plus_equals(x, y, vector_type, sprite_class):
    sprite = sprite_class()
    sprite.right_middle += vector_type((x, y))
    right_middle = sprite.right_middle
    assert right_middle == Vector(x + 0.5, y)
    assert sprite.position == right_middle + Vector(-0.5, 0)


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(y=floats(allow_nan=False, allow_infinity=False))
def test_sides_top(y, sprite_class):
    sprite = sprite_class(position=(0, y))
    assert isclose(sprite.top, y + 0.5)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_top_set(y, sprite_class):
    sprite = sprite_class()
    sprite.top = y
    assert sprite.top == y
    assert sprite.position.y == y - 0.5


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_top_plus_equals(y, sprite_class):
    sprite = sprite_class()
    sprite.top += y
    assert sprite.top == y + 0.5
    assert sprite.position.y == sprite.top - 0.5


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(x=floats(allow_nan=False, allow_infinity=False), y=floats(allow_nan=False, allow_infinity=False))
def test_sides_top_middle(x, y, sprite_class):
    sprite = sprite_class(position=(x, y))
    top_middle = sprite.top_middle
    assert isclose(top_middle.y, y + 0.5)
    assert isclose(top_middle.x, x)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_top_middle_set(x, y, vector_type, sprite_class):
    sprite = sprite_class()
    sprite.top_middle = vector_type((x, y))
    top_middle = sprite.top_middle
    assert top_middle == Vector(x, y)
    assert sprite.position == top_middle + Vector(0, -0.5)


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_top_middle_plus_equals(x, y, vector_type, sprite_class):
    sprite = sprite_class()
    sprite.top_middle += vector_type((x, y))
    top_middle = sprite.top_middle
    assert top_middle == Vector(x, y + 0.5)
    assert sprite.position == top_middle + Vector(0, -0.5)


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(x=floats(allow_nan=False, allow_infinity=False), y=floats(allow_nan=False, allow_infinity=False))
def test_sides_top_left(x, y, sprite_class):
    sprite = sprite_class(position=(x, y))
    top_left = sprite.top_left
    assert isclose(top_left.y, y + 0.5)
    assert isclose(top_left.x, x - 0.5)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_top_left_set(x, y, vector_type, sprite_class):
    sprite = sprite_class()
    sprite.top_left = vector_type((x, y))
    top_left = sprite.top_left
    assert top_left == Vector(x, y)
    assert sprite.position == top_left + Vector(0.5, -0.5)


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_top_left_plus_equals(x, y, vector_type, sprite_class):
    sprite = sprite_class()
    sprite.top_left += vector_type((x, y))
    top_left = sprite.top_left
    assert top_left == Vector(x - 0.5, y + 0.5)
    assert sprite.position == top_left + Vector(0.5, -0.5)


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@given(x=floats(allow_nan=False, allow_infinity=False), y=floats(allow_nan=False, allow_infinity=False))
def test_sides_top_right(x, y, sprite_class):
    sprite = sprite_class(position=(x, y))
    top_right = sprite.top_right
    assert isclose(top_right.y, y + 0.5)
    assert isclose(top_right.x, x + 0.5)


# ints because the kinds of floats hypothesis generates aren't realistic
# to our use case.
@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_top_right_set(x, y, vector_type, sprite_class):
    sprite = sprite_class()
    sprite.top_right = vector_type((x, y))
    top_right = sprite.top_right
    assert top_right == Vector(x, y)
    assert sprite.position == top_right + Vector(-0.5, -0.5)


@pytest.mark.parametrize("sprite_class", SPRITE_CLASSES)
@pytest.mark.parametrize("vector_type", [tuple, Vector])
@given(x=integers(max_value=10_000_000, min_value=-10_000_000), y=integers(max_value=10_000_000, min_value=-10_000_000))
def test_sides_top_right_plus_equals(x, y, vector_type, sprite_class):
    sprite = sprite_class()
    sprite.top_right += vector_type((x, y))
    top_right = sprite.top_right
    assert top_right == Vector(x + 0.5, y + 0.5)
    assert sprite.position == top_right + Vector(-0.5, -0.5)


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


# Below are tests for the new RectangleShapeMixin and the default Sprite that uses it.


class SidesResults(NamedTuple):
    """A container for results while testing sprites."""
    top: Union[float, int]
    bottom: Union[float, int]
    left: Union[float, int]
    right: Union[float, int]


class CornerResults(NamedTuple):
    """A container for results while testing sprites."""
    top_left: Vector
    top_right: Vector
    bottom_left: Vector
    bottom_right: Vector


class SpriteParams(NamedTuple):
    position: Vector
    width: Union[float, int]
    height: Union[float, int]


class CornerSetterResults(NamedTuple):
    top_left: CornerResults
    top_right: CornerResults
    bottom_left: CornerResults
    bottom_right: CornerResults


class SideSetterResults(NamedTuple):
    top: SidesResults
    bottom: SidesResults
    left: SidesResults
    right: SidesResults


@pytest.mark.parametrize("sprite_class", RECTANGLE_SPRITE_CLASSES)
@pytest.mark.parametrize("params, results", [
    [SpriteParams(Vector(0, 0), 1, 1), SidesResults(0.5, -0.5, -0.5, 0.5)],
    [SpriteParams(Vector(0, 0), 2, 1), SidesResults(0.5, -0.5, -1, 1)],
    [SpriteParams(Vector(0, 0), 1, 2), SidesResults(1, -1, -0.5, 0.5)],
    [
        SpriteParams(Vector(-62.03, 16.29), 4.87, 0.53),
        SidesResults(16.555, 16.025, -64.465, -59.595)
    ],
    [
        SpriteParams(Vector(32.88, 55.3), 7.47, 0.99),
        SidesResults(55.794999999999995, 54.805, 29.145000000000003, 36.615)
    ],
])
def test_sprite_sides_access(sprite_class, params: SpriteParams, results: SidesResults):
    sprite = sprite_class(
        position=params.position,
        width=params.width,
        height=params.height,
    )
    assert sprite.top == results.top
    assert sprite.bottom == results.bottom
    assert sprite.left == results.left
    assert sprite.right == results.right


@pytest.mark.parametrize("sprite_class", RECTANGLE_SPRITE_CLASSES)
@pytest.mark.parametrize("params, results", [
    [
        SpriteParams(Vector(0, 0), 1, 1),
        SideSetterResults(
            SidesResults(0, -1, -0.5, 0.5),
            SidesResults(1, 0, -0.5, 0.5),
            SidesResults(0.5, -0.5, 0, 1),
            SidesResults(0.5, -0.5, -1, 0)
        )
    ],
    [
        SpriteParams(Vector(0, 0), 2, 1),
        SideSetterResults(
            SidesResults(0, -1, -1, 1),
            SidesResults(1, 0, -1, 1),
            SidesResults(0.5, -0.5, 0, 2),
            SidesResults(0.5, -0.5, -2, 0)
        )
    ]
])
def test_sprite_sides_set(sprite_class, params: SpriteParams, results: SideSetterResults):
    sprite = sprite_class(
        width=params.width,
        height=params.height
    )

    sprite.left = params.position.x
    expected = results.left
    assert sprite.left == expected.left
    assert sprite.right == expected.right
    assert sprite.top == expected.top
    assert sprite.bottom == expected.bottom

    sprite.position = Vector(0, 0)
    sprite.right = params.position.x
    expected = results.right
    assert sprite.left == expected.left
    assert sprite.right == expected.right
    assert sprite.top == expected.top
    assert sprite.bottom == expected.bottom

    sprite.position = Vector(0, 0)
    sprite.top = params.position.y
    expected = results.top
    assert sprite.left == expected.left
    assert sprite.right == expected.right
    assert sprite.top == expected.top
    assert sprite.bottom == expected.bottom

    sprite.position = Vector(0, 0)
    sprite.bottom = params.position.y
    expected = results.bottom
    assert sprite.left == expected.left
    assert sprite.right == expected.right
    assert sprite.top == expected.top
    assert sprite.bottom == expected.bottom


@pytest.mark.parametrize("sprite_class", RECTANGLE_SPRITE_CLASSES)
@pytest.mark.parametrize("params, results", [
    [
        SpriteParams(Vector(0, 0), 1, 1),
        CornerResults(
            Vector(-0.5, 0.5),
            Vector(0.5, 0.5),
            Vector(-0.5, -0.5),
            Vector(0.5, -0.5)
        )
    ],
    [
        SpriteParams(Vector(0, 0), 2, 1),
        CornerResults(
            Vector(-1, 0.5),
            Vector(1, 0.5),
            Vector(-1, -0.5),
            Vector(1, -0.5)
        )
    ],
    [
        SpriteParams(Vector(0, 0), 1, 2),
        CornerResults(
            Vector(-0.5, 1),
            Vector(0.5, 1),
            Vector(-0.5, -1),
            Vector(0.5, -1)
        )
    ],
    [
        SpriteParams(Vector(-54.8, 76.64), 1.06, 2.74),
        CornerResults(
            Vector(-55.33, 78.01),
            Vector(-54.269999999999996, 78.01),
            Vector(-55.33, 75.27),
            Vector(-54.269999999999996, 75.27)
        )
    ],
    [
        SpriteParams(Vector(-58.05, 96.62), 0.36, 2.02),
        CornerResults(
            Vector(-58.23, 97.63000000000001),
            Vector(-57.87, 97.63000000000001),
            Vector(-58.23, 95.61),
            Vector(-57.87, 95.61),
        )
    ]
])
def test_sprite_corners_access(sprite_class, params: SpriteParams, results: CornerResults):
    sprite = sprite_class(
        position=params.position,
        width=params.width,
        height=params.height,
    )
    assert sprite.top_left == results.top_left
    assert sprite.top_right == results.top_right
    assert sprite.bottom_left == results.bottom_left
    assert sprite.bottom_right == results.bottom_right


@pytest.mark.parametrize("sprite_class", RECTANGLE_SPRITE_CLASSES)
@pytest.mark.parametrize("params, setter_results", [
    [
        SpriteParams(Vector(0, 0), 1, 1),
        CornerSetterResults(
            CornerResults(Vector(0, 0), Vector(1, 0), Vector(0, -1), Vector(1, -1)),
            CornerResults(Vector(-1, 0), Vector(0, 0), Vector(-1, -1), Vector(0, -1)),
            CornerResults(Vector(0, 1), Vector(1, 1), Vector(0, 0), Vector(1, 0)),
            CornerResults(Vector(-1, 1), Vector(0, 1), Vector(-1, 0), Vector(0, 0)),
        )
    ],
    [
        SpriteParams(Vector(0, 0), 2, 1),
        CornerSetterResults(
            CornerResults(Vector(0, 0), Vector(2, 0), Vector(0, -1), Vector(2, -1)),
            CornerResults(Vector(-2, 0), Vector(0, 0), Vector(-2, -1), Vector(0, -1)),
            CornerResults(Vector(0, 1), Vector(2, 1), Vector(0, 0), Vector(2, 0)),
            CornerResults(Vector(-2, 1), Vector(0, 1), Vector(-2, 0), Vector(0, 0))
        )
    ],
    [
        SpriteParams(Vector(200, 200), 1, 1),
        CornerSetterResults(
            CornerResults(Vector(200, 200), Vector(201, 200), Vector(200, 199), Vector(201, 199)),
            CornerResults(Vector(199, 200), Vector(200, 200), Vector(199, 199), Vector(200, 199)),
            CornerResults(Vector(200, 201), Vector(201, 201), Vector(200, 200), Vector(201, 200)),
            CornerResults(Vector(199, 201), Vector(200, 201), Vector(199, 200), Vector(200, 200))
        )
    ]
])
def test_sprite_corners_set(sprite_class, params: SpriteParams, setter_results: CornerSetterResults):
    sprite = sprite_class(width=params.width, heigh=params.height)

    sprite.top_left = params.position
    results = setter_results.top_left
    assert sprite.top_left == results.top_left
    assert sprite.top_right == results.top_right
    assert sprite.bottom_left == results.bottom_left
    assert sprite.bottom_right == results.bottom_right

    sprite.top_right = params.position
    results = setter_results.top_right
    assert sprite.top_left == results.top_left
    assert sprite.top_right == results.top_right
    assert sprite.bottom_left == results.bottom_left
    assert sprite.bottom_right == results.bottom_right

    sprite.bottom_left = params.position
    results = setter_results.bottom_left
    assert sprite.top_left == results.top_left
    assert sprite.top_right == results.top_right
    assert sprite.bottom_left == results.bottom_left
    assert sprite.bottom_right == results.bottom_right

    sprite.bottom_right = params.position
    results = setter_results.bottom_right
    assert sprite.top_left == results.top_left
    assert sprite.top_right == results.top_right
    assert sprite.bottom_left == results.bottom_left
    assert sprite.bottom_right == results.bottom_right


def test_rectangle_shape_mixin_center():
    class TestSprite(RectangleShapeMixin, BaseSprite):
        pass

    test_sprite = TestSprite()

    assert test_sprite.center == test_sprite.position

    test_sprite.center = Vector(100, 100)

    assert test_sprite.center == test_sprite.position
    assert test_sprite.center == Vector(100, 100)
