import socket
import ssl
from cryptography.fernet import Fernet
import os
import signal

import threading


def func_handle_client(conn, cipher_server):
    try:
        tabData = []
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            decrypted_data = cipher_server.decrypt(data).decode("utf-8")
            print(decrypted_data)
            tabData.append(decrypted_data)
            if len(tabData) == 2:
                filename = tabData[0]
                with open("./files/" + filename, 'a+') as file:
                    file.write(tabData[1])
                tabData = []
    finally:
        conn.close()

def server_conn(server_address, server_port):
    key = "Y7AYXeoiELaca2QtHeTubSGmbTOu27QyYin2f-Wfr3s="
    cipher_server = Fernet(key)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((server_address, server_port))
    server_socket.listen(5)
    print("Serveur en écoute")

    try:
        while True:
            conn, address_client = server_socket.accept()
            print(f"New connection of {address_client}")
            client_handler = threading.Thread(target=func_handle_client, args=(conn, cipher_server))
            client_handler.start()
    except Exception as e:
        print(f'error: {e}')
    finally:
        server_socket.close()

def readfile(option):
    filename = option
    try:
        with open("./files/"+filename, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f"Le fichier {filename} n'existe pas sur le serveur.")

def listen(option):
    
    port = option
    server_conn("127.0.0.1", port)

def show():
    files=os.listdir("./files/")
    print("files in server")
    for file in files:
        print(file)

def kill_all_servers():
    print("Arrêt du serveur en cours...")

    """
    Envoyer le message aux clients pour stopper toutes les connexions

    il faut tuer le processus à la fin, car si le processus est mort impossible de récupérer les infos des clients
    """
    os.kill(os.getpid(), signal.SIGTERM)

