import random
from constants import *
from ufo import UFO
from game_platform_interface import IGamePlatform

class UFOManager:
    def __init__(self, platform: IGamePlatform):
        self.platform = platform
        self.ufos = []
        self.next_spawn_frame = self.platform.get_frame_count() + random.uniform(UFO_SPAWN_INTERVAL, UFO_SPAWN_INTERVAL * 5)

    def update(self):
        if self.platform.get_frame_count() >= self.next_spawn_frame:
            self.spawn_ufo()
            self.next_spawn_frame = self.platform.get_frame_count() + random.uniform(UFO_SPAWN_INTERVAL, UFO_SPAWN_INTERVAL * 5)

        updated_ufos = []
        for ufo in self.ufos:
            ufo.update() # ufo.update() will be updated later to use platform if needed
            if ufo.is_alive:
                updated_ufos.append(ufo)
        self.ufos[:] = updated_ufos

    def spawn_ufo(self):
      # Spawn UFO at a random y position at the right edge of the screen
        y = random.randint(UFO_HEIGHT, UFO_FLYING_HEIGHT_LIMIT)
        zigzag = random.random() < 0.5  # 50%の確率でジグザグ移動
        # Pass platform to UFO constructor
        # SCREEN_WIDTH is a global constant from constants.py
        self.ufos.append(UFO(SCREEN_WIDTH, y, self.platform, zigzag=zigzag))

    def draw(self):
        for ufo in self.ufos:
            ufo.draw() # ufo.draw() will be updated later to use platform
