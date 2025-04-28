import pyxel
import math
import random
from constants import *
from meteor import Meteor
from explosion import Explosion

class MeteorManager:
    def __init__(self, explosions):
        self.explosions = explosions
        self.meteors = []

    def update(self):
        if pyxel.frame_count % METEOR_SPAWN_INTERVAL == 0:
            for _ in range(METEOR_SPAWN_COUNT):
                angle = random.uniform(-METEOR_ANGLE_RANGE, METEOR_ANGLE_RANGE)
                meteor_x = random.randint(0, SCREEN_WIDTH)
                meteor_speed = random.uniform(METEOR_SPEED_MIN, METEOR_SPEED_MAX) / 2
                meteor = Meteor(meteor_x, METEOR_INITIAL_Y, meteor_speed)
                meteor.angle = angle

                if not (0 - METEOR_OFFSCREEN_OFFSET < meteor.x + SCREEN_HEIGHT * math.cos(math.radians(90 + angle)) < SCREEN_WIDTH + METEOR_OFFSCREEN_OFFSET):
                    continue

                self.meteors.append(meteor)

        updated_meteors = []
        for meteor in self.meteors:
            meteor.update(self.explosions)
            if meteor.is_alive:
                updated_meteors.append(meteor)
        self.meteors[:] = updated_meteors

        updated_explosions = []
        for explosion in self.explosions:
            explosion.update()
            if explosion.is_alive:
                updated_explosions.append(explosion)
        self.explosions[:] = updated_explosions

    def draw(self):
        for meteor in self.meteors:
            meteor.draw()
        for explosion in self.explosions:
            explosion.draw()
