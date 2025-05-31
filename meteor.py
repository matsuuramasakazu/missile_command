import pyxel
import math
from constants import *
from explosion import Explosion
from game_object import GameObject

class Meteor(GameObject):
    def __init__(self, x, y, speed):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = 0 # Angle for movement direction

    def update(self): # Removed explosions from parameters
        if not self.is_alive:
            return None

        self._move()

        if self.y >= GRAND_Y - METEOR_RADIUS: # Adjusted to use METEOR_RADIUS for ground collision
            self.is_alive = False
            # Create explosion at the meteor's center just as it hits the ground
            return Explosion(self.x, self.y) # Return new Explosion object

        # Check if meteor is off-screen (optional, could be handled by a manager or if it expires)
        if self.x < -METEOR_OFFSCREEN_OFFSET or self.x > SCREEN_WIDTH + METEOR_OFFSCREEN_OFFSET or self.y > SCREEN_HEIGHT + METEOR_OFFSCREEN_OFFSET:
           self.is_alive = False
           return None # Or an explosion if off-screen meteors should explode

        return None # No explosion occurred in this update step

    def _move(self):
        # Assuming angle is relative to vertical (0 degrees is straight down)
        # Or if angle is like atan2, then direct use is fine.
        # The existing code uses 90 + angle, implying angle might be relative to horizontal.
        # Let's stick to the existing movement logic for now.
        self.y += self.speed * math.sin(math.radians(90 + self.angle))
        self.x += self.speed * math.cos(math.radians(90 + self.angle))

    def draw(self):
        if self.is_alive:
            pyxel.circ(self.x, self.y, METEOR_RADIUS, METEOR_COLOR)
