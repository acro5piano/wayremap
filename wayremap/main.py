import time
import sys
import evdev
import uinput
import os
from i3ipc import Connection, Event
from threading import Thread
import traceback

from wayremap import config, constants

is_remap_enabled = True


def get_identifier(device: evdev.InputDevice):
    return f'{device.name} {device.phys}'


def is_pressed(value: int) -> bool:
    return value == 1 or value == 2


def list_devices():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        identifier = get_identifier(device)
        print(f'{device.path}: {identifier}')


def find_input_path_from_name(device_identifier: str):
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if get_identifier(device) == device_identifier:
            return device.path
    raise Exception(f"Cannot find device named {device_identifier}")


def get_input_path(config: config.WayremapConfig):
    if config.input_path:
        return config.input_path
    elif config.input_identifier:
        return find_input_path_from_name(config.input_identifier)
    else:
        raise Exception(
            'You must specify either input_path or input_name to config.')


def find_sway_ipc_path() -> str:
    for root, _, files in os.walk('/run/user/'):
        for file in files:
            if 'sway-ipc' in file:
                return os.path.join(root, file)
    raise Exception('Cannot find sway socket under /run/user/')


def wait_sway(tried=0):
    try:
        find_sway_ipc_path()
    except:
        if tried == 10:
            raise Exception('Cannot find sway socket under /run/user/')
        else:
            print(f"Waiting for sway... {tried}")
            time.sleep(1)
            wait_sway(tried + 1)


def subscribe_sway(apps: list[str]):
    if apps is None or len(apps) == 0:
        print(
            "Warning: No applications specified to config. Applying remap to all applications."
        )
        return

    def on_window_focus(i3, _):
        global is_remap_enabled
        focused = i3.get_tree().find_focused()
        if not focused:  # some applications like bemenu, this check is needed.
            return
        app_name = focused.app_id or focused.window_class
        is_remap_enabled = app_name in apps
        print('Remap {} for {}'.format(is_remap_enabled, app_name))

    try:
        sway = Connection(find_sway_ipc_path())
        sway.on(Event.WINDOW_FOCUS, on_window_focus)
        sway.main()
    except:
        print(
            "Warning: Couldn't connect to Sway and  fallback to apply all applications. Is sway running?"
        )
        print(traceback.format_exc())


def remap(bindings: list[config.Binding], path: str):
    global is_remap_enabled
    real_input = evdev.InputDevice(path)
    print('using device:', real_input)

    is_ctrl = False
    is_alt = False

    try:
        with uinput.Device(constants.ALL_KEYS) as virtual_uinput:
            time.sleep(1)  # Important delay
            real_input.grab()

            for event in real_input.read_loop():
                print(event)
                if event.type == constants.EV_KEY:
                    if event.code in constants.CTRL_KEYS:
                        is_ctrl = is_pressed(event.value)
                    if event.code in constants.ALT_KEYS:
                        is_alt = is_pressed(event.value)
                    handled = False
                    for binding in bindings:
                        pass_ctrl = is_ctrl and binding.only_ctrl()
                        pass_alt = is_alt and binding.only_alt()
                        pass_ctrl_alt = is_ctrl and is_alt and binding.require_ctrl_alt(
                        )
                        if (is_remap_enabled and not handled
                                and (pass_ctrl or pass_alt or pass_ctrl_alt)
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
        print(traceback.format_exc())
        sys.exit(0)
    except OSError:
        print(
            "Error:\n  Failed to get device. Did you forget to run `sudo modprobe uinput`?"
        )
        print(traceback.format_exc())


def run(*configs: config.WayremapConfig):
    threads = list()

    for config in configs:
        thread_remap = Thread(target=remap,
                              args=(config.bindings, get_input_path(config)))
        threads.append(thread_remap)
        thread_remap.start()

        thread_subscribe_sway = Thread(target=subscribe_sway,
                                       args=(config.applications, ))
        threads.append(thread_subscribe_sway)
        thread_subscribe_sway.start()

    for t in threads:
        t.join()
