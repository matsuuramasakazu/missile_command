from constants import *
from base import Base
from city import City
from meteor_manager import MeteorManager
from missile_manager import MissileManager
from explosions_detector import ExplosionsDetector
from explosion import Explosion # Import Explosion
from ufo_manager import UFOManager
from explosion_manager import ExplosionManager
from game_platform_interface import IGamePlatform # Import IGamePlatform

class Game:
    def __init__(self, platform: IGamePlatform):
        self.platform = platform
        self.reset()

    def reset(self):
        self.score = 0
        self.game_over = False

        # Pass platform to Base and City constructors
        self.bases = [Base(x, self.platform) for x in BASE_X_POSITIONS]
        self.cities = [City(x, self.platform) for x in CITY_X_POSITIONS]

        # ExplosionManager constructor now requires the platform instance.
        self.explosion_manager = ExplosionManager(self.platform)
        self.meteor_manager = MeteorManager(self.explosion_manager, self.platform)
        self.missile_manager = MissileManager(self.bases, self.explosion_manager, self.platform)
        self.ufo_manager = UFOManager(self.platform)

        self.missile_explosions_detector = ExplosionsDetector(self.explosion_manager.get_explosions(), self.meteor_manager.meteors)
        self.meteor_explosions_detector = ExplosionsDetector(self.explosion_manager.get_explosions(), self.bases + self.cities)
        self.missile_ufo_explosions_detector = ExplosionsDetector(self.explosion_manager.get_explosions(), self.ufo_manager.ufos)

    def update(self):
        if self.game_over:
            if self.platform.is_mouse_button_pressed(self.platform.get_mouse_button_left()) or \
               self.platform.is_key_pressed(self.platform.get_key_space()):
                self.reset()
            return

        self.missile_manager.update()
        self.meteor_manager.update()
        self.ufo_manager.update()

        collided_meteors = self.missile_explosions_detector.check_collisions()
        for meteor in collided_meteors:
            meteor.is_alive = False
            # Pass platform to Explosion constructor
            self.explosion_manager.add_explosion_object(Explosion(meteor.x, meteor.y, self.platform))
        
        self.score += len(collided_meteors) * 5

        collided_bases_cities = self.meteor_explosions_detector.check_collisions()
        for item in collided_bases_cities:
            item.is_alive = False
            # Pass platform to Explosion constructor
            self.explosion_manager.add_explosion_object(Explosion(item.x, item.y, self.platform))

        self.score -= len(collided_bases_cities) * 5 # Negative score for losing cities/bases

        collided_ufos = self.missile_ufo_explosions_detector.check_collisions()
        for ufo in collided_ufos:
            ufo.is_alive = False
            # Pass platform to Explosion constructor
            self.explosion_manager.add_explosion_object(Explosion(ufo.x, ufo.y, self.platform))

        self.score += len(collided_ufos) * 10

        self.explosion_manager.update() # Explosion manager updates its explosions
        self.check_game_over()

    def check_game_over(self):
        if not any(city.is_alive for city in self.cities) or not any(base.is_alive for base in self.bases):
            self.game_over = True
        # else: # No need for else, game_over is reset in self.reset()
        #    self.game_over = False

    def draw(self):
        self.platform.clear_screen(0)
        self.platform.draw_rect(0, GRAND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GRAND_Y, GROUND_COLOR)

        for base in self.bases:
            base.draw()
        for city in self.cities:
            city.draw()
        self.meteor_manager.draw()
        self.missile_manager.draw()
        self.ufo_manager.draw()
        self.explosion_manager.draw()

        self.platform.draw_text(SCORE_TEXT_X, SCORE_TEXT_Y, f"SCORE: {self.score}", SCORE_TEXT_COLOR)

        if self.game_over:
            game_over_x = self.platform.get_screen_width() // 2 - GAME_OVER_TEXT_X_OFFSET
            game_over_y = self.platform.get_screen_height() // 2 - GAME_OVER_TEXT_Y_OFFSET
            self.platform.draw_text(game_over_x, game_over_y, "GAME OVER", GAME_OVER_TEXT_COLOR)

            retry_x = self.platform.get_screen_width() // 2 - RETRY_TEXT_X_OFFSET
            retry_y = self.platform.get_screen_height() // 2 + RETRY_TEXT_Y_OFFSET
            self.platform.draw_text(retry_x, retry_y, "CLICK or SPACE to RETRY", RETRY_TEXT_COLOR)
