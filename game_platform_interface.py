from abc import ABC, abstractmethod

class IGamePlatform(ABC):
    """
    Interface for a game platform, defining abstract methods for input, drawing, and resource management.
    """

    @abstractmethod
    def is_mouse_button_pressed(self, button: int) -> bool:
        """Checks if the specified mouse button is currently pressed."""
        pass

    @abstractmethod
    def get_mouse_x(self) -> int:
        """Gets the current x-coordinate of the mouse cursor."""
        pass

    @abstractmethod
    def get_mouse_y(self) -> int:
        """Gets the current y-coordinate of the mouse cursor."""
        pass

    @abstractmethod
    def is_key_pressed(self, key: int) -> bool:
        """Checks if the specified key is currently pressed."""
        pass

    @abstractmethod
    def clear_screen(self, color: int) -> None:
        """Clears the screen with the specified color."""
        pass

    @abstractmethod
    def draw_rect(self, x: int, y: int, width: int, height: int, color: int) -> None:
        """Draws a rectangle with the specified dimensions and color."""
        pass

    @abstractmethod
    def draw_text(self, x: int, y: int, text: str, color: int) -> None:
        """Draws text at the specified position with the specified color."""
        pass

    @abstractmethod
    def load_resource(self, filename: str) -> None:
        """Loads a resource from the specified file."""
        pass

    @abstractmethod
    def draw_image(self, img_idx: int, x: int, y: int, u: int, v: int, width: int, height: int, color_key: int = None) -> None:
        """Draws an image at the specified position with the specified parameters."""
        pass

    @abstractmethod
    def get_frame_count(self) -> int:
        """Gets the current frame count."""
        pass

    @abstractmethod
    def set_mouse_visible(self, visible: bool) -> None:
        """Sets the visibility of the mouse cursor."""
        pass

    @abstractmethod
    def get_screen_width(self) -> int:
        """Gets the width of the screen."""
        pass

    @abstractmethod
    def get_screen_height(self) -> int:
        """Gets the height of the screen."""
        pass

    @abstractmethod
    def get_mouse_button_left(self) -> int:
        """Gets the platform-specific constant for the left mouse button."""
        pass

    @abstractmethod
    def get_key_space(self) -> int:
        """Gets the platform-specific constant for the space key."""
        pass

    @abstractmethod
    def draw_circle(self, x: int, y: int, radius: int, color: int) -> None:
        """Draws a circle with the specified parameters."""
        pass

    @abstractmethod
    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
        """Draws a line with the specified parameters."""
        pass
