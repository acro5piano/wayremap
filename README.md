# wayremap

A dynamic keyboard remapper for Wayland. 

It works on both X Window Manager and Wayland, but focused on Wayland as it intercepts evdev input and require root permission.

# Motivation

Sway and Wayland is awesome. It brings lots of benefit to Linux desktop environment.

When I was using X desktop envionment, there is an awesome tool called `xremap` which remap keys **based on current focused application**.

https://github.com/k0kubun/xremap

I was looking for something similar to `xremap`, but not found, so I decided to create on my own.

# Run

For Wayland security model, we have to do execute key remapping as root.

```bash
# TODO: easy install with pip
# pip install wayremap python-uinput evdev
```

And write your own service:

```python
from wayremap import run

wayremap_config = [
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

    # OSX-like key binding
    Binding('alt.a', [[k.KEY_LEFTCTRL, k.KEY_A]]),
    Binding('alt.c', [[k.KEY_LEFTCTRL, k.KEY_C]]),
    Binding('alt.v', [[k.KEY_LEFTCTRL, k.KEY_V]]),
    Binding('alt.x', [[k.KEY_LEFTCTRL, k.KEY_X]]),
]


run(wayremap_config, '/dev/input/event4') 
```

Note that `'/dev/input/event4'` varies among system.
