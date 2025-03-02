import pyxel
from constants import *

class City:
    def __init__(self, x):
        self.x = x
        self.y = CITY_Y
        self.is_alive = True

    def draw(self):
        if self.is_alive:
            pyxel.blt(self.x - CITY_IMG_WIDTH // 2, self.y, 0, CITY_IMG_X, CITY_IMG_Y, CITY_IMG_WIDTH, CITY_IMG_HEIGHT)
