from wayremap.config import WayremapConfig, Binding
from wayremap.main import run
import uinput as k

wayremap_config = WayremapConfig(
    applications=[
        'Brave-browser',
        'Leafpad',
        'firefoxdeveloperedition',
    ],
    bindings=[
        # Emacs-like key binding
        Binding('ctrl.alt.a', [[k.KEY_LEFTCTRL, k.KEY_HOME]]),
        Binding('ctrl.alt.e', [[k.KEY_LEFTCTRL, k.KEY_END]]),
        Binding('ctrl.alt.h', [[k.KEY_LEFTCTRL, k.KEY_BACKSPACE]]),
        Binding('ctrl.f', [[k.KEY_RIGHT]]),
        Binding('ctrl.b', [[k.KEY_LEFT]]),
        Binding('ctrl.p', [[k.KEY_UP]]),
        Binding('ctrl.n', [[k.KEY_DOWN]]),
        Binding('ctrl.k',
                [[k.KEY_LEFTSHIFT, k.KEY_END], [k.KEY_LEFTCTRL, k.KEY_X]]),
        Binding('ctrl.a', [[k.KEY_HOME]]),
        Binding('ctrl.e', [[k.KEY_END]]),
        Binding('ctrl.y', [[k.KEY_LEFTCTRL, k.KEY_V]]),
        Binding('alt.f', [[k.KEY_LEFTCTRL, k.KEY_RIGHT]]),
        Binding('alt.b', [[k.KEY_LEFTCTRL, k.KEY_LEFT]]),
        Binding('alt.d', [[k.KEY_LEFTCTRL, k.KEY_DELETE]]),
        Binding('ctrl.h', [[k.KEY_BACKSPACE]]),
        Binding('ctrl.s', [[k.KEY_LEFTCTRL, k.KEY_F]]),

        # OSX-like key binding
        Binding('alt.a', [[k.KEY_LEFTCTRL, k.KEY_A]]),
        Binding('alt.c', [[k.KEY_LEFTCTRL, k.KEY_C]]),
        Binding('alt.v', [[k.KEY_LEFTCTRL, k.KEY_V]]),
        Binding('alt.x', [[k.KEY_LEFTCTRL, k.KEY_X]]),

        # Slack helm!
        Binding('alt.x', [[k.KEY_LEFTCTRL, k.KEY_K]]),
    ])

run(wayremap_config, '/dev/input/event4')
