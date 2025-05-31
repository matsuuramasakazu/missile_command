from constants import *
from game_platform_interface import IGamePlatform

class Explosion:
    def __init__(self, x, y, platform: IGamePlatform):
        self.x = x
        self.y = y
        self.radius = EXPLOSION_INITIAL_RADIUS
        self.max_radius = EXPLOSION_RADIUS_MAX
        self.duration = EXPLOSION_DURATION
        self.is_alive = True
        self.platform = platform # Store platform

    def update(self):
        if not self.is_alive:
            return

        if self.radius >= self.max_radius or self.duration <= 0:
            self.is_alive = False
        else:
            self.radius += EXPLOSION_RADIUS_INCREMENT
            self.duration -= EXPLOSION_DURATION_DECREMENT

    def draw(self):
        if self.is_alive:
            self.platform.draw_circle(self.x, self.y, self.radius, EXPLOSION_COLOR)
