import unittest
import pyxel
from unittest.mock import patch
from missile_manager import MissileManager
from base import Base
from constants import *
from test_game import TestGame

class TestMissileManager(unittest.TestCase):
    def setUp(self):
        if TestGame._is_pyxel_initialized == False:
            pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Missile Command")
            TestGame._is_pyxel_initialized = True

        self.bases = [Base(x) for x in BASE_X_POSITIONS]
        self.manager = MissileManager(self.bases, [])

    @patch('pyxel.btnp')
    def test_update_missile_launch(self, mock_btnp):
        mock_btnp.return_value=True
        pyxel.mouse_x = BASE_X_POSITIONS[0]
        pyxel.mouse_y = 200
        self.manager.update()
        self.assertEqual(len(self.manager.missiles), 1)

    def test_find_nearest_base(self):
        nearest_base = self.manager.find_nearest_base(BASE_X_POSITIONS[0] + 10)
        self.assertEqual(nearest_base.x, BASE_X_POSITIONS[0])

    def test_find_nearest_base_no_alive_bases(self):
        for base in self.bases:
            base.is_alive = False
        nearest_base = self.manager.find_nearest_base(BASE_X_POSITIONS[0] + 10)
        self.assertIsNone(nearest_base)
