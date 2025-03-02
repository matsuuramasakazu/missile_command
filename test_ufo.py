import unittest
import pyxel
from ufo import UFO
from constants import *

class TestUFO(unittest.TestCase):
    def test_ufo_creation(self):
        ufo = UFO(100, 50)
        self.assertEqual(ufo.x, 100)
        self.assertEqual(ufo.y, 50)
        self.assertTrue(ufo.is_alive)

    def test_ufo_update(self):
        ufo = UFO(100, 50)
        ufo.update()
        self.assertEqual(ufo.x, 100 - UFO_SPEED)
        ufo.x = -UFO_WIDTH - 1
        ufo.update()
        self.assertFalse(ufo.is_alive)
