import unittest
import ppb.event


class TestKey(unittest.TestCase):

    def setUp(self):
        self.key = ppb.event.Key(65, "A")

    def test_representation(self):
        self.assertEqual(self.key.__repr__(), 'Key(65, "A")')


class TestCollision(unittest.TestCase):

    def setUp(self):
        self.collision = ppb.event.Collision(1, 2)

    def test_representation(self):
        rep = self.collision.__repr__()
        self.assertIn(str(1), rep)
        self.assertIn(str(2), rep)
        self.assertNotIn(str(3), rep)
