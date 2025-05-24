import pyxel
from constants import *
from base import Base
from city import City
from meteor_manager import MeteorManager
from missile_manager import MissileManager
from explosions_detector import ExplosionsDetector
from ufo_manager import UFOManager

class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.score = 0
        self.game_over = False

        self.bases = [Base(x) for x in BASE_X_POSITIONS]
        self.cities = [City(x) for x in CITY_X_POSITIONS]
        self.explosions = []  # 共通の爆発リスト

        self.meteor_manager = MeteorManager(self.explosions)
        self.missile_manager = MissileManager(self.bases, self.explosions)
        self.ufo_manager = UFOManager()

        self.missile_explosions_detector = ExplosionsDetector(self.explosions, self.meteor_manager.meteors)
        self.meteor_explosions_detector = ExplosionsDetector(self.explosions, self.bases + self.cities)
        self.missile_ufo_explosions_detector = ExplosionsDetector(self.explosions, self.ufo_manager.ufos)

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_SPACE):
                self.reset()
            return

        self.missile_manager.update()

        self.meteor_manager.update()
        
        collided_meteors, new_meteors_explosions = self.missile_explosions_detector.check_collisions()
        self.explosions.extend(new_meteors_explosions)
        self.score += len(collided_meteors) * 5
        for meteor in collided_meteors: # New loop
            meteor.is_alive = False     # New line

        collided_bases_cities, new_bases_cities_explosions = self.meteor_explosions_detector.check_collisions()
        self.explosions.extend(new_bases_cities_explosions)
        self.score -= len(collided_bases_cities) * 5 # Note: This looks like a bug, score should probably increase. However, stick to the requested change for now.
        for item in collided_bases_cities: # New loop
            item.is_alive = False      # New line

        self.ufo_manager.update()
        collided_ufos, new_ufos_explosions = self.missile_ufo_explosions_detector.check_collisions()
        self.explosions.extend(new_ufos_explosions)
        self.score += len(collided_ufos) * 10
        for ufo in collided_ufos: # New loop
            ufo.is_alive = False  # New line

        self.check_game_over()

    def check_game_over(self):
        if not any(city.is_alive for city in self.cities) or not any(base.is_alive for base in self.bases):
            self.game_over = True
        else:
            self.game_over = False

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, GRAND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GRAND_Y, GROUND_COLOR)

        for base in self.bases:
            base.draw()
        for city in self.cities:
            city.draw()
        self.meteor_manager.draw()
        self.missile_manager.draw()
        self.ufo_manager.draw()

        pyxel.text(SCORE_TEXT_X, SCORE_TEXT_Y, f"SCORE: {self.score}", SCORE_TEXT_COLOR)

        if self.game_over:
            pyxel.text(pyxel.width // 2 - GAME_OVER_TEXT_X_OFFSET, pyxel.height // 2 - GAME_OVER_TEXT_Y_OFFSET, "GAME OVER", GAME_OVER_TEXT_COLOR)
            pyxel.text(pyxel.width // 2 - RETRY_TEXT_X_OFFSET, pyxel.height // 2 + RETRY_TEXT_Y_OFFSET, "CLICK or SPACE to RETRY", RETRY_TEXT_COLOR)
