from constants import * # pyxel import removed
from game_object import GameObject
from game_platform_interface import IGamePlatform # Import IGamePlatform

class City(GameObject):
    def __init__(self, x, platform: IGamePlatform): # Add platform
        super().__init__()
        self.x = x
        self.y = CITY_Y
        self.platform = platform # Store platform

    def draw(self):
        if self.is_alive:
            # Use platform.draw_image
            # Assuming image bank 0 for game assets.
            # platform.draw_image parameters: img_idx, x, y, u, v, width, height, color_key=None
            # pyxel.blt was: self.x - CITY_IMG_WIDTH // 2, self.y, 0 (img_bank), CITY_IMG_X, CITY_IMG_Y, CITY_IMG_WIDTH, CITY_IMG_HEIGHT
            self.platform.draw_image(img_idx=0,
                                     x=self.x - CITY_IMG_WIDTH // 2,
                                     y=self.y,
                                     u=CITY_IMG_X,
                                     v=CITY_IMG_Y,
                                     width=CITY_IMG_WIDTH,
                                     height=CITY_IMG_HEIGHT)
