import unittest
from explosions_detector import ExplosionsDetector
from explosion import Explosion
from meteor import Meteor
from ufo import UFO
from missile_manager import MissileManager
from meteor_manager import MeteorManager
from constants import *

class TestExplosionsDetector(unittest.TestCase):
    def setUp(self):
        self.meteor_manager = MeteorManager([])
        self.missile_manager = MissileManager([], [])
        self.detector = ExplosionsDetector(
            self.missile_manager.explosions, self.meteor_manager.meteors
        )

    def test_check_collisions_true(self):
        explosion = Explosion(100, 100)
        explosion.radius = 10
        meteor = Meteor(105, 105, 5)
        self.missile_manager.explosions.append(explosion)
        self.meteor_manager.meteors.append(meteor)
        is_collision = self.detector.check_collisions()
        self.assertTrue(is_collision)
        self.assertFalse(meteor.is_alive)

    def test_check_collisions_false(self):
        explosion = Explosion(100, 100)
        explosion.radius = 1
        meteor = Meteor(110, 110, 5)

        self.missile_manager.explosions.append(explosion)
        self.meteor_manager.meteors.append(meteor)
        is_collision = self.detector.check_collisions()
        self.assertFalse(is_collision)

    def test_check_collisions_ufo(self):
        explosion = Explosion(100, 100)
        explosion.radius = 10
        ufo = UFO(105, 105)
        self.missile_manager.explosions.append(explosion)
        self.detector.targets = [ufo]  # Check against UFOs
        is_collision = self.detector.check_collisions()
        self.assertTrue(is_collision)
        self.assertFalse(ufo.is_alive)

    def test_multiple_targets_hit(self):
        explosion = Explosion(100, 100)
        explosion.radius = 15
        meteor1 = Meteor(105, 105, 1)
        meteor2 = Meteor(95, 95, 1)
        self.missile_manager.explosions.append(explosion)
        self.detector.targets = [meteor1, meteor2]
        is_collision = self.detector.check_collisions()
        self.assertTrue(is_collision)
        self.assertFalse(meteor1.is_alive)
        self.assertFalse(meteor2.is_alive)
