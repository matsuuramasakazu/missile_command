import unittest
from city import City
from constants import *
from test_game_platform import TestGamePlatform # Added

class TestCity(unittest.TestCase):
    def setUp(self):
        self.platform = TestGamePlatform() # Added

    def test_city_creation(self):
        city = City(50, self.platform) # Modified: Added platform
        self.assertEqual(city.x, 50)
        self.assertEqual(city.y, CITY_Y)
        self.assertTrue(city.is_alive)

    # Assuming City constructor might also have type checks for x,
    # similar to Base. If there were tests for invalid x, they'd be updated too.
    # For example:
    # def test_city_creation_invalid_x(self):
    #     with self.assertRaises(TypeError):
    #         City("abc", self.platform)
