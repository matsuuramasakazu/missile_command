import unittest
from explosions_detector import ExplosionsDetector
from explosion import Explosion
from meteor import Meteor
from ufo import UFO
from constants import *
from test_game_platform import TestGamePlatform # Added

class TestExplosionsDetector(unittest.TestCase):
    def setUp(self):
        self.platform = TestGamePlatform() # Added
        # Initialize with empty lists for explosions and targets,
        # as these will be set per-test.
        self.detector = ExplosionsDetector([], [])

    def test_check_collisions_true(self):
        trigger_explosion = Explosion(100, 100, self.platform)
        trigger_explosion.radius = 10
        meteor = Meteor(105, 105, 5, self.platform)
        meteor.is_alive = True 

        self.detector.explosions = [trigger_explosion] 
        self.detector.targets = [meteor]

        collided_targets = self.detector.check_collisions()
        self.assertEqual(len(collided_targets), 1)
        self.assertIn(meteor, collided_targets)
        self.assertTrue(meteor.is_alive, "check_collisions should not change target.is_alive")

    def test_check_collisions_false(self):
        trigger_explosion = Explosion(100, 100, self.platform)
        trigger_explosion.radius = 1
        meteor = Meteor(110, 110, 5, self.platform)
        meteor.is_alive = True

        self.detector.explosions = [trigger_explosion]
        self.detector.targets = [meteor]

        collided_targets = self.detector.check_collisions()
        self.assertEqual(len(collided_targets), 0)
        self.assertTrue(meteor.is_alive) 

    def test_check_collisions_ufo(self):
        trigger_explosion = Explosion(100, 100, self.platform)
        trigger_explosion.radius = 10
        ufo = UFO(105, 105, self.platform)
        ufo.is_alive = True 

        self.detector.explosions = [trigger_explosion]
        self.detector.targets = [ufo]

        collided_targets = self.detector.check_collisions()
        self.assertEqual(len(collided_targets), 1)
        self.assertIn(ufo, collided_targets)
        self.assertTrue(ufo.is_alive, "check_collisions should not change ufo.is_alive") 

    def test_multiple_targets_hit(self):
        trigger_explosion = Explosion(100, 100, self.platform)
        trigger_explosion.radius = 15
        meteor1 = Meteor(105, 105, 1, self.platform)
        meteor1.is_alive = True
        meteor2 = Meteor(95, 95, 1, self.platform)
        meteor2.is_alive = True
        meteor_miss = Meteor(130, 130, 1, self.platform)
        meteor_miss.is_alive = True

        self.detector.explosions = [trigger_explosion]
        self.detector.targets = [meteor1, meteor2, meteor_miss] 
        
        collided_targets = self.detector.check_collisions()
        self.assertEqual(len(collided_targets), 2)
        self.assertIn(meteor1, collided_targets)
        self.assertIn(meteor2, collided_targets)
        self.assertNotIn(meteor_miss, collided_targets)
        self.assertTrue(meteor1.is_alive, "check_collisions should not change meteor1.is_alive")
        self.assertTrue(meteor2.is_alive, "check_collisions should not change meteor2.is_alive")
        self.assertTrue(meteor_miss.is_alive) 
        
    def test_target_already_not_alive(self):
        trigger_explosion = Explosion(100, 100, self.platform)
        trigger_explosion.radius = 10
        meteor = Meteor(105, 105, 5, self.platform)
        meteor.is_alive = False 

        self.detector.explosions = [trigger_explosion]
        self.detector.targets = [meteor]

        collided_targets = self.detector.check_collisions()
        self.assertEqual(len(collided_targets), 0)
        self.assertFalse(meteor.is_alive)

    def test_explosion_not_alive(self):
        trigger_explosion = Explosion(100, 100, self.platform)
        trigger_explosion.radius = 10
        trigger_explosion.is_alive = False 
        meteor = Meteor(105, 105, 5, self.platform)
        meteor.is_alive = True

        self.detector.explosions = [trigger_explosion]
        self.detector.targets = [meteor]

        collided_targets = self.detector.check_collisions()
        self.assertEqual(len(collided_targets), 0)
        self.assertTrue(meteor.is_alive)
