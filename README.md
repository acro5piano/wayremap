[![test](https://github.com/acro5piano/wayremap/actions/workflows/test.yml/badge.svg)](https://github.com/acro5piano/wayremap/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/wayremap.svg)](https://badge.fury.io/py/wayremap)

# wayremap

Dynamic keyboard remapper for Wayland.

It works on both X Window Manager and Wayland, but focused on Wayland as it intercepts evdev input and require root permission.

# Motivation

Wayland and Sway is awesome. It brings lots of benefit to Linux desktop environment.

When I was using X desktop envionment, there is an awesome tool called `xremap` which remap keys **based on current focused application**.

https://github.com/k0kubun/xremap

I was looking for something similar to `xremap` for Wayland, but not found, so I decided to create on my own.

# Install

```bash
sudo pip install wayremap
```

# Run

For Wayland security model, we have to do execute key remapping as root.

Simply write your own service and run it as python script:

```python
 # /opt/wayremap.py

from wayremap.config import WayremapConfig, Binding
from wayremap.main import run
import uinput as k

wayremap_config = WayremapConfig(
    # Filter applications which remap will be applied
    applications=[
        'Chromium',
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

```

And then

```
sudo modprobe uinput
sudo python /opt/wayremap.py
```

Please note that

- modifier keys are `ctrl` or `alt` or both
- `'/dev/input/event4'` varies among system.

# Enable wayremap as systemd service

```bash
echo uinput | sudo tee /etc/modules-load.d/wayremap.conf # Add uinput to dependent linux modules
sudo vim /etc/wayremap.config.py # Edit your config
sudo cp systemd/wayremap.service /etc/systemd/system/wayremap.service
sudo systemctl enable wayremap
sudo reboot
```

# Known bugs

- ~~`3` is pressed when changing focused window~~ → Fixed now
- Key repeating become slow while switching focused windowd

# Roadmap

- Support `shift` key too.
- Enable to run wihtout Sway.
- Packaging for Arch Linux, Debian, Fedora, etc.
- Enable to load per-application config.
- Re-write in Rust for better performance.
