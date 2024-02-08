import enum
import time

from pyglet.window import key


class Buttons(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()
    CONFIRM = enum.auto()
    CANCEL = enum.auto()
    PLAY_1 = enum.auto()
    PLAY_2 = enum.auto()
    PLAY_3 = enum.auto()
    PLAY_4 = enum.auto()
    PLAY_5 = enum.auto()
    PLAY_6 = enum.auto()


class InputEvent:
    def __init__(self, key, pressed=True):
        self.time = time.time()
        self.pressed = pressed
        self.key = key

    def __repr__(self):
        return f"InputEvent({self.key}, {self.pressed})"


class InputManager:

    def __init__(self):
        self.reset()
        self.mapping = {
            key.UP: Buttons.UP,
            key.DOWN: Buttons.DOWN,
            key.LEFT: Buttons.LEFT,
            key.RIGHT: Buttons.RIGHT,
            key.ENTER: Buttons.CONFIRM,
            key.ESCAPE: Buttons.CANCEL,
            key.S: Buttons.PLAY_1,
            key.D: Buttons.PLAY_2,
            key.F: Buttons.PLAY_3,
            key.J: Buttons.PLAY_4,
            key.K: Buttons.PLAY_5,
            key.L: Buttons.PLAY_6,
        }

    def translate_key(self, symbol):
        return self.mapping.get(symbol)

    def handle_key_with_state(self, symbol, pressed):
        self.raw_events.append(InputEvent(symbol, pressed))
        self.raw_active_keys[symbol] = pressed
        button = self.translate_key(symbol)
        if button:
            self.active_buttons[button] = pressed
            self.events.append(InputEvent(button, pressed))
            return True
        return False

    def handle_key_press(self, symbol):
        return self.handle_key_with_state(symbol, True)

    def handle_key_release(self, symbol):
        return self.handle_key_with_state(symbol, False)

    def _poll(self, events):
        if not events:
            return False
        return events.pop()

    def poll(self):
        """Returns the last event, or False if there are no events."""
        return self._poll(self.events)

    def poll_raw(self):
        """Same as self.poll, but for raw events"""
        return self._poll(self.raw_events)

    def reset(self):
        self.reset_raw()
        self.reset_inputs()

    def reset_raw(self):
        self.raw_events = []
        self.raw_active_keys = {}

    def reset_inputs(self):
        self.events = []
        self.active_buttons = {x: False for x in Buttons}
