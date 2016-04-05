import unittest
import ppb.event


class TestKey(unittest.TestCase):

    def setUp(self):
        self.key = ppb.event.Key(65, "A")

    def test_representation(self):
        self.assertEqual(self.key.__repr__(), 'Key(65, "A")')
