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
            pyxel.blt(self.x - 8, self.y, 0, 8, 0, 16, 8) # ピクセルマップ描画

class City:
    def __init__(self, x):
        self.x = x
        self.y = CITY_Y
        self.is_alive = True

    def draw(self):
        if self.is_alive:
            pyxel.blt(self.x - 8, self.y, 0, 0, 8, 16, 8) # ピクセルマップ描画

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
            distance = math.sqrt((self.x - city.x)**2 + (self.y - city.y - 4)**2)
            if city.is_alive and distance <= 8:
                self.is_alive = False
                city.is_alive = False
                explosions.append(Explosion(self.x, self.y))
                return score - 5, explosions
        return score, explosions

    def _check_base_collision(self, bases, explosions, score):
        for base in bases:
            distance = math.sqrt((self.x - base.x)**2 + (self.y - base.y - 4)**2)
            if base.is_alive and distance <= 8:
                self.is_alive = False
                base.is_alive = False
                explosions.append(Explosion(self.x, self.y))
                return score - 10, explosions
        return score, explosions

    def draw(self):
        if self.is_alive:
            pyxel.circ(self.x, self.y, 1, 14)

class Missile:
    def __init__(self, start_base, target_x, target_y):
        self.start_x = start_base.x
        self.start_y = start_base.y
        self.x = self.start_x
        self.y = self.start_y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = 5
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
            pyxel.line(self.start_x, self.start_y, self.x, self.y, 10)
            pyxel.circ(self.x, self.y, 1, 10)

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 1
        self.max_radius = EXPLOSION_RADIUS_MAX
        self.duration = EXPLOSION_DURATION
        self.is_alive = True

    def update(self):
        if not self.is_alive:
            return

        if self.radius >= self.max_radius or self.duration <= 0:
            self.is_alive = False
        else:
            self.radius += 0.5
            self.duration -= 1

    def draw(self):
        if self.is_alive:
            pyxel.circ(self.x, self.y, self.radius, 8)

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Missile Command")
        pyxel.load("my_resource.pyxres") # リソースファイル読み込み
        self.reset() # ゲーム状態をリセット
        pyxel.mouse(True) # マウスポインタ表示

    def run(self):
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.bases = [Base(20), Base(160), Base(300)] # 基地のx座標を調整
        self.cities = [City(60), City(90), City(120), City(200), City(230), City(260)] # 都市のx座標を調整
        self.meteors = []
        self.missiles = []
        self.explosions = []
        self.score = 0
        self.game_over = False


    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_SPACE):
                self.reset() # ゲームリセット処理を呼び出す
            return

        if pyxel.frame_count % 30 == 0:
            for _ in range(1):
                angle = random.uniform(-45, 45)
                meteor_x = random.randint(0, SCREEN_WIDTH)
                meteor_speed = random.uniform(METEOR_SPEED_MIN, METEOR_SPEED_MAX)/2
                meteor = Meteor(meteor_x, 0, meteor_speed)
                meteor.angle = angle

                if not (0 - 5 < meteor.x + SCREEN_HEIGHT * math.cos(math.radians(90 + angle)) < SCREEN_WIDTH + 5):
                    continue

                self.meteors.append(meteor)

        updated_meteors = []
        for meteor in self.meteors:
            prev_score = self.score
            self.score, self.explosions = meteor.update(self.bases, self.cities, self.explosions, self.score)
            if meteor.is_alive:
                updated_meteors.append(meteor)
            elif self.score == prev_score and meteor.y >= GRAND_Y:
                self.explosions.append(Explosion(meteor.x, GRAND_Y))
                self.check_ground_hit(meteor.x)
        self.meteors = updated_meteors


        # Update and remove dead missiles and explosions
        for entity_list in [self.missiles, self.explosions]:
            updated_entities = []
            for entity in entity_list:
                entity.update()
                if entity.is_alive:
                    updated_entities.append(entity)
            entity_list[:] = updated_entities

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if any(base.is_alive for base in self.bases):
                nearest_base = self.find_nearest_base(pyxel.mouse_x)
                if nearest_base:
                    self.missiles.append(Missile(nearest_base, pyxel.mouse_x, pyxel.mouse_y))

        self.check_collisions()
        self.check_game_over()

    def check_ground_hit(self, meteor_x):
        for base in self.bases:
            if base.is_alive and abs(base.x - meteor_x) < 16:
                base.is_alive = False
        for city in self.cities:
            if city.is_alive and abs(city.x- meteor_x) < 16:
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

    def check_collisions(self):
        for explosion in self.explosions:
            if not explosion.is_alive:
                continue
            for meteor in self.meteors:
                if not meteor.is_alive:
                    continue
                distance = math.sqrt((explosion.x - meteor.x)**2 + (explosion.y - meteor.y)**2)
                if distance < explosion.radius + 3:
                    meteor.is_alive = False
                    self.score += 5
                    self.meteors.remove(meteor)
                    self.explosions.append(Explosion(meteor.x, meteor.y))

    def check_game_over(self):
        if not any(city.is_alive for city in self.cities) or not any(base.is_alive for base in self.bases):
            self.game_over = True
        else:
            self.game_over = False

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, GRAND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GRAND_Y, 2)

        for base in self.bases:
            base.draw()
        for city in self.cities:
            city.draw()
        for meteor in self.meteors:
            meteor.draw()
        for missile in self.missiles:
            missile.draw()
        for explosion in self.explosions:
            explosion.draw()

        pyxel.text(5, 5, f"SCORE: {self.score}", 7)

        if self.game_over:
            pyxel.text(pyxel.width // 2 - 40, pyxel.height // 2 - 10, "GAME OVER", 8)
            pyxel.text(pyxel.width // 2 - 60, pyxel.height // 2 + 5, "CLICK or SPACE to RETRY", 7)

if __name__ == "__main__":
    app = App()
    app.run()
