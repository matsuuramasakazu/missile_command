import pyxel
from constants import * # SCREEN_WIDTH, SCREEN_HEIGHT should be here
# from game import Game # Will be imported after platform
from pyxel_game_platform import PyxelGamePlatform # Import PyxelGamePlatform
from game import Game # Import Game

if __name__ == "__main__":
    pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Missile Command")

    # Instantiate and use the platform
    platform = PyxelGamePlatform()
    platform.load_resource("my_resource.pyxres") # Use platform to load resources
    platform.set_mouse_visible(True) # Use platform to set mouse visibility

    # Pass the platform instance to the Game constructor
    game = Game(platform)

    pyxel.run(game.update, game.draw)
