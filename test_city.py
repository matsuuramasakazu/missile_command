import unittest
from city import City
from constants import *

class TestCity(unittest.TestCase):
    def test_city_creation(self):
        city = City(50)
        self.assertEqual(city.x, 50)
        self.assertEqual(city.y, CITY_Y)
        self.assertTrue(city.is_alive)
