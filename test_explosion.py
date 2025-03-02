import unittest
import pyxel
from explosion import Explosion
from constants import *

class TestExplosion(unittest.TestCase):
    def test_explosion_creation(self):
        explosion = Explosion(10, 20)
        self.assertEqual(explosion.x, 10)
        self.assertEqual(explosion.y, 20)
        self.assertEqual(explosion.radius, 1)
        self.assertEqual(explosion.max_radius, EXPLOSION_RADIUS_MAX)
        self.assertEqual(explosion.duration, EXPLOSION_DURATION)
        self.assertTrue(explosion.is_alive)

    def test_explosion_update(self):
        explosion = Explosion(10, 20)
        explosion.update()
        self.assertEqual(explosion.radius, 1.5)
        self.assertEqual(explosion.duration, 19)

        # Simulate until explosion is done
        for _ in range(EXPLOSION_DURATION):
            explosion.update()
        self.assertFalse(explosion.is_alive)
