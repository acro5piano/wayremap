# sway-remap

A keyboard remapper tool for Sway window manager. Still active development.

# Motivation

Sway and Wayland is awesome. It brings lots of benefit to Linux desktop environment.

When I was using X desktop envionment, there is an awesome tool called `xremap` which remap keys **based on current focused application**.

https://github.com/k0kubun/xremap

I was looking for something similar to `xremap`, but not found, so I decided to create on my own.

# Run

For Wayland security model, we have to do execute key remapping as root.

```bash
cargo build --release
sudo cp target/release/sway-remap /usr/local/bin
sudo sway-remap sway-remap.yml
```

where sway-remap.yml should be like this:

```yaml
- applications:
    - Brave-browser
    - firefoxdeveloperedition
    - Chromium
  remap:
    # OSX like key binding
    - from: leftalt.a
      to: [capslock.a]
    - from: leftalt.c
      to: [capslock.c]
    - from: leftalt.v
      to: [capslock.v]

    # Emacs like key binding (priority first)
    - from: leftalt.f
      to: [capslock.right]
    - from: leftalt.b
      to: [capslock.left]
    - from: leftalt.d
      to: [capslock.delete]
    - from: capslock.leftalt.h
      to: [capslock.backspace]

    - from: capslock.f
      to: [right]
    - from: capslock.b
      to: [left]
    - from: capslock.n
      to: [down]
    - from: capslock.p
      to: [up]
    - from: capslock.y
      to: [capslock.v]
    - from: capslock.h
      to: [backspace]
    - from: capslock.d
      to: [delete]
    - from: capslock.a
      to: [home]
    - from: capslock.e
      to: [end]
    - from: capslock.k
      to: [leftshift.end, capslock.x]
```

Note that:

- `leftctrl` can be work, but not tested

# Known bugs

- Cannot repeat key combo (such as `[leftshift.end, capslock.x]`)
- Sometimes hang
- Sway path should not be hard coded.
