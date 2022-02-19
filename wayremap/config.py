from dataclasses import dataclass
from typing import Optional
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
    input_path: Optional[str] = None
    input_identifier: Optional[str] = None
