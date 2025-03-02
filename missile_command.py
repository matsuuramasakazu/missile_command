import pyxel
import math
import random
from constants import *

class Base:
    def __init__(self, x):
        if not isinstance(x, (int, float)):
            raise TypeError("x must be a numeric value")
        self.x = x
        self.y = BASE_Y
        self.is_alive = True

    def draw(self):
        if self.is_alive:
            pyxel.blt(self.x - BASE_IMG_WIDTH // 2, self.y, 0, BASE_IMG_X, BASE_IMG_Y, BASE_IMG_WIDTH, BASE_IMG_HEIGHT)

class City:
    def __init__(self, x):
        self.x = x
        self.y = CITY_Y
        self.is_alive = True

    def draw(self):
        if self.is_alive:
            pyxel.blt(self.x - CITY_IMG_WIDTH // 2, self.y, 0, CITY_IMG_X, CITY_IMG_Y, CITY_IMG_WIDTH, CITY_IMG_HEIGHT)

class Meteor:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.is_alive = True
        self.angle = 0

    def update(self, bases, cities, explosions, score):
        self._move()
        if self.y >= GRAND_Y:
            self.is_alive = False
            return score, explosions

        score, explosions = self._check_base_collision(bases, explosions, score)
        score, explosions = self._check_city_collision(cities, explosions, score)
        
        return score, explosions

    def _move(self):
        self.y += self.speed * math.sin(math.radians(90 + self.angle))
        self.x += self.speed * math.cos(math.radians(90 + self.angle))

    def _check_city_collision(self, cities, explosions, score):
        for city in cities:
            distance = math.sqrt((self.x - city.x)**2 + (self.y - city.y - CITY_COLLISION_OFFSET)**2)
            if city.is_alive and distance <= CITY_IMG_WIDTH // 2:
                self.is_alive = False
                city.is_alive = False
                explosions.append(Explosion(self.x, self.y))
                return score - 5, explosions
        return score, explosions

    def _check_base_collision(self, bases, explosions, score):
        for base in bases:
            distance = math.sqrt((self.x - base.x)**2 + (self.y - base.y - BASE_COLLISION_OFFSET)**2)
            if base.is_alive and distance <= BASE_IMG_WIDTH // 2:
                self.is_alive = False
                base.is_alive = False
                explosions.append(Explosion(self.x, self.y))
                return score - 10, explosions
        return score, explosions

    def draw(self):
        if self.is_alive:
            pyxel.circ(self.x, self.y, METEOR_RADIUS, METEOR_COLOR)

class Missile:
    def __init__(self, start_base, target_x, target_y):
        self.start_x = start_base.x
        self.start_y = start_base.y
        self.x = self.start_x
        self.y = self.start_y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = MISSILE_SPEED
        self.is_alive = True
        self.explosion = None
        self.angle = math.atan2(target_y - self.start_y, target_x - self.start_x)

    def update(self):
        if not self.is_alive:
            return

        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance <= self.speed:
            self.x = self.target_x
            self.y = self.target_y
            self.is_alive = False
            self.explosion = Explosion(self.x, self.y)
        else:
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)

    def draw(self):
        if self.is_alive:
            pyxel.line(self.start_x, self.start_y, self.x, self.y, MISSILE_COLOR)
            pyxel.circ(self.x, self.y, MISSILE_RADIUS, MISSILE_COLOR)

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = EXPLOSION_INITIAL_RADIUS
        self.max_radius = EXPLOSION_RADIUS_MAX
        self.duration = EXPLOSION_DURATION
        self.is_alive = True

    def update(self):
        if not self.is_alive:
            return

        if self.radius >= self.max_radius or self.duration <= 0:
            self.is_alive = False
        else:
            self.radius += EXPLOSION_RADIUS_INCREMENT
            self.duration -= EXPLOSION_DURATION_DECREMENT

    def draw(self):
        if self.is_alive:
            pyxel.circ(self.x, self.y, self.radius, EXPLOSION_COLOR)

class MeteorManager:
    def __init__(self, bases, cities):
        self.bases = bases
        self.cities = cities
        self.meteors = []
        self.explosions = []

    def update(self, score):
        if pyxel.frame_count % METEOR_SPAWN_INTERVAL == 0:
            for _ in range(METEOR_SPAWN_COUNT):
                angle = random.uniform(-METEOR_ANGLE_RANGE, METEOR_ANGLE_RANGE)
                meteor_x = random.randint(0, SCREEN_WIDTH)
                meteor_speed = random.uniform(METEOR_SPEED_MIN, METEOR_SPEED_MAX) / 2
                meteor = Meteor(meteor_x, METEOR_INITIAL_Y, meteor_speed)
                meteor.angle = angle

                if not (0 - METEOR_OFFSCREEN_OFFSET < meteor.x + SCREEN_HEIGHT * math.cos(math.radians(90 + angle)) < SCREEN_WIDTH + METEOR_OFFSCREEN_OFFSET):
                    continue

                self.meteors.append(meteor)

        updated_meteors = []
        for meteor in self.meteors:
            prev_score = score
            score, self.explosions = meteor.update(self.bases, self.cities, self.explosions, score)
            if meteor.is_alive:
                updated_meteors.append(meteor)
            elif score == prev_score and meteor.y >= GRAND_Y:
                self.explosions.append(Explosion(meteor.x, GRAND_Y))
                self.check_ground_hit(meteor.x)
        self.meteors = updated_meteors
        return score

    def check_ground_hit(self, meteor_x):
        for base in self.bases:
            if base.is_alive and abs(base.x - meteor_x) < GROUND_HIT_DISTANCE:
                base.is_alive = False
        for city in self.cities:
            if city.is_alive and abs(city.x - meteor_x) < GROUND_HIT_DISTANCE:
                city.is_alive = False

    def draw(self):
        for meteor in self.meteors:
            meteor.draw()
        for explosion in self.explosions:
            explosion.draw()

class MissileManager:
    def __init__(self, bases):
        self.bases = bases
        self.missiles = []
        self.explosions = []

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if any(base.is_alive for base in self.bases):
                nearest_base = self.find_nearest_base(pyxel.mouse_x)
                if nearest_base:
                    self.missiles.append(Missile(nearest_base, pyxel.mouse_x, pyxel.mouse_y))

        updated_missiles = []
        for missile in self.missiles:
            missile.update()
            if missile.is_alive:
                updated_missiles.append(missile)
            elif missile.explosion:
                self.explosions.append(missile.explosion)
        self.missiles = updated_missiles

        updated_explosions = []
        for explosion in self.explosions:
            explosion.update()
            if explosion.is_alive:
                updated_explosions.append(explosion)
        self.explosions = updated_explosions

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
        for explosion in self.explosions:
            explosion.draw()

class CollisionDetector:
    def __init__(self, meteor_manager, missile_manager):
        self.meteor_manager = meteor_manager
        self.missile_manager = missile_manager

    def check_collisions(self):
        for explosion in self.missile_manager.explosions:
            if not explosion.is_alive:
                continue
            for meteor in self.meteor_manager.meteors:
                if not meteor.is_alive:
                    continue
                distance = math.sqrt((explosion.x - meteor.x)**2 + (explosion.y - meteor.y)**2)
                if distance < explosion.radius + COLLISION_DISTANCE:
                    meteor.is_alive = False
                    self.missile_manager.explosions.append(Explosion(meteor.x, meteor.y))
                    return True, meteor
        return False, None

class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.bases = [Base(x) for x in BASE_X_POSITIONS]
        self.cities = [City(x) for x in CITY_X_POSITIONS]
        self.meteor_manager = MeteorManager(self.bases, self.cities)
        self.missile_manager = MissileManager(self.bases)
        self.collision_detector = CollisionDetector(self.meteor_manager, self.missile_manager)
        self.score = 0
        self.game_over = False

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_SPACE):
                self.reset()
            return

        self.score = self.meteor_manager.update(self.score)
        self.missile_manager.update()

        is_collision, meteor = self.collision_detector.check_collisions()
        if is_collision:
            self.score += 5

        self.check_game_over()

    def check_ground_hit(self, meteor_x):
        for base in self.bases:
            if base.is_alive and abs(base.x - meteor_x) < GROUND_HIT_DISTANCE:
                base.is_alive = False
        for city in self.cities:
            if city.is_alive and abs(city.x- meteor_x) < GROUND_HIT_DISTANCE:
                city.is_alive = False

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

        pyxel.text(SCORE_TEXT_X, SCORE_TEXT_Y, f"SCORE: {self.score}", SCORE_TEXT_COLOR)

        if self.game_over:
            pyxel.text(pyxel.width // 2 - GAME_OVER_TEXT_X_OFFSET, pyxel.height // 2 - GAME_OVER_TEXT_Y_OFFSET, "GAME OVER", GAME_OVER_TEXT_COLOR)
            pyxel.text(pyxel.width // 2 - RETRY_TEXT_X_OFFSET, pyxel.height // 2 + RETRY_TEXT_Y_OFFSET, "CLICK or SPACE to RETRY", RETRY_TEXT_COLOR)

if __name__ == "__main__":
    pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Missile Command")
    pyxel.load("my_resource.pyxres")
    pyxel.mouse(True)
    game = Game()
    pyxel.run(game.update, game.draw)
