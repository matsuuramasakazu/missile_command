import math
from constants import *
from explosion import Explosion
from game_object import GameObject
from game_platform_interface import IGamePlatform

class Missile(GameObject):
    def __init__(self, start_base, target_x, target_y, platform: IGamePlatform):
        super().__init__()
        self.start_x = start_base.x
        self.start_y = start_base.y
        self.x = self.start_x
        self.y = self.start_y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = MISSILE_SPEED
        self.angle = math.atan2(target_y - self.start_y, target_x - self.start_x)
        self.platform = platform

    def update(self):
        if not self.is_alive:
            return None

        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance <= self.speed: # Target reached
            self.x = self.target_x
            self.y = self.target_y
            self.is_alive = False
            # Create explosion, pass platform
            return Explosion(self.x, self.y, self.platform)
        else:
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)

        return None

    def draw(self):
        if self.is_alive:
            self.platform.draw_line(self.start_x, self.start_y, self.x, self.y, MISSILE_COLOR)
            self.platform.draw_circle(self.x, self.y, MISSILE_RADIUS, MISSILE_COLOR)
