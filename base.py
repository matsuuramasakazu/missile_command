import pyxel
from constants import *

class Base:
    def __init__(self, x):
        if not isinstance(x, (int, float)):
            raise TypeError("x must be a numeric value")
        self.x = x
        self.y = BASE_Y
        self.is_alive = True

    def draw(self):
        if self.is_alive:
            pyxel.blt(self.x - BASE_IMG_WIDTH // 2, self.y, 0, BASE_IMG_X, BASE_IMG_Y, BASE_IMG_WIDTH, BASE_IMG_HEIGHT)
