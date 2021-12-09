import time
import sys
import evdev
import uinput
from all_keys import ALL_KEYS
from config import Binding, WayremapConfig, example_config
from constants import ALL_KEYS, ALT_KEYS, CTRL_KEYS, EV_KEY
from i3ipc import Connection, Event
from threading import Thread


def is_pressed(value: int) -> bool:
    return value == 1 or value == 2


is_remap_enabled = True


def list_devices():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print(device.path, device.name, device.phys)


def subscribe_sway(apps: list[str]):
    def on_window_focus(i3, _e):
        global is_remap_enabled
        focused = i3.get_tree().find_focused()
        app_name = focused.app_id or focused.window_class
        is_remap_enabled = app_name in apps
        print('Remap {} for {}'.format(is_remap_enabled, app_name))

    sway = Connection('/run/user/1000/sway-ipc.1000.1601.sock')
    sway.on(Event.WINDOW_FOCUS, on_window_focus)
    sway.main()


def remap(bindings: list[Binding], path: str):
    global is_remap_enabled
    real_input = evdev.InputDevice(path)
    print('using device:', real_input)

    is_ctrl = False
    is_alt = False

    try:
        with uinput.Device(ALL_KEYS) as virtual_uinput:
            time.sleep(1)  # Important delay
            real_input.grab()

            for event in real_input.read_loop():
                if not is_remap_enabled:
                    virtual_uinput.emit((0x01, event.code), event.value)
                elif event.type == EV_KEY:
                    if event.code in CTRL_KEYS:
                        is_ctrl = is_pressed(event.value)
                    if event.code in ALT_KEYS:
                        is_alt = is_pressed(event.value)
                    handled = False
                    for binding in bindings:
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


def run(config: WayremapConfig, path: str):
    threads = list()

    thread_remap = Thread(target=remap, args=(config.bindings, path))
    threads.append(thread_remap)
    thread_remap.start()

    thread_subscribe_sway = Thread(target=subscribe_sway,
                                   args=(config.applications, ))
    threads.append(thread_subscribe_sway)
    thread_subscribe_sway.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    # list_devices()
    run(example_config, '/dev/input/event4')
