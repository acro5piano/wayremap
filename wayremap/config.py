from dataclasses import dataclass
import uinput as k
import wayremap.ecodes as e
from wayremap import constants


@dataclass
class Binding:
    remap: list[int]
    to: list[list[tuple[int, int]]]

    def get_remap_keycode(self) -> int:
        """
        @type evdev.ecodes.KEY_F
        """
        return self.remap[len(self.remap) - 1]

    def _has_ctrl(self) -> bool:
        for k in constants.CTRL_KEYS:
            if k in self.remap:
                return True
        return False

    def _has_alt(self) -> bool:
        for k in constants.ALT_KEYS:
            if k in self.remap:
                return True
        return False

    def only_ctrl(self) -> bool:
        return self._has_ctrl() and not self._has_alt()

    def only_alt(self) -> bool:
        return not self._has_ctrl() and self._has_alt()

    def require_ctrl_alt(self) -> bool:
        return self._has_ctrl() and self._has_alt()


@dataclass
class WayremapConfig:
    applications: list[str]
    bindings: list[Binding]


example_config = WayremapConfig(
    applications=[
        'Brave-browser',
        'chromium',
        'firefoxdeveloperedition',
    ],
    bindings=[
        # Emacs-like key binding
        Binding([e.KEY_LEFTCTRL, e.KEY_LEFTALT, e.KEY_A],
                [[k.KEY_LEFTCTRL, k.KEY_HOME]]),
        Binding([e.KEY_LEFTCTRL, e.KEY_LEFTALT, e.KEY_E],
                [[k.KEY_LEFTCTRL, k.KEY_END]]),
        Binding([e.KEY_LEFTCTRL, e.KEY_LEFTALT, e.KEY_H],
                [[k.KEY_LEFTCTRL, k.KEY_BACKSPACE]]),
        Binding([e.KEY_LEFTCTRL, e.KEY_F], [[k.KEY_RIGHT]]),
        Binding([e.KEY_LEFTCTRL, e.KEY_B], [[k.KEY_LEFT]]),
        Binding([e.KEY_LEFTCTRL, e.KEY_P], [[k.KEY_UP]]),
        Binding([e.KEY_LEFTCTRL, e.KEY_N], [[k.KEY_DOWN]]),
        Binding([e.KEY_LEFTCTRL, e.KEY_K],
                [[k.KEY_LEFTSHIFT, k.KEY_END], [k.KEY_LEFTCTRL, k.KEY_X]]),
        Binding([e.KEY_LEFTCTRL, e.KEY_A], [[k.KEY_HOME]]),
        Binding([e.KEY_LEFTCTRL, e.KEY_E], [[k.KEY_END]]),
        Binding([e.KEY_LEFTCTRL, e.KEY_Y], [[k.KEY_LEFTCTRL, k.KEY_V]]),
        Binding([e.KEY_LEFTALT, e.KEY_F], [[k.KEY_LEFTCTRL, k.KEY_RIGHT]]),
        Binding([e.KEY_LEFTALT, e.KEY_B], [[k.KEY_LEFTCTRL, k.KEY_LEFT]]),
        Binding([e.KEY_LEFTALT, e.KEY_D], [[k.KEY_LEFTCTRL, k.KEY_DELETE]]),
        Binding([e.KEY_LEFTCTRL, e.KEY_H], [[k.KEY_BACKSPACE]]),
        Binding([e.KEY_LEFTCTRL, e.KEY_D], [[k.KEY_DELETE]]),
        Binding([e.KEY_LEFTCTRL, e.KEY_S], [[k.KEY_LEFTCTRL, k.KEY_F]]),

        # OSX-like key binding
        Binding([e.KEY_LEFTALT, e.KEY_A], [[k.KEY_LEFTCTRL, k.KEY_A]]),
        Binding([e.KEY_LEFTALT, e.KEY_C], [[k.KEY_LEFTCTRL, k.KEY_C]]),
        Binding([e.KEY_LEFTALT, e.KEY_V], [[k.KEY_LEFTCTRL, k.KEY_V]]),

        # Slack helm!
        Binding([e.KEY_LEFTALT, e.KEY_X], [[k.KEY_LEFTCTRL, k.KEY_K]]),
    ])
