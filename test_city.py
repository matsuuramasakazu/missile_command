import unittest
from city import City
from constants import *
from test_game_platform import TestGamePlatform # Added

class TestCity(unittest.TestCase):
    def setUp(self):
        self.platform = TestGamePlatform()

    def test_city_creation(self):
        city = City(50, self.platform)
        self.assertEqual(city.x, 50)
        self.assertEqual(city.y, CITY_Y)
        self.assertTrue(city.is_alive)
