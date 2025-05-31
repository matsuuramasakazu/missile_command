import math
import random
from constants import *
from meteor import Meteor
from game_platform_interface import IGamePlatform

class MeteorManager:
    def __init__(self, explosion_manager, platform: IGamePlatform):
        self.explosion_manager = explosion_manager
        self.platform = platform
        self.meteors = []

    def update(self):
        if self.platform.get_frame_count() % METEOR_SPAWN_INTERVAL == 0:
            for _ in range(METEOR_SPAWN_COUNT):
                angle = random.uniform(-METEOR_ANGLE_RANGE, METEOR_ANGLE_RANGE)
                meteor_x = random.randint(0, SCREEN_WIDTH) # Assuming SCREEN_WIDTH is a constant
                meteor_speed = random.uniform(METEOR_SPEED_MIN, METEOR_SPEED_MAX) / 2
                meteor = Meteor(meteor_x, METEOR_INITIAL_Y, meteor_speed, self.platform)
                meteor.angle = angle

                # Assuming SCREEN_HEIGHT is a constant for trajectory calculation logic
                if not (0 - METEOR_OFFSCREEN_OFFSET < meteor.x + SCREEN_HEIGHT * math.cos(math.radians(90 + angle)) < SCREEN_WIDTH + METEOR_OFFSCREEN_OFFSET):
                    continue

                self.meteors.append(meteor)

        updated_meteors = []
        for meteor in self.meteors:
            # If meteor.update() itself can cause an explosion (e.g. expiration), it should return an Explosion object
            new_explosion = meteor.update() # Anticipate meteor.update() returning an Explosion or None
            if new_explosion:
                self.explosion_manager.add_explosion_object(new_explosion)
            if meteor.is_alive:
                updated_meteors.append(meteor)
        self.meteors[:] = updated_meteors

    def draw(self):
        for meteor in self.meteors:
            meteor.draw()
