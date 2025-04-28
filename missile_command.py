import pyxel
from constants import *
from game import Game

if __name__ == "__main__":
    pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Missile Command")
    pyxel.load("my_resource.pyxres")
    pyxel.mouse(True)
    game = Game()
    pyxel.run(game.update, game.draw)
