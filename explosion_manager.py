# import pyxel # Removed
from explosion import Explosion # Assuming Explosion is in explosion.py
from constants import * # If ExplosionManager uses any constants

class ExplosionManager:
    def __init__(self, platform): # Added platform argument
        self.explosions = []
        self.platform = platform # Store platform

    def add_explosion(self, x, y):
        # Explosion constructor now needs a platform
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
            explosion.update() # Explosion.update() will use its own platform if needed
            if explosion.is_alive:
                updated_explosions.append(explosion)
        self.explosions[:] = updated_explosions

    def draw(self):
        for explosion in self.explosions:
            explosion.draw() # Explosion.draw() will use its own platform

    def get_explosions(self):
        return self.explosions
