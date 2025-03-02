import pyxel
import math
from constants import *
from explosion import Explosion

class ExplosionsDetector:
    def __init__(self, explosions, targets):
        self.explosions = explosions
        self.targets = targets

    def check_collisions(self):
        for explosion in self.explosions:
            if not explosion.is_alive:
                continue
            for target in self.targets:
                if not target.is_alive:
                    continue
                distance = math.sqrt((explosion.x - target.x)**2 + (explosion.y - target.y)**2)
                if distance < explosion.radius + COLLISION_DISTANCE:
                    target.is_alive = False
                    # Add explosion effect when UFO is hit
                    self.explosions.append(Explosion(target.x, target.y))
                    return True
        return False
