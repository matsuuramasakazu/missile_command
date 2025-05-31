# import pyxel # Removed
from explosion import Explosion
from constants import *

class ExplosionManager:
    def __init__(self, platform):
        self.explosions = []
        self.platform = platform

    def add_explosion(self, x, y):
        new_explosion = Explosion(x, y, self.platform)
        self.explosions.append(new_explosion)

    def add_explosion_object(self, explosion_obj):
        if isinstance(explosion_obj, Explosion):
            self.explosions.append(explosion_obj)
        else:
            print("Error: Attempted to add a non-Explosion object to ExplosionManager")

    def update(self):
        updated_explosions = []
        for explosion in self.explosions:
            explosion.update()
            if explosion.is_alive:
                updated_explosions.append(explosion)
        self.explosions[:] = updated_explosions

    def draw(self):
        for explosion in self.explosions:
            explosion.draw()

    def get_explosions(self):
        return self.explosions
