import pygame # PygameGamePlatform might need pygame to be imported where it's run
from pygame_game_platform import PygameGamePlatform
from game import Game
from constants import SCREEN_WIDTH, SCREEN_HEIGHT # Ensure these are available

if __name__ == "__main__":
    # Initialize the platform
    platform = PygameGamePlatform()

    # Load game resources (e.g., images, sounds)
    # The argument to load_resource is ignored by PygameGamePlatform,
    # as it loads a predefined set of images.
    platform.load_resource(None)

    # Set mouse visibility
    platform.set_mouse_visible(True) # Or False, depending on game needs

    # Create the game instance
    game = Game(platform)

    # Game loop
    running = True
    while running:
        # Handle platform-specific events (like window close)
        # The handle_events() method in PygameGamePlatform should
        # process Pygame events and return False if pygame.QUIT is detected.
        if not platform.handle_events():
            running = False

        # Update game logic
        game.update()

        # Draw game elements
        # game.draw() typically calls platform methods to draw on the screen
        game.draw()

        # Update the display (e.g., flip the Pygame buffer)
        platform.update_display()

        # Pygame specific: control frame rate (optional, but good practice)
        # This can also be part of PygameGamePlatform's update_display or a separate method
        if hasattr(pygame, 'time') and hasattr(pygame.time, 'Clock'):
             pygame.time.Clock().tick(60) # Limit to 60 FPS


    # Quit the platform (this should include pygame.quit())
    platform.quit()
