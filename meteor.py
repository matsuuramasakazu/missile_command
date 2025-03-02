import pyxel
import math
from constants import *
from explosion import Explosion

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
            explosions.append(Explosion(self.x, GRAND_Y))  # Add explosion at ground hit
            
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
