import os


def find(name, path):
    for root, _, files in os.walk(path):
        for file in files:
            if 'sway-ipc' in file:
                print(file)
                return os.path.join(root, name)


print(find('sway-ipc.1000.1601.sock', '/run/user/'))
