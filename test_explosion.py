import unittest
from explosion import Explosion
from constants import * # This should import EXPLOSION_RADIUS_MAX, EXPLOSION_DURATION
from test_game_platform import TestGamePlatform

# Define constants locally if not reliably imported via `from constants import *`
# These values were previously assumed based on test logic.
FALLBACK_EXPLOSION_SPEED = 0.5
FALLBACK_EXPLOSION_DURATION_DECREMENT = 1.5

class TestExplosion(unittest.TestCase):
    def setUp(self):
        self.platform = TestGamePlatform()
        # Try to use constants from import, fallback if NameError occurs (though tests can't catch this here)
        # For safety in tests, we'll directly use the fallback or ensure they are defined before use.
        self.explosion_speed = globals().get('EXPLOSION_SPEED', FALLBACK_EXPLOSION_SPEED)
        self.explosion_duration_decrement = globals().get('EXPLOSION_DURATION_DECREMENT', FALLBACK_EXPLOSION_DURATION_DECREMENT)


    def test_explosion_creation(self):
        explosion = Explosion(10, 20, self.platform)
        self.assertEqual(explosion.x, 10)
        self.assertEqual(explosion.y, 20)
        self.assertEqual(explosion.radius, 1) # Initial radius
        self.assertEqual(explosion.max_radius, EXPLOSION_RADIUS_MAX)
        self.assertEqual(explosion.duration, EXPLOSION_DURATION)
        self.assertTrue(explosion.is_alive)

    def test_explosion_update(self):
        explosion = Explosion(10, 20, self.platform)

        initial_radius = explosion.radius
        initial_duration = explosion.duration

        explosion.update()

        self.assertEqual(explosion.radius, initial_radius + self.explosion_speed)
        self.assertEqual(explosion.duration, initial_duration - self.explosion_duration_decrement)

        max_updates = 0
        if self.explosion_duration_decrement > 0:
            max_updates = int(initial_duration / self.explosion_duration_decrement) + 5
        else:
            max_updates = int(initial_duration / 0.1) + 5

        for i in range(max_updates):
            if not explosion.is_alive:
                break
            explosion.update()
            if i == max_updates -1:
                self.assertFalse(explosion.is_alive, "Explosion did not become inactive within max_updates")

        self.assertFalse(explosion.is_alive)
