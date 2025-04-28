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

    def test_ufo_zigzag_true(self):
        ufo = UFO(100, 50, zigzag=True)
        initial_y = ufo.y
        ufo.update()
        # y座標が変化していること
        self.assertNotEqual(ufo.y, initial_y)

    def test_ufo_zigzag_false(self):
        ufo = UFO(100, 50, zigzag=False)
        initial_y = ufo.y
        ufo.update()
        # y座標は変化しないこと
        self.assertEqual(ufo.y, initial_y)
