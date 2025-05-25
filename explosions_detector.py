import math
from constants import *
from explosion import Explosion

class ExplosionsDetector:
    def __init__(self, explosions, targets):
        self.explosions = explosions
        self.targets = targets

    def check_collisions(self):
        collided_targets = []
        for explosion in self.explosions:
            if not explosion.is_alive:
                continue
            for target in self.targets:
                if not target.is_alive: # Still useful to not check already dead targets
                    continue
                distance = math.hypot(explosion.x - target.x, explosion.y - target.y)
                if distance < explosion.radius + COLLISION_DISTANCE:
                    # target.is_alive = False # This line is now removed
                    collided_targets.append(target) # Add target to list of collided, but don't change its state
        return collided_targets
