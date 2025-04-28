import unittest
import pyxel
from unittest.mock import patch
from ufo_manager import UFOManager
from constants import *
from test_game import TestGame

class TestUFOManager(unittest.TestCase):
    def setUp(self):
        if TestGame._is_pyxel_initialized == False:
            pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Missile Command")
            TestGame._is_pyxel_initialized = True

    @patch('pyxel.frame_count', 0)
    @patch('ufo_manager.random.randint')
    @patch('ufo_manager.random.uniform')
    def test_update_spawn(self, mock_uniform, mock_randint):
        mock_uniform.return_value = 120
        mock_randint.return_value = 200

        self.ufo_manager = UFOManager()
        pyxel.frame_count = 121
        self.ufo_manager.update()
        self.assertEqual(len(self.ufo_manager.ufos), 1)
        self.assertAlmostEqual(self.ufo_manager.ufos[0].y, 200, delta=0.5)

    @patch('pyxel.frame_count', 0)
    @patch('ufo_manager.random.uniform')
    def test_update_no_spawn(self, mock_uniform):
        mock_uniform.return_value = 120
        self.ufo_manager = UFOManager()
        pyxel.frame_count = 119
        self.ufo_manager.update()
        self.assertEqual(len(self.ufo_manager.ufos), 0)
