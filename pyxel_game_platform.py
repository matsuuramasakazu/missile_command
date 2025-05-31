import pyxel
from game_platform_interface import IGamePlatform

class PyxelGamePlatform(IGamePlatform):
    """
    Implementation of IGamePlatform using the Pyxel library.
    """

    def is_mouse_button_pressed(self, button: int) -> bool:
        """Checks if the specified mouse button is currently pressed."""
        return pyxel.btnp(button)

    def get_mouse_x(self) -> int:
        """Gets the current x-coordinate of the mouse cursor."""
        return pyxel.mouse_x

    def get_mouse_y(self) -> int:
        """Gets the current y-coordinate of the mouse cursor."""
        return pyxel.mouse_y

    def is_key_pressed(self, key: int) -> bool:
        """Checks if the specified key is currently pressed."""
        return pyxel.btnp(key)

    def clear_screen(self, color: int) -> None:
        """Clears the screen with the specified color."""
        pyxel.cls(color)

    def draw_rect(self, x: int, y: int, width: int, height: int, color: int) -> None:
        """Draws a rectangle with the specified dimensions and color."""
        pyxel.rect(x, y, width, height, color)

    def draw_text(self, x: int, y: int, text: str, color: int) -> None:
        """Draws text at the specified position with the specified color."""
        pyxel.text(x, y, text, color)

    def load_resource(self, filename: str) -> None:
        """Loads a resource from the specified file."""
        pyxel.load(filename)

    def draw_image(self, img_idx: int, x: int, y: int, u: int, v: int, width: int, height: int, color_key: int = None) -> None:
        """Draws an image at the specified position with the specified parameters."""
        # In Pyxel, img_idx typically refers to one of the three image banks (0, 1, or 2).
        # The actual image data is loaded into these banks via pyxel.load() or by editing them in the Pyxel editor.
        # u, v are the coordinates within the specified image bank.
        if color_key is None:
            pyxel.blt(x, y, img_idx, u, v, width, height)
        else:
            pyxel.blt(x, y, img_idx, u, v, width, height, color_key)

    def get_frame_count(self) -> int:
        """Gets the current frame count."""
        return pyxel.frame_count

    def set_mouse_visible(self, visible: bool) -> None:
        """Sets the visibility of the mouse cursor."""
        pyxel.mouse(visible)

    def get_screen_width(self) -> int:
        """Gets the width of the screen."""
        return pyxel.width

    def get_screen_height(self) -> int:
        """Gets the height of the screen."""
        return pyxel.height

    def get_mouse_button_left(self) -> int:
        """Gets the platform-specific constant for the left mouse button."""
        return pyxel.MOUSE_BUTTON_LEFT

    def get_key_space(self) -> int:
        """Gets the platform-specific constant for the space key."""
        return pyxel.KEY_SPACE

    def draw_circle(self, x: int, y: int, radius: int, color: int) -> None:
        """Draws a circle with the specified parameters."""
        pyxel.circ(x, y, radius, color)

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
        """Draws a line with the specified parameters."""
        pyxel.line(x1, y1, x2, y2, color)
