import unittest
import pyxel
import math
from unittest.mock import patch
from meteor import Meteor
from base import Base
from city import City
from constants import *

class TestMeteor(unittest.TestCase):
    def test_meteor_creation(self):
        meteor = Meteor(10, 20, 3)
        self.assertEqual(meteor.x, 10)
        self.assertEqual(meteor.y, 20)
        self.assertEqual(meteor.speed, 3)
        self.assertTrue(meteor.is_alive)

    @patch('meteor.Meteor._check_base_collision')
    def test_meteor_update_base_collision(self, mock_check_base_collision):
        bases = [Base(100)]
        cities = []
        explosions = []
        meteor = Meteor(100, BASE_Y - 4, 1)
        mock_check_base_collision.return_value = None
        meteor.update(explosions)
        self.assertEqual(mock_check_base_collision.call_count, 0)

    @patch('meteor.Meteor._check_city_collision')
    def test_meteor_update_city_collision(self, mock_check_base_collision):
        bases = []
        cities = [City(100)]
        explosions = []
        meteor = Meteor(100, CITY_Y - 4, 1)
        mock_check_base_collision.return_value = None
        meteor.update(explosions)
        self.assertEqual(mock_check_base_collision.call_count, 0)

    def test_meteor_check_base_collision(self):
        bases = [Base(100)]
        explosions = []
        meteor = Meteor(100, BASE_Y - 4, 1)
        meteor._check_base_collision(bases, explosions)
        self.assertFalse(meteor.is_alive)
        self.assertFalse(bases[0].is_alive)
        self.assertEqual(len(explosions), 1)

    def test_meteor_check_city_collision(self):
        bases = []
        cities = [City(100)]
        explosions = []
        meteor = Meteor(100, CITY_Y - 4, 1)
        meteor._check_city_collision(cities, explosions)
        self.assertFalse(meteor.is_alive)
        self.assertFalse(cities[0].is_alive)
        self.assertEqual(len(explosions), 1)

    def test_meteor_move_angle_0(self):
        meteor = Meteor(10, 20, 3)
        meteor.angle = 0
        meteor._move()
        self.assertEqual(meteor.x, 10)
        self.assertEqual(meteor.y, 20 + 3)

    def test_meteor_move_angle_90(self):
        meteor = Meteor(10, 20, 3)
        meteor.angle = 90
        meteor._move()
        self.assertEqual(meteor.x, 10 + 3 * math.cos(math.radians(180)))
        self.assertEqual(meteor.y, 20 + 3 * math.sin(math.radians(180)))

    def test_meteor_move_angle_minus_90(self):
        meteor = Meteor(10, 20, 3)
        meteor.angle = -90
        meteor._move()
        self.assertEqual(meteor.x, 10 + 3 * math.cos(math.radians(0)))
        self.assertEqual(meteor.y, 20 + 3 * math.sin(math.radians(0)))

    def test_meteor_move_angle_45(self):
        meteor = Meteor(10, 20, 3)
        meteor.angle = 45
        meteor._move()
        self.assertAlmostEqual(meteor.x, 10 + 3 * math.cos(math.radians(135)))
        self.assertAlmostEqual(meteor.y, 20 + 3 * math.sin(math.radians(135)))

    def test_meteor_move_angle_minus_45(self):
        meteor = Meteor(10, 20, 3)
        meteor.angle = -45
        meteor._move()
        self.assertAlmostEqual(meteor.x, 10 + 3 * math.cos(math.radians(45)))
        self.assertAlmostEqual(meteor.y, 20 + 3 * math.sin(math.radians(45)))
