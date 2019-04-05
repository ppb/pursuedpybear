from unittest import TestCase

from ppb import BaseSprite, Vector
from ppb.sprites import Rotatable


class TestBaseSprite(TestCase):

    def setUp(self):
        self.sprite = BaseSprite()
        self.wide_sprite = BaseSprite(size=2, pos=(2, 2))

    def test_pos(self):
        self.assertEqual(self.sprite.position, Vector(0, 0))
        self.assertEqual(self.wide_sprite.position, Vector(2, 2))

    def test_center(self):
        self.assertEqual(self.sprite.center, self.sprite.position)

        self.sprite.center = 1, 1
        self.assertEqual(self.sprite.position.x, 1)
        self.assertEqual(self.sprite.position.y, 1)
        self.assertEqual(self.sprite.center, self.sprite.position)

        self.sprite.center = Vector(2, 2)
        self.assertEqual(self.sprite.position.x, 2)
        self.assertEqual(self.sprite.position.y, 2)

        self.sprite.center += -1, -1
        self.assertEqual(self.sprite.position.x, 1)
        self.assertEqual(self.sprite.position.y, 1)

        self.sprite.center += 0, 1
        self.assertEqual(self.sprite.position.x, 1)
        self.assertEqual(self.sprite.position.y, 2)

    def test_left(self):
        self.assertEqual(self.sprite.left, -0.5)
        self.assertEqual(self.wide_sprite.left, 1)

        self.sprite.left = 0
        self.assertEqual(self.sprite.position.x, 0.5)
        self.assertEqual(self.sprite.position.y, 0)

        self.sprite.left += 2
        self.assertEqual(self.sprite.position.x, 2.5)
        self.assertEqual(self.sprite.position.y, 0)

    def test_right(self):
        self.assertEqual(self.sprite.right, 0.5)
        self.assertEqual(self.wide_sprite.right, 3)

        self.sprite.right = 0
        self.assertEqual(self.sprite.position.x, -0.5)
        self.assertEqual(self.sprite.position.y, 0)

        self.sprite.right += 2
        self.assertEqual(self.sprite.position.x, 1.5)
        self.assertEqual(self.sprite.position.y, 0)

    def test_top(self):
        self.assertEqual(self.sprite.top, -0.5)
        self.assertEqual(self.wide_sprite.top, 1)

        self.sprite.top = 0
        self.assertEqual(self.sprite.position.x, 0)
        self.assertEqual(self.sprite.position.y, 0.5)

        self.sprite.top += 2
        self.assertEqual(self.sprite.position.x, 0)
        self.assertEqual(self.sprite.position.y, 2.5)

    def test_bottom(self):
        self.assertEqual(self.sprite.bottom, 0.5)
        self.assertEqual(self.wide_sprite.bottom, 3)

        self.sprite.bottom = 0
        self.assertEqual(self.sprite.position.x, 0)
        self.assertEqual(self.sprite.position.y, -0.5)

        self.sprite.bottom += 2
        self.assertEqual(self.sprite.position.x, 0)
        self.assertEqual(self.sprite.position.y, 1.5)

    def test_center_accessors(self):
        self.sprite.center.x = 20
        self.assertEqual(self.sprite.position.x, 20)
        self.assertEqual(self.sprite.position.y, 0)

        self.sprite.center.y = 15
        self.assertEqual(self.sprite.position.x, 20)
        self.assertEqual(self.sprite.position.y, 15)

    def test_left_top(self):
        self.assertEqual(self.sprite.left.top, Vector(-0.5, -0.5))

        self.sprite.left.top = (2, 2)
        self.assertEqual(self.sprite.left.top, Vector(2, 2))

        self.sprite.left.top += (2, 2)
        self.assertEqual(self.sprite.left.top, Vector(4, 4))

        result = self.sprite.left.top + (3, 3)
        self.assertEqual(result, Vector(7, 7))

        self.assertEqual(self.sprite.position, Vector(4.5, 4.5))

    def test_left_bottom(self):
        self.assertEqual(self.sprite.left.bottom, Vector(-0.5, 0.5))

        self.sprite.left.bottom = (1, 2)
        self.assertEqual(self.sprite.left.bottom, Vector(1, 2))

        self.sprite.left.bottom += (2, 1)
        self.assertEqual(self.sprite.left.bottom, Vector(3, 3))

        result = self.sprite.left.bottom + (3, 2)
        self.assertEqual(result, Vector(6, 5))

        self.assertEqual(self.sprite.position, Vector(3.5, 2.5))

    def test_left_center(self):
        self.assertEqual(self.sprite.left.center, Vector(-0.5, 0))

        self.sprite.left.center = (1, 1)
        self.assertEqual(self.sprite.left.center, Vector(1, 1))

        self.sprite.left.center += (2, 1)
        self.assertEqual(self.sprite.left.center, Vector(3, 2))

        result = self.sprite.left.center + (2, 3)
        self.assertEqual(result, Vector(5, 5))

        self.assertEqual(self.sprite.position, Vector(3.5, 2))

    def test_right_bottom(self):
        self.assertEqual(self.sprite.right.bottom, Vector(0.5, 0.5))

        self.sprite.right.bottom = (1, 1)
        self.assertEqual(self.sprite.right.bottom, Vector(1, 1))

        self.sprite.right.bottom += (2, 1)
        self.assertEqual(self.sprite.right.bottom, Vector(3, 2))

        result = self.sprite.right.bottom + (2, 3)
        self.assertEqual(result, Vector(5, 5))

        self.assertEqual(self.sprite.position, Vector(2.5, 1.5))

    def test_right_top(self):
        self.assertEqual(self.sprite.right.top, Vector(0.5, -0.5))

        self.sprite.right.top = (1, 1)
        self.assertEqual(self.sprite.right.top, Vector(1, 1))

        self.sprite.right.top += (2, 1)
        self.assertEqual(self.sprite.right.top, Vector(3, 2))

        result = self.sprite.right.top + (2, 3)
        self.assertEqual(result, Vector(5, 5))

        self.assertEqual(self.sprite.position, Vector(2.5, 2.5))

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

    def test_top_left(self):
        self.assertEqual(self.sprite.top.left, Vector(-0.5, -0.5))

        self.sprite.top.left = (2, 2)
        self.assertEqual(self.sprite.top.left, Vector(2, 2))

        self.sprite.top.left += (2, 2)
        self.assertEqual(self.sprite.top.left, Vector(4, 4))

        result = self.sprite.top.left + (3, 3)
        self.assertEqual(result, Vector(7, 7))

        self.assertEqual(self.sprite.position, Vector(4.5, 4.5))

    def test_top_right(self):
        self.assertEqual(self.sprite.top.right, Vector(0.5, -0.5))

        self.sprite.top.right = (1, 1)
        self.assertEqual(self.sprite.top.right, Vector(1, 1))

        self.sprite.top.right += (2, 1)
        self.assertEqual(self.sprite.top.right, Vector(3, 2))

        result = self.sprite.top.right + (2, 3)
        self.assertEqual(result, Vector(5, 5))

        self.assertEqual(self.sprite.position, Vector(2.5, 2.5))

    def test_top_center(self):
        self.assertEqual(self.sprite.top.center, Vector(0, -0.5))

        self.sprite.top.center = (1, 1)
        self.assertEqual(self.sprite.top.center, Vector(1, 1))

    def test_top_top(self):
        self.assertRaises(AttributeError, getattr, self.sprite.top, "top")
        self.assertRaises(AttributeError, setattr, self.sprite.top, "top", Vector(1, 1))

    def test_top_bottom(self):
        self.assertRaises(AttributeError, getattr, self.sprite.top, "bottom")
        self.assertRaises(AttributeError, setattr, self.sprite.top, "bottom", Vector(1, 1))

    def test_bottom_left(self):
        self.assertEqual(self.sprite.bottom.left, Vector(-0.5, 0.5))

        self.sprite.bottom.left = (2, 2)
        self.assertEqual(self.sprite.bottom.left, Vector(2, 2))

        self.sprite.bottom.left += (2, 2)
        self.assertEqual(self.sprite.bottom.left, Vector(4, 4))

        result = self.sprite.bottom.left + (3, 3)
        self.assertEqual(result, Vector(7, 7))

        self.assertEqual(self.sprite.position, Vector(4.5, 3.5))

    def test_bottom_right(self):
        self.assertEqual(self.sprite.bottom.right, Vector(0.5, 0.5))

        self.sprite.bottom.right = (1, 1)
        self.assertEqual(self.sprite.bottom.right, Vector(1, 1))

        self.sprite.bottom.right += (2, 1)
        self.assertEqual(self.sprite.bottom.right, Vector(3, 2))

        result = self.sprite.bottom.right + (2, 3)
        self.assertEqual(result, Vector(5, 5))

        self.assertEqual(self.sprite.position, Vector(2.5, 1.5))

    def test_bottom_center(self):
        self.assertEqual(self.sprite.bottom.center, Vector(0, 0.5))

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
    class TestSprite(BaseSprite):
        size = 1.1

    assert TestSprite().left < -0.5


def test_rotatable_instatiation():
    rotatable = Rotatable()
    assert rotatable.rotation == 0


def test_rotatable_subclass():

    class TestRotatable(Rotatable):
        _rotation = 180
        basis = Vector(0, 1)

    rotatable = TestRotatable()
    assert rotatable.rotation == 180
    assert rotatable.facing == Vector(0, -1)


def test_rotatable_rotation_setter():
    rotatable = Rotatable()

    rotatable.rotation = 405
    assert rotatable.rotation == 45


def test_rotatable_rotate():
    rotatable = Rotatable()

    assert rotatable.rotation == 0
    rotatable.rotate(180)
    assert rotatable.rotation == 180
    rotatable.rotate(200)
    assert rotatable.rotation == 20
    rotatable.rotate(-300)
    assert rotatable.rotation == 80


def test_rotatable_base_sprite():
    test_sprite = BaseSprite()

    test_sprite.rotate(1)
    assert test_sprite.rotation == 1
