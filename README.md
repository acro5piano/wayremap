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

# For beta version
sudo pip3 install git+https://github.com/acro5piano/wayremap

```

# Run

For Wayland security model, we have to run key remapping as root permission.

Simply write your own service and run it as python script:

```python
 # /etc/wayremap.config.py

from wayremap import ecodes as e, run, WayremapConfig, Binding
import uinput as k

wayremap_config = WayremapConfig(
    # Note that `'/dev/input/event4'` varies among system.
    input_path='/dev/input/event4',

    # Filter applications which remap will be applied
    applications=[
        'Chromium',
        'Brave-browser',
        'Leafpad',
        'firefoxdeveloperedition',
    ],

    bindings=[
        # To see all available binding keys, please see
        # https://github.com/acro5piano/wayremap/blob/06d27c9bb86b766d7fd1e4230f3a16827785519e/wayremap/ecodes.py
        # modifier keys are `KEY_LEFTCTRL` or `KEY_LEFTALT`, or both. Neither `shift` nor `super` is not implemented yet.

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

# Finally, run wayremap.
run(wayremap_config)

```

And then

```
sudo modprobe uinput
sudo python /opt/wayremap.py
```

# Enable wayremap as a systemd service

```bash
echo uinput | sudo tee /etc/modules-load.d/wayremap.conf # Add uinput to auto-loaded linux modules
sudo vim /etc/wayremap.config.py # Edit your config
sudo cp ./systemd/wayremap.service /etc/systemd/system/wayremap.service
sudo systemctl enable wayremap
sudo reboot
```

# Known bugs

- ~~`3` is pressed when changing focused window~~ → Fixed now
- Key repeating become slow while switching focused windowd

# Roadmap

- [x] Enable to run wihtout Sway.
- [ ] Support `shift` and `super` keys too.
- [ ] Packaging for Arch Linux, Debian, Fedora, etc.
- [ ] Enable to load per-application config.
- [ ] Re-write in Rust for better performance.
