import socket
import ssl
from cryptography.fernet import Fernet
import os
import signal


def server_conn(server_address, server_port):
    key = "Y7AYXeoiELaca2QtHeTubSGmbTOu27QyYin2f-Wfr3s="
    cipher_suite = Fernet(key)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tabData = []
    server_socket.bind((server_address, server_port))
    server_socket.listen(5)
    print("Serveur en écoute")
    conn, address_client = server_socket.accept()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        try:
            decrypted_data = cipher_suite.decrypt(data).decode("utf-8")
            print(decrypted_data)
            tabData.append(decrypted_data)
            if len(tabData)==2:
                filename = tabData[0]
                with open("./files/"+filename, 'a+') as file:
                    file.write(tabData[1])
                tabData=[]
        except Exception as e:
            print(f"Erreur : {e}")
        finally:
            server_socket.close()

def readfile(option):
    print(option)
    readfile_args = option.split()
    print(readfile_args)
    filename = readfile_args[1]
    
    try:
        with open("./files/"+filename, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f"Le fichier {filename} n'existe pas sur le serveur.")

def listen(option):
    listen_args = option.split()
    port = int(listen_args[1])
    server_conn("127.0.0.1", port)

def show():
    files=os.listdir("./files/")
    print("files in server")
    for file in files:
        print(file)

def kill_all_servers():
    print("Arrêt du serveur en cours...")
    os.kill(os.getpid(), signal.SIGTERM)

