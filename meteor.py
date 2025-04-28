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
        self.angle = 0

    def update(self, explosions):
        self._move()
        if self.y >= GRAND_Y:
            self.is_alive = False
            explosions.append(Explosion(self.x, GRAND_Y))

    def _move(self):
        self.y += self.speed * math.sin(math.radians(90 + self.angle))
        self.x += self.speed * math.cos(math.radians(90 + self.angle))

    def draw(self):
        if self.is_alive:
            pyxel.circ(self.x, self.y, METEOR_RADIUS, METEOR_COLOR)
