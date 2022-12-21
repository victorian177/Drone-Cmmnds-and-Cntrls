from pynput import keyboard

from inputter import Inputter, EVENT_TYPES
from utils import string_stripper


class KeyboardInputter(Inputter):
    def set_event_catcher(self):
        """Setting event listener for keyboard."""
        self.event_catcher = keyboard.Events()
        self.event_catcher.start()

    def read_event(self):
        event_data = self.event_catcher.get()
        return event_data

    def resolve_event(self, event_data) -> dict:
        COMBINATION_KEY = "\\"
        SHORTCUT_KEY = "ctrl"
        PRESS = keyboard.Events.Press
        RELEASE = keyboard.Events.Release
        STRIP_LIST = ["'", "_l", "_r", "Key."]

        def get_key(event_data):
            key_string = str(event_data.key)
            key_string = string_stripper(key_string, STRIP_LIST)
            return key_string

        def key_combo(key_combo_hex):
            hex_str = key_combo_hex.replace(COMBINATION_KEY, "")
            letter = None

            if hex_str[0] == "r":
                letter = "m"
            else:
                integer = int(hex_str[1:], 16)
                if 1 <= integer <= 26:
                    letter = chr(ord("a") + integer - 1)

            key_combo_str = SHORTCUT_KEY + "+" + letter
            return key_combo_str

        event_type = None
        key = get_key(event_data)

        if COMBINATION_KEY in key:
            key = key_combo(key)

        if type(event_data) == PRESS:
            event_type = EVENT_TYPES[0]
        elif type(event_data) == RELEASE:
            event_type = EVENT_TYPES[1]

        event_info = {"type": event_type, "key": key}
        return event_info
