import unittest
from explosions_detector import ExplosionsDetector
from explosion import Explosion
from meteor import Meteor
from ufo import UFO
from constants import *

class TestExplosionsDetector(unittest.TestCase):
    def setUp(self):
        # Initialize with empty lists for explosions and targets,
        # as these will be set per-test.
        self.detector = ExplosionsDetector([], [])

    def test_check_collisions_true(self): # Renamed for clarity
        trigger_explosion = Explosion(100, 100)
        trigger_explosion.radius = 10
        meteor = Meteor(105, 105, 5)
        meteor.is_alive = True 

        self.detector.explosions = [trigger_explosion] 
        self.detector.targets = [meteor]

        collided_targets, new_explosions = self.detector.check_collisions() # Unpack tuple

        # Verify collided targets
        self.assertEqual(len(collided_targets), 1)
        self.assertIn(meteor, collided_targets)
        
        # Verify target.is_alive was NOT changed by check_collisions
        self.assertTrue(meteor.is_alive, "check_collisions should not change target.is_alive")

        # Verify new explosions
        self.assertEqual(len(new_explosions), 1)
        self.assertIsInstance(new_explosions[0], Explosion)
        self.assertEqual(new_explosions[0].x, meteor.x)
        self.assertEqual(new_explosions[0].y, meteor.y)

    def test_check_collisions_false(self): # Renamed for clarity
        trigger_explosion = Explosion(100, 100)
        trigger_explosion.radius = 1
        meteor = Meteor(110, 110, 5)
        meteor.is_alive = True

        self.detector.explosions = [trigger_explosion]
        self.detector.targets = [meteor]

        collided_targets, new_explosions = self.detector.check_collisions() # Unpack tuple

        self.assertEqual(len(collided_targets), 0)
        self.assertEqual(len(new_explosions), 0)
        self.assertTrue(meteor.is_alive) 

    def test_check_collisions_ufo(self): # Renamed for clarity
        trigger_explosion = Explosion(100, 100)
        trigger_explosion.radius = 10
        ufo = UFO(105, 105)
        ufo.is_alive = True 

        self.detector.explosions = [trigger_explosion]
        self.detector.targets = [ufo]

        collided_targets, new_explosions = self.detector.check_collisions() # Unpack tuple

        self.assertEqual(len(collided_targets), 1)
        self.assertIn(ufo, collided_targets)
        self.assertTrue(ufo.is_alive, "check_collisions should not change ufo.is_alive") 
        self.assertEqual(len(new_explosions), 1)
        self.assertIsInstance(new_explosions[0], Explosion)
        self.assertEqual(new_explosions[0].x, ufo.x)
        self.assertEqual(new_explosions[0].y, ufo.y)

    def test_multiple_targets_hit(self): # Renamed for clarity
        trigger_explosion = Explosion(100, 100)
        trigger_explosion.radius = 15
        meteor1 = Meteor(105, 105, 1)
        meteor1.is_alive = True
        meteor2 = Meteor(95, 95, 1)
        meteor2.is_alive = True
        meteor_miss = Meteor(130, 130, 1)
        meteor_miss.is_alive = True

        self.detector.explosions = [trigger_explosion]
        self.detector.targets = [meteor1, meteor2, meteor_miss] 
        
        collided_targets, new_explosions = self.detector.check_collisions() # Unpack tuple
        
        self.assertEqual(len(collided_targets), 2)
        self.assertIn(meteor1, collided_targets)
        self.assertIn(meteor2, collided_targets)
        self.assertNotIn(meteor_miss, collided_targets)

        self.assertTrue(meteor1.is_alive, "check_collisions should not change meteor1.is_alive")
        self.assertTrue(meteor2.is_alive, "check_collisions should not change meteor2.is_alive")
        self.assertTrue(meteor_miss.is_alive) 
        
        self.assertEqual(len(new_explosions), 2)
        expected_coords = {(meteor1.x, meteor1.y), (meteor2.x, meteor2.y)}
        actual_coords = {(exp.x, exp.y) for exp in new_explosions}
        self.assertEqual(actual_coords, expected_coords)

    def test_target_already_not_alive(self): # New test
        trigger_explosion = Explosion(100, 100)
        trigger_explosion.radius = 10
        meteor = Meteor(105, 105, 5)
        meteor.is_alive = False 

        self.detector.explosions = [trigger_explosion]
        self.detector.targets = [meteor]

        collided_targets, new_explosions = self.detector.check_collisions()
        self.assertEqual(len(collided_targets), 0)
        self.assertEqual(len(new_explosions), 0)
        self.assertFalse(meteor.is_alive)

    def test_explosion_not_alive(self): # New test
        trigger_explosion = Explosion(100, 100)
        trigger_explosion.radius = 10
        trigger_explosion.is_alive = False 
        meteor = Meteor(105, 105, 5)
        meteor.is_alive = True

        self.detector.explosions = [trigger_explosion]
        self.detector.targets = [meteor]

        collided_targets, new_explosions = self.detector.check_collisions()
        self.assertEqual(len(collided_targets), 0)
        self.assertEqual(len(new_explosions), 0)
        self.assertTrue(meteor.is_alive)
