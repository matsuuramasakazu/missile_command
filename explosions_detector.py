import math
from constants import *
from explosion import Explosion

class ExplosionsDetector:
    def __init__(self, explosions, targets):
        self.explosions = explosions
        self.targets = targets

    def check_collisions(self):
        collision_detected = False
        new_explosions = []
        for explosion in self.explosions:
            if not explosion.is_alive:
                continue
            for target in self.targets:
                if not target.is_alive:
                    continue
                distance = math.hypot(explosion.x - target.x, explosion.y - target.y)
                if distance < explosion.radius + COLLISION_DISTANCE:
                    target.is_alive = False
                    new_explosions.append(Explosion(target.x, target.y))
                    collision_detected = True
        self.explosions.extend(new_explosions)
        return collision_detected
