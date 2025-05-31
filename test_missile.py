import unittest
from missile import Missile
from explosion import Explosion
from base import Base
from constants import *
from test_game_platform import TestGamePlatform # Added

class TestMissile(unittest.TestCase):
    def setUp(self):
        self.platform = TestGamePlatform()
        # Create a base with the platform for tests that need a Base instance
        self.base = Base(100, self.platform)

    def test_missile_creation(self):
        # Missile(base: Base, target_x: int, target_y: int, platform: IGamePlatform)
        missile = Missile(self.base, 200, 100, self.platform) # Added platform
        self.assertEqual(missile.start_x, self.base.x) # Base x is 100
        self.assertEqual(missile.start_y, BASE_Y)
        self.assertEqual(missile.target_x, 200)
        self.assertEqual(missile.target_y, 100)
        self.assertEqual(missile.speed, MISSILE_SPEED)
        self.assertTrue(missile.is_alive)
        # The original test_missile.py had `self.assertIsNone(missile.explosion)` commented out.
        # If a missile creates its explosion on target reach (in update),
        # then it shouldn't have one at creation. This depends on Missile's internal logic.
        # For now, keeping it as it was (commented or absent).

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

        missile = Missile(self.base, target_x, target_y, self.platform) # Added platform

        # Loop to ensure it reaches, as exact steps can be tricky with float precision / speed
        new_explosion = None
        for _ in range(10): # Max 10 updates, should be enough for short distances
            if not missile.is_alive:
                break
            new_explosion = missile.update() # update should use platform if needed for timing/drawing

        self.assertFalse(missile.is_alive)
        self.assertIsNotNone(new_explosion)
        self.assertIsInstance(new_explosion, Explosion)
        # Optional: Check if the explosion has the platform
        # self.assertEqual(new_explosion.platform, self.platform)
        # Optional: Check explosion position
        # self.assertEqual(new_explosion.x, target_x)
        # self.assertEqual(new_explosion.y, target_y)

# Note: The original test_missile_update_reach_target had a target (105, BASE_Y)
# with base at (100, BASE_Y). This is a horizontal distance of 5.
# If MISSILE_SPEED is, for example, 4, it would take 2 updates to cover x=5.
# (x moves from 100 to 104 in 1st update, then 104 to 105 (target) in 2nd update if it stops exactly).
# The loop I added makes it more robust for varying speeds.
# The missile should become not alive once it reaches its target and creates an explosion.
# The Missile class is responsible for passing the platform to the Explosion it creates.
# The test just needs to provide the platform to the Missile.
