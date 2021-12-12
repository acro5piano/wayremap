from i3ipc import Connection, Event

i3 = Connection()


# Dynamically name your workspaces after the current window class
def on_window_focus(i3, _):
    focused = i3.get_tree().find_focused()
    app_name = focused.app_id or focused.window_class
    print(app_name)


# Subscribe to events
i3.on(Event.WINDOW_FOCUS, on_window_focus)

# Start the main loop and wait for events to come in.
i3.main()
