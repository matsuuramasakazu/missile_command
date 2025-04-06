import pyxel
import random
from constants import *
from ufo import UFO

class UFOManager:
    def __init__(self):
        self.ufos = []
        self.next_spawn_frame = pyxel.frame_count + random.uniform(UFO_SPAWN_INTERVAL, UFO_SPAWN_INTERVAL * 5)

    def update(self):
        if pyxel.frame_count >= self.next_spawn_frame:
            self.spawn_ufo()
            self.next_spawn_frame = pyxel.frame_count + random.uniform(UFO_SPAWN_INTERVAL, UFO_SPAWN_INTERVAL * 5)

        updated_ufos = []
        for ufo in self.ufos:
            ufo.update()
            if ufo.is_alive:
                updated_ufos.append(ufo)
        self.ufos[:] = updated_ufos

    def spawn_ufo(self):
      # Spawn UFO at a random y position at the right edge of the screen
        y = random.randint(UFO_HEIGHT, UFO_FLYING_HEIGHT_LIMIT)
        self.ufos.append(UFO(SCREEN_WIDTH, y))

    def draw(self):
        for ufo in self.ufos:
            ufo.draw()
