import socket
from cryptography.fernet import Fernet
import os
import threading
import sys
import psutil
import time
tab_conn = []

def handle_client(conn, cipher_suite):
    try:
        tabData = []
        while True:
            print("Waiting for data...")
            data = conn.recv(1024)
            if not data:
                break
            decrypted_data = cipher_suite.decrypt(data).decode("utf-8")
            print(decrypted_data)
            tabData.append(decrypted_data)
            if len(tabData) == 2:
                filename = tabData[0]
                with open("./files/" + filename, 'a+') as file:
                    file.write(tabData[1])
                tabData = []
                conn.close()
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def socket_alive(tab_conn):
    for conn in tab_conn:
        try:
            conn.getpeername()
        except OSError:
            tab_conn.remove(conn)
    return bool(tab_conn)

def clean():
    psutil.Process(get_pid()).terminate()
    
def get_pid():
    with open('serverpid.txt','r') as file:
        pid = file.read()
    return int(pid)

def write_pid():
    with open('serverpid.txt','w') as file:
        file.write(str(os.getpid()))

def verify_kill():
        while True:
            if os.path.exists('kill.txt') and socket_alive(tab_conn):
                send_kill_message(tab_conn)
                time.sleep(2)
            if os.path.exists('kill.txt') and not socket_alive(tab_conn):
                os.remove('kill.txt')
                clean()
           
        
def server_conn(server_address, server_port):
    write_pid()
    key = "Y7AYXeoiELaca2QtHeTubSGmbTOu27QyYin2f-Wfr3s="
    cipher_suite = Fernet(key)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_address, server_port))
    server_socket.listen(5)
    print("Server is listening...")

    while True:
        conn, address_client = server_socket.accept()
        tab_conn.append(conn)
        print("Waiting for data...")
        print(f"New connection from {address_client}")
        client_handler = threading.Thread(target=handle_client, args=(conn, cipher_suite))
        client_handler.start()
        threading.Thread(target=verify_kill).start()


def send_kill_message(tab_conn):
    
    key = "Y7AYXeoiELaca2QtHeTubSGmbTOu27QyYin2f-Wfr3s="
    message = "kill"
    print("Sending kill message to all clients...")
    for conn in tab_conn:
        if len(tab_conn)!=0:
            encrypted_message = Fernet(key).encrypt(message.encode('utf-8'))
            conn.send(encrypted_message)
            tab_conn.remove(conn)
    
def readfile(option):
    filename = option
    try:
        with open("./files/"+filename, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f"File {filename} does not exist on the server.")

def listen(option):
    port = option
    server_conn("192.168.1.13", port)

def show():
    files = os.listdir("./files/")
    print("Files on the server:")
    for file in files:
        print(file)

def kill_all_servers():
    with open('kill.txt', 'w') as file:
        file.write("kill")
    
