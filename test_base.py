import unittest
from base import Base
from constants import *

class TestBase(unittest.TestCase):
    def test_base_creation(self):
        base = Base(100)
        self.assertEqual(base.x, 100)
        self.assertEqual(base.y, BASE_Y)
        self.assertTrue(base.is_alive)

    def test_base_creation_invalid_x(self):
        with self.assertRaises(TypeError):
            Base("abc")
