import unittest
import pyxel
import math
from unittest.mock import patch
from missile import Missile
from base import Base
from constants import *

class TestMissile(unittest.TestCase):
    def test_missile_creation(self):
        base = Base(100)
        missile = Missile(base, 200, 100)
        self.assertEqual(missile.start_x, 100)
        self.assertEqual(missile.start_y, BASE_Y)
        self.assertEqual(missile.target_x, 200)
        self.assertEqual(missile.target_y, 100)
        self.assertEqual(missile.speed, MISSILE_SPEED)
        self.assertTrue(missile.is_alive)
        self.assertIsNone(missile.explosion)

    def test_missile_update_reach_target(self):
        base = Base(100)
        missile = Missile(base, 105, BASE_Y)
        missile.update()
        self.assertFalse(missile.is_alive)
        self.assertIsNotNone(missile.explosion)
