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

    @patch('missile_command.Game.find_nearest_base')
    @patch('pyxel.btnp')
    @patch('pyxel.frame_count')
    def test_update_missile_launch(self, mock_find_nearest_base, mock_btnp, mock_frame_count):
        mock_base = Base(100)
        mock_find_nearest_base.return_value = mock_base
        mock_btnp.return_value = True
        mock_frame_count.return_value = 0
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

class TestMeteorManager(unittest.TestCase):
    def setUp(self):
        if TestGame._is_pyxel_initialized == False:
            pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Missile Command")
            TestGame._is_pyxel_initialized = True

        self.bases = [Base(x) for x in BASE_X_POSITIONS]
        self.cities = [City(x) for x in CITY_X_POSITIONS]
        self.manager = MeteorManager(self.bases, self.cities)

    @patch('pyxel.frame_count', METEOR_SPAWN_INTERVAL)
    @patch('missile_command.random.randint')
    @patch('missile_command.random.uniform')
    def test_update_meteor_spawn(self, mock_uniform, mock_randint):
        mock_uniform.return_value = 0  # Any value within -METEOR_ANGLE_RANGE to METEOR_ANGLE_RANGE
        mock_randint.return_value = 100 # Any value between 0 and SCREEN_WIDTH

        self.manager.update(0)
        self.assertEqual(len(self.manager.meteors), METEOR_SPAWN_COUNT)

    def test_check_ground_hit(self):
        meteor_x = self.bases[0].x
        self.manager.check_ground_hit(meteor_x)
        self.assertFalse(self.bases[0].is_alive)

class TestMissileManager(unittest.TestCase):
    def setUp(self):
        self.bases = [Base(x) for x in BASE_X_POSITIONS]
        self.manager = MissileManager(self.bases)

    @patch('missile_command.Missile')
    def test_update_missile_launch(self, MockMissile):
        # Simulate a mouse click
        with patch('pyxel.btnp', return_value=True):
            pyxel.mouse_x = 100
            pyxel.mouse_y = 200
            self.manager.update()
            self.assertEqual(MockMissile.call_count, 1)

    def test_find_nearest_base(self):
        nearest_base = self.manager.find_nearest_base(BASE_X_POSITIONS[0] + 10)
        self.assertEqual(nearest_base.x, BASE_X_POSITIONS[0])

    def test_find_nearest_base_no_alive_bases(self):
        for base in self.bases:
            base.is_alive = False
        nearest_base = self.manager.find_nearest_base(BASE_X_POSITIONS[0] + 10)
        self.assertIsNone(nearest_base)

class TestCollisionDetector(unittest.TestCase):
    def setUp(self):
        self.meteor_manager = MeteorManager([], [])
        self.missile_manager = MissileManager([])
        self.detector = CollisionDetector(self.meteor_manager, self.missile_manager)

    def test_check_collisions_true(self):
        explosion = Explosion(100, 100)
        explosion.radius = 10
        meteor = Meteor(105, 105, 5)
        self.missile_manager.explosions.append(explosion)
        self.meteor_manager.meteors.append(meteor)
        is_collision, _ = self.detector.check_collisions()
        self.assertTrue(is_collision)

    def test_check_collisions_false(self):
        explosion = Explosion(100, 100)
        explosion.radius = 1
        meteor = Meteor(110, 110, 5)

        self.missile_manager.explosions.append(explosion)
        self.meteor_manager.meteors.append(meteor)
        is_collision, _ = self.detector.check_collisions()
        self.assertFalse(is_collision)

if __name__ == "__main__":
    unittest.main()
