import unittest
# This is a test comment
import math
from meteor import Meteor
from constants import *

class TestMeteor(unittest.TestCase):
    def test_meteor_creation(self):
        meteor = Meteor(10, 20, 3)
        self.assertEqual(meteor.x, 10)
        self.assertEqual(meteor.y, 20)
        self.assertEqual(meteor.speed, 3)
        self.assertTrue(meteor.is_alive)

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

    def test_meteor_update_reach_grand(self):
        meteor = Meteor(105, GRAND_Y-2, 1)
        new_explosion = meteor.update()
        self.assertFalse(meteor.is_alive)
        self.assertIsNotNone(new_explosion)