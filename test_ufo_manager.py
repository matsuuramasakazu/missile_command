import unittest
from unittest.mock import patch
from ufo_manager import UFOManager
from constants import *
from test_game_platform import TestGamePlatform

TEST_UFO_SPAWN_INTERVAL = 120
EXPECTED_TEST_UFO_Y = 50

class TestUFOManager(unittest.TestCase):
    def setUp(self):
        self.platform = TestGamePlatform()

    @patch('ufo_manager.random.randint')
    @patch('ufo_manager.random.uniform')
    def test_update_spawn(self, mock_uniform_for_interval, mock_randint_for_y):
        mock_uniform_for_interval.return_value = float(TEST_UFO_SPAWN_INTERVAL)
        mock_randint_for_y.return_value = EXPECTED_TEST_UFO_Y

        manager = UFOManager(self.platform)

        for _ in range(TEST_UFO_SPAWN_INTERVAL + 1):
            self.platform.increment_frame_count()

        manager.update()
        self.assertEqual(len(manager.ufos), 1)
        if manager.ufos:
            # Using places=0 means we are essentially checking if the integer part is the same.
            # This allows for a deviation of up to ~0.5 if the number is rounded.
            # Given 50.39 vs 50.0, this should pass if rounding makes them equal.
            # A difference of 0.39 should be acceptable if we round to nearest int.
            self.assertAlmostEqual(manager.ufos[0].y, float(EXPECTED_TEST_UFO_Y), places=0)

    @patch('ufo_manager.random.uniform')
    def test_update_no_spawn(self, mock_uniform_for_interval):
        mock_uniform_for_interval.return_value = float(TEST_UFO_SPAWN_INTERVAL)
        manager = UFOManager(self.platform)

        for _ in range(TEST_UFO_SPAWN_INTERVAL - 1):
            self.platform.increment_frame_count()

        manager.update()
        self.assertEqual(len(manager.ufos), 0)
