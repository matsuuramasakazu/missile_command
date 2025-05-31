from game_platform_interface import IGamePlatform
from screen_constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Mock constants for mouse buttons and keys
MOUSE_BUTTON_LEFT = 0
KEY_SPACE = 1

class TestGamePlatform(IGamePlatform):
    def __init__(self):
        self._mouse_x: int = 0
        self._mouse_y: int = 0
        self._pressed_mouse_buttons: set[int] = set()
        self._pressed_keys: set[int] = set()
        self._frame_count: int = 0
        self._mouse_visible: bool = True

    # Input state control methods
    def set_mouse_position(self, x: int, y: int) -> None:
        self._mouse_x = x
        self._mouse_y = y

    def set_mouse_button_pressed(self, button: int, pressed: bool) -> None:
        if pressed:
            self._pressed_mouse_buttons.add(button)
        else:
            self._pressed_mouse_buttons.discard(button)

    def set_key_pressed(self, key: int, pressed: bool) -> None:
        if pressed:
            self._pressed_keys.add(key)
        else:
            self._pressed_keys.discard(key)

    def increment_frame_count(self) -> None:
        self._frame_count += 1

    # IGamePlatform interface methods
    def is_mouse_button_pressed(self, button: int) -> bool:
        return button in self._pressed_mouse_buttons

    def get_mouse_x(self) -> int:
        return self._mouse_x

    def get_mouse_y(self) -> int:
        return self._mouse_y

    def is_key_pressed(self, key: int) -> bool:
        return key in self._pressed_keys

    def clear_screen(self, color: int) -> None:
        pass  # Minimal implementation

    def draw_rect(self, x: int, y: int, width: int, height: int, color: int) -> None:
        pass  # Minimal implementation

    def draw_text(self, x: int, y: int, text: str, color: int) -> None:
        pass  # Minimal implementation

    def load_resource(self, filename: str) -> None:
        pass # Minimal implementation for now, might need to store loaded resources if tests require it

    def draw_image(self, img_idx: int, x: int, y: int, u: int, v: int, width: int, height: int, color_key: int = None) -> None:
        pass  # Minimal implementation

    def get_frame_count(self) -> int:
        return self._frame_count

    def set_mouse_visible(self, visible: bool) -> None:
        self._mouse_visible = visible

    def get_screen_width(self) -> int:
        return SCREEN_WIDTH

    def get_screen_height(self) -> int:
        return SCREEN_HEIGHT

    def get_mouse_button_left(self) -> int:
        return MOUSE_BUTTON_LEFT

    def get_key_space(self) -> int:
        return KEY_SPACE

    def draw_circle(self, x: int, y: int, radius: int, color: int) -> None:
        pass  # Minimal implementation

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
        pass  # Minimal implementation
