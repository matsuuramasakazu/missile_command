import pyxel
from constants import *
from missile import Missile

class MissileManager:
    def __init__(self, bases, explosion_manager):
        self.bases = bases
        self.explosion_manager = explosion_manager
        self.missiles = []

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if any(base.is_alive for base in self.bases):
                nearest_base = self.find_nearest_base(pyxel.mouse_x)
                if nearest_base:
                    self.missiles.append(Missile(nearest_base, pyxel.mouse_x, pyxel.mouse_y))

        updated_missiles = []
        for missile in self.missiles:
            new_explosion = missile.update()
            if new_explosion:
                self.explosion_manager.add_explosion_object(new_explosion)
            if missile.is_alive:
                updated_missiles.append(missile)
        self.missiles[:] = updated_missiles

    def find_nearest_base(self, mouse_x):
        alive_bases = [base for base in self.bases if base.is_alive]
        if not alive_bases:
            return None

        nearest_base = None
        min_distance = float('inf')
        for base in alive_bases:
            distance = abs(base.x - mouse_x)
            if distance < min_distance:
                min_distance = distance
                nearest_base = base
        return nearest_base

    def draw(self):
        for missile in self.missiles:
            missile.draw()
