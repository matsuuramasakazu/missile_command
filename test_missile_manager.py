import unittest
# import pyxel # Removed
# from unittest.mock import patch # Removed (only used for pyxel.btnp)
from missile_manager import MissileManager
from base import Base
from constants import *
# from test_game import TestGame # Removed
from test_game_platform import TestGamePlatform # Added

class TestMissileManager(unittest.TestCase):
    def setUp(self):
        # Removed pyxel.init logic
        self.platform = TestGamePlatform()

        # Create Base instances with the platform
        self.bases = [Base(x, self.platform) for x in BASE_X_POSITIONS]

        # MissileManager(bases, explosions_quad_tree, platform)
        # Assuming the second argument is for explosions_quad_tree, pass an empty list or mock if needed.
        # For existing tests, an empty list was used.
        self.manager = MissileManager(self.bases, [], self.platform) # Added platform

    # Removed @patch('pyxel.btnp')
    def test_update_missile_launch(self): # Removed mock_btnp
        # Simulate mouse position and button press using the platform
        self.platform.set_mouse_position(BASE_X_POSITIONS[0], 200) # mouse_x, mouse_y
        self.platform.set_mouse_button_pressed(self.platform.get_mouse_button_left(), True)

        self.manager.update() # MissileManager.update() should use the platform for inputs

        self.assertEqual(len(self.manager.missiles), 1)

        # Check if the created missile has the platform (optional deep check)
        if self.manager.missiles:
            # Assuming Missile objects have a 'platform' attribute
            # self.assertEqual(self.manager.missiles[0].platform, self.platform)
            pass

        # Reset mouse button state
        self.platform.set_mouse_button_pressed(self.platform.get_mouse_button_left(), False)

    def test_find_nearest_base(self):
        # This test doesn't directly involve platform interactions after setup,
        # but relies on self.bases being correctly initialized with Base objects.
        nearest_base = self.manager.find_nearest_base(BASE_X_POSITIONS[0] + 10)
        self.assertEqual(nearest_base.x, BASE_X_POSITIONS[0])

    def test_find_nearest_base_no_alive_bases(self):
        for base in self.bases:
            base.is_alive = False # Bases are already platform-aware from setUp
        nearest_base = self.manager.find_nearest_base(BASE_X_POSITIONS[0] + 10)
        self.assertIsNone(nearest_base)

# Note: MissileManager is responsible for creating Missile objects.
# It must be updated to pass the platform to these Missiles.
# This test suite ensures MissileManager receives a platform and that
# inputs previously from pyxel are now simulated via the platform.
# The test for missile launch checks if a missile is added.
# A deeper test could verify that the missile created by the manager
# indeed has the platform, but that depends on Missile storing it.
# (which it should, as per test_missile.py refactoring).
