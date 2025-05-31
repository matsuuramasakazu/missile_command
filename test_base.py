import unittest
from base import Base
from constants import *
from test_game_platform import TestGamePlatform # Added

class TestBase(unittest.TestCase):
    def setUp(self):
        self.platform = TestGamePlatform() # Added

    def test_base_creation(self):
        base = Base(100, self.platform) # Modified: Added platform
        self.assertEqual(base.x, 100)
        self.assertEqual(base.y, BASE_Y)
        self.assertTrue(base.is_alive)

    def test_base_creation_invalid_x(self):
        with self.assertRaises(TypeError):
            Base("abc", self.platform) # Modified: Added platform
        # Test for invalid platform (optional, but good practice)
        with self.assertRaises(TypeError): # Or appropriate error like AttributeError
            Base(100, "not a platform")

# It's also possible that the TypeError for "abc" was meant for x,
# and the constructor might raise a different error if platform is missing.
# For now, the primary goal is to add the platform.
# If Base("abc") was meant to test x without platform, that test might need adjustment
# if the constructor signature change means platform is always required.
# Assuming platform is now a required argument after x.
# If Base("abc", self.platform) fails due to "abc" before platform check, the original intent is met.
# If it fails due to platform type error first, that's also a valid failure for incorrect usage.
# The test for "not a platform" is an explicit check for platform type.
# The original test was `Base("abc")`. If the number of args changed, it would be `TypeError`.
# If `Base("abc", self.platform)` is called, it would likely be a `TypeError` if `x` expects int.
# Let's stick to the primary change of adding platform.

class TestBase(unittest.TestCase): # Re-declaring to ensure clean overwrite
    def setUp(self):
        self.platform = TestGamePlatform()

    def test_base_creation(self):
        base = Base(100, self.platform)
        self.assertEqual(base.x, 100)
        self.assertEqual(base.y, BASE_Y)
        self.assertTrue(base.is_alive)

    def test_base_creation_invalid_x(self):
        # If Base constructor now strictly requires platform,
        # Base("abc") would raise TypeError due to missing argument.
        # If we pass platform, Base("abc", self.platform), it should still be TypeError for x.
        with self.assertRaises(TypeError):
            Base("abc", self.platform)

        # It's good practice to also test for invalid platform type if desired,
        # but the original test was about the type of 'x'.
        # For example:
        # with self.assertRaises(TypeError): # Or specific error if platform has type check
        #     Base(100, "not_a_platform_instance")
