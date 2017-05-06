from unittest import TestCase

from ppb import BaseSprite, Vector


class TestBaseSprite(TestCase):

    def setUp(self):
        self.sprite = BaseSprite()
        self.wide_sprite = BaseSprite(size=2, pos=(2, 2))

    def test_pos(self):
        self.assertEqual(self.sprite.pos, Vector(0, 0))
        self.assertEqual(self.wide_sprite.pos, Vector(2, 2))

    def test_center(self):
        self.assertEqual(self.sprite.center, self.sprite.pos)

        self.sprite.center = 1, 1
        self.assertEqual(self.sprite.pos.x, 1)
        self.assertEqual(self.sprite.pos.y, 1)
        self.assertEqual(self.sprite.center, self.sprite.pos)

        self.sprite.center = Vector(2, 2)
        self.assertEqual(self.sprite.pos.x, 2)
        self.assertEqual(self.sprite.pos.y, 2)

        self.sprite.center += -1, -1
        self.assertEqual(self.sprite.pos.x, 1)
        self.assertEqual(self.sprite.pos.y, 1)

        self.sprite.center += 0, 1
        self.assertEqual(self.sprite.pos.x, 1)
        self.assertEqual(self.sprite.pos.y, 2)

    def test_left(self):
        self.assertEqual(self.sprite.left, -0.5)
        self.assertEqual(self.wide_sprite.left, 1)

        self.sprite.left = 0
        self.assertEqual(self.sprite.pos.x, 0.5)
        self.assertEqual(self.sprite.pos.y, 0)

        self.sprite.left += 2
        self.assertEqual(self.sprite.pos.x, 2.5)
        self.assertEqual(self.sprite.pos.y, 0)

    def test_right(self):
        self.assertEqual(self.sprite.right, 0.5)
        self.assertEqual(self.wide_sprite.right, 3)

        self.sprite.right = 0
        self.assertEqual(self.sprite.pos.x, -0.5)
        self.assertEqual(self.sprite.pos.y, 0)

        self.sprite.right += 2
        self.assertEqual(self.sprite.pos.x, 1.5)
        self.assertEqual(self.sprite.pos.y, 0)

    def test_top(self):
        self.assertEqual(self.sprite.top, -0.5)
        self.assertEqual(self.wide_sprite.top, 1)

        self.sprite.top = 0
        self.assertEqual(self.sprite.pos.x, 0)
        self.assertEqual(self.sprite.pos.y, 0.5)

        self.sprite.top += 2
        self.assertEqual(self.sprite.pos.x, 0)
        self.assertEqual(self.sprite.pos.y, 2.5)

    def test_bottom(self):
        self.assertEqual(self.sprite.bottom, 0.5)
        self.assertEqual(self.wide_sprite.bottom, 3)

        self.sprite.bottom = 0
        self.assertEqual(self.sprite.pos.x, 0)
        self.assertEqual(self.sprite.pos.y, -0.5)

        self.sprite.bottom += 2
        self.assertEqual(self.sprite.pos.x, 0)
        self.assertEqual(self.sprite.pos.y, 1.5)

    def test_center_accessors(self):
        self.sprite.center.x = 20
        self.assertEqual(self.sprite.pos.x, 20)
        self.assertEqual(self.sprite.pos.y, 0)

        self.sprite.center.y = 15
        self.assertEqual(self.sprite.pos.x, 20)
        self.assertEqual(self.sprite.pos.y, 15)

    def test_left_top(self):
        self.assertEqual(self.sprite.left.top, Vector(-0.5, -0.5))

        self.sprite.left.top = (2, 2)
        self.assertEqual(self.sprite.left.top, Vector(2, 2))

        self.sprite.left.top += (2, 2)
        self.assertEqual(self.sprite.left.top, Vector(4, 4))

        result = self.sprite.left.top + (3, 3)
        self.assertEqual(result, Vector(7, 7))

        self.assertEqual(self.sprite.pos, Vector(4.5, 4.5))

    def test_left_bottom(self):
        self.assertEqual(self.sprite.left.bottom, Vector(-0.5, 0.5))

        self.sprite.left.bottom = (1, 2)
        self.assertEqual(self.sprite.left.bottom, Vector(1, 2))

        self.sprite.left.bottom += (2, 1)
        self.assertEqual(self.sprite.left.bottom, Vector(3, 3))

        result = self.sprite.left.bottom + (3, 2)
        self.assertEqual(result, Vector(6, 5))

        self.assertEqual(self.sprite.pos, Vector(3.5, 2.5))

    def test_left_center(self):
        self.assertEqual(self.sprite.left.center, Vector(-0.5, 0))

        self.sprite.left.center = (1, 1)
        self.assertEqual(self.sprite.left.center, Vector(1, 1))

        self.sprite.left.center += (2, 1)
        self.assertEqual(self.sprite.left.center, Vector(3, 2))

        result = self.sprite.left.center + (2, 3)
        self.assertEqual(result, Vector(5, 5))

        self.assertEqual(self.sprite.pos, Vector(3.5, 2))

    def test_right_bottom(self):
        self.assertEqual(self.sprite.right.bottom, Vector(0.5, 0.5))

        self.sprite.right.bottom = (1, 1)
        self.assertEqual(self.sprite.right.bottom, Vector(1, 1))

        self.sprite.right.bottom += (2, 1)
        self.assertEqual(self.sprite.right.bottom, Vector(3, 2))

        result = self.sprite.right.bottom + (2, 3)
        self.assertEqual(result, Vector(5, 5))

        self.assertEqual(self.sprite.pos, Vector(2.5, 1.5))

    def test_right_top(self):
        self.assertEqual(self.sprite.right.top, Vector(0.5, -0.5))

        self.sprite.right.top = (1, 1)
        self.assertEqual(self.sprite.right.top, Vector(1, 1))

        self.sprite.right.top += (2, 1)
        self.assertEqual(self.sprite.right.top, Vector(3, 2))

        result = self.sprite.right.top + (2, 3)
        self.assertEqual(result, Vector(5, 5))

        self.assertEqual(self.sprite.pos, Vector(2.5, 2.5))

    def test_right_center(self):
        self.assertEqual(self.sprite.right.center, Vector(0.5, 0))

        self.sprite.right.center = (1, 1)
        self.assertEqual(self.sprite.right.center, Vector(1, 1))

        self.sprite.right.center += (2, 1)
        self.assertEqual(self.sprite.right.center, Vector(3, 2))

        result = self.sprite.right.center + (2, 3)
        self.assertEqual(result, Vector(5, 5))

        self.assertEqual(self.sprite.pos, Vector(2.5, 2))

    def test_top_left(self):
        pass

    def test_top_right(self):
        pass

    def test_top_center(self):
        pass