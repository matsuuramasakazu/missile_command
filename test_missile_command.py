import unittest
import pyxel
import math
import random
from unittest.mock import patch
from missile_command import *
from constants import * # Import constants


class TestBase(unittest.TestCase):
    def test_base_creation(self):
        base = Base(100)
        self.assertEqual(base.x, 100)
        self.assertEqual(base.y, BASE_Y)
        self.assertTrue(base.is_alive)

    def test_base_creation_invalid_x(self):
        with self.assertRaises(TypeError):
            Base("abc")


class TestCity(unittest.TestCase):
    def test_city_creation(self):
        city = City(50)
        self.assertEqual(city.x, 50)
        self.assertEqual(city.y, CITY_Y)
        self.assertTrue(city.is_alive)


class TestMeteor(unittest.TestCase):
    def test_meteor_creation(self):
        meteor = Meteor(10, 20, 3)
        self.assertEqual(meteor.x, 10)
        self.assertEqual(meteor.y, 20)
        self.assertEqual(meteor.speed, 3)
        self.assertTrue(meteor.is_alive)


    @patch('missile_command.Meteor._check_base_collision')
    @patch('missile_command.Explosion')
    def test_meteor_update_base_collision(self, MockExplosion, MockCheckBaseCollision):
        bases = [Base(100)]
        cities = []
        explosions = []
        score = 100
        meteor = Meteor(100, BASE_Y - 4, 1)
        MockCheckBaseCollision.return_value = (score - 10, explosions)
        score, explosions = meteor.update(bases, cities, explosions, score)
        self.assertEqual(MockCheckBaseCollision.call_count, 1)
        self.assertEqual(score, 90)

    @patch('missile_command.Meteor._check_city_collision')
    @patch('missile_command.Explosion')
    def test_meteor_update_city_collision(self, MockExplosion, MockCheckCityCollision):
        bases = []
        cities = [City(100)]
        explosions = []
        score = 100
        meteor = Meteor(100, CITY_Y-4, 1)
        MockCheckCityCollision.return_value = (score - 5, explosions)
        score, explosions = meteor.update(bases, cities, explosions, score)
        self.assertEqual(MockCheckCityCollision.call_count, 1)
        self.assertEqual(score, 95)

    @patch('missile_command.Explosion')
    def test_meteor_check_base_collision(self, MockExplosion):
        bases = [Base(100)]
        explosions = []
        score = 100
        meteor = Meteor(100, BASE_Y - 4, 1)
        score, explosions = meteor._check_base_collision(bases, explosions, score)
        self.assertFalse(meteor.is_alive)
        self.assertFalse(bases[0].is_alive)
        self.assertEqual(len(explosions), 1)
        self.assertEqual(score, 90)

    @patch('missile_command.Explosion')
    def test_meteor_check_city_collision(self, MockExplosion):
        bases = []
        cities = [City(100)]
        explosions = []
        score = 100
        meteor = Meteor(100, CITY_Y-4, 1)
        score, explosions = meteor._check_city_collision(cities, explosions, score)
        self.assertFalse(meteor.is_alive)
        self.assertFalse(cities[0].is_alive)
        self.assertEqual(len(explosions), 1)
        self.assertEqual(score, 95)

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

class TestMissile(unittest.TestCase):
    def test_missile_creation(self):
        base = Base(100)
        missile = Missile(base, 200, 100)
        self.assertEqual(missile.start_x, 100)
        self.assertEqual(missile.start_y, BASE_Y)
        self.assertEqual(missile.target_x, 200)
        self.assertEqual(missile.target_y, 100)
        self.assertEqual(missile.speed, MISSILE_SPEED) # Use constant from constants.py
        self.assertTrue(missile.is_alive)
        self.assertIsNone(missile.explosion)

    @patch('missile_command.Explosion')
    def test_missile_update_reach_target(self, MockExplosion):
        base = Base(100)
        missile = Missile(base, 105, BASE_Y)
        missile.update()
        self.assertFalse(missile.is_alive)
        self.assertIsNotNone(missile.explosion)

class TestExplosion(unittest.TestCase):
    def test_explosion_creation(self):
        explosion = Explosion(10, 20)
        self.assertEqual(explosion.x, 10)
        self.assertEqual(explosion.y, 20)
        self.assertEqual(explosion.radius, 1)
        self.assertEqual(explosion.max_radius, EXPLOSION_RADIUS_MAX)
        self.assertEqual(explosion.duration, EXPLOSION_DURATION)
        self.assertTrue(explosion.is_alive)

    def test_explosion_update(self):
        explosion = Explosion(10,20)
        explosion.update()
        self.assertEqual(explosion.radius, 1.5)
        self.assertEqual(explosion.duration, 14)

        # Simulate until explosion is done
        for _ in range(EXPLOSION_DURATION):
            explosion.update()
        self.assertFalse(explosion.is_alive)

# Integration test - needs pyxel to be installed
class TestApp(unittest.TestCase):
    def test_app_reset(self):
        app = App()  # Initialize with pyxel
        self.assertEqual(len(app.bases), 3)
        self.assertEqual(len(app.cities), 6)
        app.reset()
        self.assertEqual(len(app.bases), 3)
        self.assertEqual(len(app.cities), 6)
        self.assertEqual(app.score, 0)
        self.assertFalse(app.game_over)

if __name__ == "__main__":
    unittest.main()
