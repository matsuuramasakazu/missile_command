import pyxel
from constants import *
from game_object import GameObject

class City(GameObject):
    def __init__(self, x):
        super().__init__()
        self.x = x
        self.y = CITY_Y

    def draw(self):
        if self.is_alive:
            pyxel.blt(self.x - CITY_IMG_WIDTH // 2, self.y, 0, CITY_IMG_X, CITY_IMG_Y, CITY_IMG_WIDTH, CITY_IMG_HEIGHT)
