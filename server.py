import socket
from cryptography.fernet import Fernet
import os
import signal
import threading
import sys
import psutil
import time
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

def server_conn(server_address, server_port):
    write_pid()
    
    key = "Y7AYXeoiELaca2QtHeTubSGmbTOu27QyYin2f-Wfr3s="
    cipher_suite = Fernet(key)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((server_address, server_port))
    server_socket.listen(5)
    print("Serveur en écoute")

 
    while True:
        conn, address_client = server_socket.accept()
        tab_conn.append(conn)
        print(f"Nouvelle connexion de {address_client}")

        client_handler = threading.Thread(target=handle_client, args=(conn, cipher_suite))
        client_handler.start()

    
def send_kill_message(tab_conn):
    if os.path.exists('kill.txt') == True:
        message = "kill"
        for conn in tab_conn:
            conn.send(message.encode("utf-8"))
            
            

def readfile(option):
    filename = option
    try:
        with open("./files/"+filename, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f"Le fichier {filename} n'existe pas sur le serveur.")

def listen(option):
    
    port = option
    server_conn("192.168.1.16", port)

def show():
    files=os.listdir("./files/")
    print("files in server")
    for file in files:
        print(file)

def kill_all_servers():
    print("Arrêt du serveur en cours...")
    with open('kill.txt','w+') as file:
        file.write('kill')

    



