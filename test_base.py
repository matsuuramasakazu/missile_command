import unittest
from base import Base
from constants import *
from test_game_platform import TestGamePlatform

class TestBase(unittest.TestCase):
    def setUp(self):
        self.platform = TestGamePlatform()

    def test_base_creation(self):
        base = Base(100, self.platform)
        self.assertEqual(base.x, 100)
        self.assertEqual(base.y, BASE_Y)
        self.assertTrue(base.is_alive)

    def test_base_creation_invalid_x(self):
        with self.assertRaises(TypeError):
            Base("abc", self.platform)
