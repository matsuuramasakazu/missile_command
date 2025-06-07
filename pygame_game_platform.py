import pygame
import os # For path joining
from game_platform_interface import IGamePlatform
from constants import SCREEN_WIDTH, SCREEN_HEIGHT # Assuming these are in constants

# Placeholder for Pygame specific key mappings if needed
# For example: PYGAME_KEY_SPACE = pygame.K_SPACE

class PygameGamePlatform(IGamePlatform):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pygame Game") # Basic caption
        self.font = pygame.font.Font(None, 36) # Default font
        self._frame_count = 0
        self.spritesheet_surface = None
        # It's good practice to call load_resource() early,
        # but the main test block will call it for now.

    def is_mouse_button_pressed(self, button: int) -> bool:
        # Pygame's mouse buttons are 0 (left), 1 (middle), 2 (right)
        # This mapping might need adjustment based on how 'button' is defined in IGamePlatform
        # For now, assuming 'button' maps directly or via provided constants like get_mouse_button_left()
        return pygame.mouse.get_pressed()[button]

    def get_mouse_x(self) -> int:
        return pygame.mouse.get_pos()[0]

    def get_mouse_y(self) -> int:
        return pygame.mouse.get_pos()[1]

    def is_key_pressed(self, key: int) -> bool:
        # This requires a mapping from IGamePlatform key constants to Pygame key constants
        # Placeholder:
        keys = pygame.key.get_pressed()
        # Assuming 'key' is a Pygame constant like pygame.K_SPACE
        if 0 <= key < len(keys):
            return keys[key]
        return False

    def clear_screen(self, color: int = (0, 0, 0)) -> None:
        # Assuming color is an RGB tuple
        self.screen.fill(color)

    def draw_rect(self, x: int, y: int, width: int, height: int, color: int) -> None:
        # Assuming color is an RGB tuple
        pygame.draw.rect(self.screen, color, (x, y, width, height))

    def draw_text(self, x: int, y: int, text: str, color: int) -> None:
        # Assuming color is an RGB tuple
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def load_resource(self, filename: str) -> None:
        # The 'filename' argument is ignored. Load the main spritesheet.
        spritesheet_path = os.path.join("assets", "spritesheet.png")
        # Attempt to use __file__ to make path relative to this script file
        # This is more robust if the script is run from a different current working directory.
        if '__file__' in locals(): # Check if __file__ is defined (not always the case, e.g. in some embedded scenarios)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            spritesheet_path = os.path.join(script_dir, "assets", "spritesheet.png")
        else: # Fallback to CWD-relative path if __file__ is not available
            spritesheet_path = os.path.join("assets", "spritesheet.png")


        try:
            self.spritesheet_surface = pygame.image.load(spritesheet_path).convert_alpha()
            print(f"Loaded spritesheet: {spritesheet_path}")
        except pygame.error as e:
            print(f"Error loading spritesheet {spritesheet_path}: {e}")
            self.spritesheet_surface = None
        except FileNotFoundError:
            print(f"Spritesheet file not found: {spritesheet_path}")
            self.spritesheet_surface = None
        return None


    def draw_image(self, img_idx: int, x: int, y: int, u: int, v: int, width: int, height: int, color_key: int = None) -> None:
        # img_idx and color_key are ignored for now.
        # Transparency is handled by convert_alpha() on load or would need a global color key.
        if not self.spritesheet_surface:
            # Optionally draw a placeholder if the spritesheet is missing
            # For now, just print a warning or do nothing.
            # print("Warning: Spritesheet not loaded, cannot draw image.")
            return

        # Create a Rect for the area to blit from the source spritesheet
        source_area = pygame.Rect(u, v, width, height)

        # Blit the specified part of the spritesheet
        self.screen.blit(self.spritesheet_surface, (x, y), area=source_area)

    def get_frame_count(self) -> int:
        # This could be a simple counter incremented each frame/update
        return self._frame_count # Needs to be incremented somewhere, e.g., in a game loop update method

    def set_mouse_visible(self, visible: bool) -> None:
        pygame.mouse.set_visible(visible)

    def get_screen_width(self) -> int:
        return self.screen.get_width()

    def get_screen_height(self) -> int:
        return self.screen.get_height()

    def get_mouse_button_left(self) -> int:
        # Pygame's constant for the left mouse button is 0
        return 0

    def get_key_space(self) -> int:
        # Placeholder: Return Pygame's constant for the space key
        return pygame.K_SPACE

    def draw_circle(self, x: int, y: int, radius: int, color: int) -> None:
        # Assuming color is an RGB tuple
        pygame.draw.circle(self.screen, color, (x, y), radius)

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
        # Assuming color is an RGB tuple
        pygame.draw.line(self.screen, color, (x1, y1), (x2, y2))

    # Additional methods that might be useful for a Pygame platform:
    def update_display(self):
        pygame.display.flip()
        self._frame_count += 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame.quit() # Do not call pygame.quit() here.
                return False # Indicate game should close by returning False
        return True # Indicate game should continue

    def quit(self):
        pygame.quit()

# Need to import image constants for the test block
from image_constants import CITY_IMG_X, CITY_IMG_Y, CITY_IMG_WIDTH, CITY_IMG_HEIGHT

if __name__ == '__main__':
    # Example Usage (Optional: for testing the platform directly)
    platform = PygameGamePlatform()
    platform.load_resource(None) # Load the spritesheet

    running = True
    color_red = (255, 0, 0)
    color_blue = (0, 0, 255)
    color_green = (0, 255, 0)
    color_white = (255, 255, 255)

    rect_x, rect_y = 50, 50
    circle_x, circle_y = 200, 150

    sprite_draw_x = 100
    sprite_draw_y = 100


    while running:
        running = platform.handle_events() # Handle window close and other events

        # Input handling example
        if platform.is_mouse_button_pressed(platform.get_mouse_button_left()):
            rect_x, rect_y = platform.get_mouse_x() - 25, platform.get_mouse_y() - 25

        if platform.is_key_pressed(platform.get_key_space()):
            # Move the drawn sprite when space is pressed
            sprite_draw_y += 5
            if sprite_draw_y > platform.get_screen_height() - CITY_IMG_HEIGHT:
                sprite_draw_y = 100


        platform.clear_screen((10,20,30)) # Dark blue background

        platform.draw_rect(rect_x, rect_y, 50, 50, color_red)
        platform.draw_circle(circle_x, circle_y, 30, color_blue)
        platform.draw_line(0,0, platform.get_screen_width(), platform.get_screen_height(), color_green)
        platform.draw_text(10, 10, f"Frame: {platform.get_frame_count()}", color_white)
        platform.draw_text(10, 30, f"Mouse: ({platform.get_mouse_x()}, {platform.get_mouse_y()})", color_white)

        # Test drawing part of the spritesheet (the "city" part)
        # img_idx is 0 (ignored), x, y for screen position, then u,v,w,h from image_constants
        if platform.spritesheet_surface:
            platform.draw_image(0, sprite_draw_x, sprite_draw_y,
                                CITY_IMG_X, CITY_IMG_Y,
                                CITY_IMG_WIDTH, CITY_IMG_HEIGHT)
        else:
            platform.draw_text(10, 70, "Spritesheet not loaded!", color_red)


        platform.update_display()
        pygame.time.Clock().tick(60) # Limit to 60 FPS

    platform.quit()
