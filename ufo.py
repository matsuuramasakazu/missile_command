import pyxel
import math
from constants import *
from game_object import GameObject

class UFO(GameObject):
    def __init__(self, x, y, zigzag=False):
        super().__init__()
        self.x = x
        self.y = y
        self.zigzag = zigzag
        self.zigzag_phase = 0

    def update(self):
        self.x -= UFO_SPEED  # 左に移動
        if self.zigzag:
            self.zigzag_phase += 0.2
            self.y += 2 * math.sin(self.zigzag_phase)
        if self.x < -UFO_WIDTH:
            self.is_alive = False

    def draw(self):
        if self.is_alive:
            pyxel.blt(self.x, self.y, 0, UFO_IMG_X, UFO_IMG_Y, UFO_WIDTH, UFO_HEIGHT)
