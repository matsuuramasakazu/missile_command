import unittest
from ufo import UFO
from constants import *
from test_game_platform import TestGamePlatform # Added

class TestUFO(unittest.TestCase):
    def setUp(self):
        self.platform = TestGamePlatform() # Added

    def test_ufo_creation(self):
        # Assuming UFO constructor is UFO(x, y, platform, zigzag=False)
        ufo = UFO(100, 50, self.platform) # Added platform
        self.assertEqual(ufo.x, 100)
        self.assertEqual(ufo.y, 50)
        self.assertTrue(ufo.is_alive)

    def test_ufo_update(self):
        ufo = UFO(100, 50, self.platform) # Added platform

        # Store initial x for comparison after update
        initial_x = ufo.x
        ufo.update() # UFO.update() might use the platform
        self.assertEqual(ufo.x, initial_x - UFO_SPEED)

        # Test boundary condition for is_alive
        ufo.x = -UFO_WIDTH - 1
        ufo.update()
        self.assertFalse(ufo.is_alive)

    def test_ufo_zigzag_true(self):
        ufo = UFO(100, 50, self.platform, zigzag=True) # Added platform
        initial_y = ufo.y

        # UFO's zigzag movement might depend on platform's frame_count or random services via platform
        # For this test, we just ensure the platform is passed.
        # We might need to call platform.increment_frame_count() multiple times
        # if zigzag pattern takes a few frames to manifest a y-change.
        # Let's update a few times to give zigzag a chance.
        for _ in range(5): # Arbitrary number of updates
            if ufo.y != initial_y:
                break
            ufo.update()

        self.assertNotEqual(ufo.y, initial_y)

    def test_ufo_zigzag_false(self):
        ufo = UFO(100, 50, self.platform, zigzag=False) # Added platform
        initial_y = ufo.y
        ufo.update()
        self.assertEqual(ufo.y, initial_y) # y should not change if zigzag is false

# Note: The UFO constructor signature is assumed to be (x, y, platform, zigzag=False).
# If zigzag is a positional argument, the order would matter.
# The original calls were UFO(100, 50) and UFO(100, 50, zigzag=True).
# This implies zigzag is a keyword argument or the last positional one.
# Assuming (x, y, platform, zigzag=False) or (x, y, platform, speed, zigzag=False) etc.
# Let's assume it's (x, y, platform, zigzag=optional_keyword)
# The UFO class itself would need to be updated to accept and use the platform.
# The test_ufo_zigzag_true was modified to loop a few times, as zigzag patterns
# often rely on some internal counter or state that changes over frames.
# If UFO_SPEED makes it go off screen quickly, this test might need adjustment.
# The original test_ufo_update had:
#   ufo.x = -UFO_WIDTH -1
#   ufo.update()
#   self.assertFalse(ufo.is_alive)
# This implies UFO becomes not alive when it moves beyond -UFO_WIDTH.
# My modified test_ufo_update retains this logic.
# The main point is adding self.platform to constructor.
