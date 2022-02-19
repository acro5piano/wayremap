import uinput as k
from wayremap import ecodes as e, WayremapConfig, Binding, run

applications = [
    'Brave-browser',
]

bindings = [
    Binding([e.KEY_LEFTCTRL, e.KEY_S], [[k.KEY_LEFTCTRL, k.KEY_F]]),
]

run(
    WayremapConfig(input_identifier=
                   'Lenovo TrackPoint Keyboard II usb-0000:00:14.0-1/input0',
                   applications=applications,
                   bindings=bindings),
    WayremapConfig(input_path='/dev/input/event4',
                   applications=applications,
                   bindings=bindings),
)
