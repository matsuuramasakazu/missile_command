import math # pyxel import removed
from constants import *
from game_object import GameObject
from game_platform_interface import IGamePlatform # Import IGamePlatform

class UFO(GameObject):
    def __init__(self, x, y, platform: IGamePlatform, zigzag=False): # Add platform
        super().__init__()
        self.x = x
        self.y = y
        self.zigzag = zigzag
        self.zigzag_phase = 0
        self.platform = platform # Store platform

    def update(self):
        self.x -= UFO_SPEED  # 左に移動
        if self.zigzag:
            self.zigzag_phase += 0.2 # Consider making this rate a constant
            self.y += UFO_ZIGZAG_AMPLITUDE * math.sin(self.zigzag_phase) # Use constant for amplitude
        if self.x < -UFO_WIDTH: # Assuming UFO_WIDTH is from constants
            self.is_alive = False

    def draw(self):
        if self.is_alive:
            # Use platform.draw_image
            # Assuming image bank 0.
            # platform.draw_image parameters: img_idx, x, y, u, v, width, height, color_key=None
            # pyxel.blt was: self.x, self.y, 0 (img_bank), UFO_IMG_X, UFO_IMG_Y, UFO_WIDTH, UFO_HEIGHT
            self.platform.draw_image(img_idx=0,
                                     x=self.x,
                                     y=self.y,
                                     u=UFO_IMG_X,
                                     v=UFO_IMG_Y,
                                     width=UFO_WIDTH,
                                     height=UFO_HEIGHT)
