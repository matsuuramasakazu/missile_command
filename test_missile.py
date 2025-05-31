import unittest
from missile import Missile
from explosion import Explosion
from base import Base
from constants import *
from test_game_platform import TestGamePlatform

class TestMissile(unittest.TestCase):
    def setUp(self):
        self.platform = TestGamePlatform()
        # Create a base with the platform for tests that need a Base instance
        self.base = Base(100, self.platform)

    def test_missile_creation(self):
        # Missile(base: Base, target_x: int, target_y: int, platform: IGamePlatform)
        missile = Missile(self.base, 200, 100, self.platform)
        self.assertEqual(missile.start_x, self.base.x) # Base x is 100
        self.assertEqual(missile.start_y, BASE_Y)
        self.assertEqual(missile.target_x, 200)
        self.assertEqual(missile.target_y, 100)
        self.assertEqual(missile.speed, MISSILE_SPEED)
        self.assertTrue(missile.is_alive)

    def test_missile_update_reach_target(self):
        # Create a missile that will reach its target in one step or very few.
        # Missile speed is MISSILE_SPEED (e.g., 4)
        # If target is very close to base.
        # Original test used target (105, BASE_Y), base was (100, BASE_Y)
        # Distance is 5. If speed is 4, it reaches/passes in 2 updates.
        # If speed is >=5, it reaches in 1 update.
        # Let's make target distinct from start to ensure movement.
        target_x = self.base.x + MISSILE_SPEED
        target_y = BASE_Y - MISSILE_SPEED # Move diagonally up a bit

        missile = Missile(self.base, target_x, target_y, self.platform)

        # Loop to ensure it reaches, as exact steps can be tricky with float precision / speed
        new_explosion = None
        for _ in range(10): # Max 10 updates, should be enough for short distances
            if not missile.is_alive:
                break
            new_explosion = missile.update() # update should use platform if needed for timing/drawing

        self.assertFalse(missile.is_alive)
        self.assertIsNotNone(new_explosion)
        self.assertIsInstance(new_explosion, Explosion)
        self.assertEqual(new_explosion.x, target_x)
        self.assertEqual(new_explosion.y, target_y)
