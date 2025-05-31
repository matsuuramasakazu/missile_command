from constants import *
from game_object import GameObject
from game_platform_interface import IGamePlatform

class Base(GameObject):
    def __init__(self, x, platform: IGamePlatform):
        super().__init__()
        if not isinstance(x, (int, float)):
            raise TypeError("x must be a numeric value")
        self.x = x
        self.y = BASE_Y
        self.platform = platform # Store platform

    def draw(self):
        if self.is_alive:
            # Use platform.draw_image
            # Assuming image bank 0 for game assets loaded via pyxel.load()
            # The platform's draw_image is: img_idx, x, y, u, v, width, height, color_key=None
            # pyxel.blt was: self.x - BASE_IMG_WIDTH // 2, self.y, 0 (img_bank), BASE_IMG_X, BASE_IMG_Y, BASE_IMG_WIDTH, BASE_IMG_HEIGHT
            # So, img_idx should be 0.
            self.platform.draw_image(img_idx=0,
                                     x=self.x - BASE_IMG_WIDTH // 2,
                                     y=self.y,
                                     u=BASE_IMG_X,
                                     v=BASE_IMG_Y,
                                     width=BASE_IMG_WIDTH,
                                     height=BASE_IMG_HEIGHT)
