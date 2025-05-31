import math # pyxel import removed
from constants import *
from explosion import Explosion
from game_object import GameObject
from game_platform_interface import IGamePlatform # Import IGamePlatform

class Meteor(GameObject):
    def __init__(self, x, y, speed, platform: IGamePlatform): # Add platform
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = 0 # Angle for movement direction
        self.platform = platform # Store platform

    def update(self):
        if not self.is_alive:
            return None

        self._move()

        if self.y >= GRAND_Y - METEOR_RADIUS:
            self.is_alive = False
            # Create explosion, pass platform
            return Explosion(self.x, self.y, self.platform)

        # Check if meteor is off-screen
        # Assuming SCREEN_WIDTH and SCREEN_HEIGHT are from constants.py and represent the fixed game dimensions
        if self.x < -METEOR_OFFSCREEN_OFFSET or self.x > SCREEN_WIDTH + METEOR_OFFSCREEN_OFFSET or self.y > SCREEN_HEIGHT + METEOR_OFFSCREEN_OFFSET:
           self.is_alive = False
           return None

        return None

    def _move(self):
        self.y += self.speed * math.sin(math.radians(90 + self.angle))
        self.x += self.speed * math.cos(math.radians(90 + self.angle))

    def draw(self):
        if self.is_alive:
            # Use platform.draw_circle
            self.platform.draw_circle(self.x, self.y, METEOR_RADIUS, METEOR_COLOR)
