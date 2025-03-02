import pyxel
from constants import *

class UFO:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_alive = True

    def update(self):
        self.x -= UFO_SPEED  # Assuming UFO moves from right to left
        if self.x < -UFO_WIDTH:
            self.is_alive = False

    def draw(self):
        if self.is_alive:
            pyxel.blt(self.x, self.y, 0, UFO_IMG_X, UFO_IMG_Y, UFO_WIDTH, UFO_HEIGHT)
