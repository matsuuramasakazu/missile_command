import pyxel
import random
import math
from constants import *
from ufo import UFO
from ufo_manager import UFOManger
from base import Base
from city import City
from meteor import Meteor
from missile import Missile
from explosion import Explosion
from meteor_manager import MeteorManager
from missile_manager import MissileManager
from explosions_detector import ExplosionsDetector
from game import Game

if __name__ == "__main__":
    pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Missile Command")
    pyxel.load("my_resource.pyxres")
    pyxel.mouse(True)
    game = Game()
    pyxel.run(game.update, game.draw)
