import time
import sys
import evdev
import uinput
from all_keys import ALL_KEYS
from config import Binding, example_config
from constants import ALL_KEYS, ALT_KEYS, CTRL_KEYS, EV_KEY


def is_pressed(value: int) -> bool:
    return value == 1 or value == 2


def list_devices():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print(device.path, device.name, device.phys)


def run(config: list[Binding], path: str):
    real_input = evdev.InputDevice(path)
    print("using device:", real_input)

    is_ctrl = False
    is_alt = False

    try:
        with uinput.Device(ALL_KEYS) as virtual_uinput:
            time.sleep(1)  # Important delay
            real_input.grab()

            for event in real_input.read_loop():
                if event.type == EV_KEY:
                    if event.code in CTRL_KEYS:
                        is_ctrl = is_pressed(event.value)
                    if event.code in ALT_KEYS:
                        is_alt = is_pressed(event.value)
                    handled = False
                    for binding in config:
                        pass_ctrl = is_ctrl and binding.only_ctrl()
                        pass_alt = is_alt and binding.only_alt()
                        pass_ctrl_alt = is_ctrl and is_alt and binding.require_ctrl_alt(
                        )
                        if ((pass_ctrl or pass_alt or pass_ctrl_alt)
                                and not handled
                                and event.code == binding.get_remap_keycode()
                                and is_pressed(event.value)):
                            handled = True
                            virtual_uinput.emit(uinput.KEY_CAPSLOCK, 0)
                            virtual_uinput.emit(uinput.KEY_LEFTALT, 0)
                            for key_combo in binding.to:
                                virtual_uinput.emit_combo(key_combo)
                            if is_ctrl:
                                virtual_uinput.emit(uinput.KEY_CAPSLOCK, 1)
                            if is_alt:
                                virtual_uinput.emit(uinput.KEY_LEFTALT, 1)
                    if not handled:
                        virtual_uinput.emit((0x01, event.code), event.value)
    except KeyboardInterrupt:
        real_input.ungrab()
        sys.exit(0)
    except OSError:
        print(
            "Error:\n  Failed to get device. Did you forget to run `sudo modprobe uinput`?"
        )


if __name__ == '__main__':
    # list_devices()
    run(example_config, '/dev/input/event4')
