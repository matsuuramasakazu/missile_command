import unittest
import pyxel
from unittest.mock import patch
from meteor_manager import MeteorManager
from constants import *
from test_game import TestGame

class TestMeteorManager(unittest.TestCase):
    def setUp(self):
        if TestGame._is_pyxel_initialized == False:
            pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Missile Command")
            TestGame._is_pyxel_initialized = True

        self.manager = MeteorManager([])

    @patch('pyxel.frame_count', METEOR_SPAWN_INTERVAL)
    @patch('meteor_manager.random.randint')
    @patch('meteor_manager.random.uniform')
    def test_update_meteor_spawn(self, mock_uniform, mock_randint):
        mock_uniform.return_value = 0  # Any value within -METEOR_ANGLE_RANGE to METEOR_ANGLE_RANGE
        mock_randint.return_value = 100  # Any value between 0 and SCREEN_WIDTH

        self.manager.update()
        self.assertEqual(len(self.manager.meteors), METEOR_SPAWN_COUNT)
