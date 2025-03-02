import unittest
import pyxel
from unittest.mock import patch
from game import Game
from constants import *

class TestGame(unittest.TestCase):
    _is_pyxel_initialized = False

    def setUp(self):
        if TestGame._is_pyxel_initialized == False:
            pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Missile Command")
            TestGame._is_pyxel_initialized = True

        self.game = Game()

    def test_reset(self):
        self.game.reset()
        self.assertEqual(len(self.game.bases), 3)
        self.assertEqual(len(self.game.cities), 6)
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.game_over)

    @patch('pyxel.frame_count', 0)
    @patch('pyxel.btnp')
    def test_update_missile_launch(self, mock_btnp):
        mock_btnp.return_value = True
        pyxel.mouse_x = 200
        pyxel.mouse_y = 150

        self.game.update()
        self.assertEqual(len(self.game.missile_manager.missiles), 1)

    def test_check_game_over_true(self):
        for base in self.game.bases:
            base.is_alive = False
        for city in self.game.cities:
            city.is_alive = False
        self.game.check_game_over()
        self.assertTrue(self.game.game_over)

    def test_check_game_over_false(self):
        self.game.check_game_over()
        self.assertFalse(self.game.game_over)
