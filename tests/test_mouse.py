from pytest import fixture
from pytest import raises

from ppb import Vector
from ppb.mouse import Mouse
from ppb.mouse import FeatureNotProvided


@fixture
def empty_mouse():
    """A default mouse with no system features."""
    return Mouse()


def test_press_error(empty_mouse):
    with raises(FeatureNotProvided):
        empty_mouse.press(0)
        # Button is arbitrary,
        # consider testing against all three common buttons.

def test_move_raises(empty_mouse):
    with raises(FeatureNotProvided):
        empty_mouse.move(Vector(3, 2))
        # Vector is arbitrary. Consider testing ten random vectors.


def test_move_to_raises(empty_mouse):
    with raises(FeatureNotProvided):
        empty_mouse.move_to(Vector(-100, 500))
        # Vector is arbitrary. Consider testing ten random vectors.



