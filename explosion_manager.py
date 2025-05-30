import pyxel
from explosion import Explosion # Assuming Explosion is in explosion.py
from constants import * # If ExplosionManager uses any constants

class ExplosionManager:
    def __init__(self):
        self.explosions = []

    def add_explosion(self, x, y):
        # This method might need to change if Explosion objects are created elsewhere
        # and passed in, rather than coordinates.
        # For now, let's assume it receives coordinates to create an explosion.
        new_explosion = Explosion(x, y)
        self.explosions.append(new_explosion)

    def add_explosion_object(self, explosion_obj):
        # Method to add an already created Explosion object
        if isinstance(explosion_obj, Explosion):
            self.explosions.append(explosion_obj)
        else:
            # Handle error or log if needed
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
        # Method to provide access to the explosions list, e.g., for ExplosionsDetector
        return self.explosions
