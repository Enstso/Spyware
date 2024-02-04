import socket
import ssl
import os
import signal

def generate_keys():
    # Générer une paire de clés pour le serveur
    os.system("openssl req -nodes -newkey rsa:2048 -keyout server_private_key.pem -out server_csr.pem")
    os.system("openssl x509 -req -sha256 -days 365 -in server_csr.pem -signkey server_private_key.pem -out server_public_key.pem")

# Générer les clés pour le serveur
generate_keys()

# Chemins des clés du serveur
PRIVATE_KEY = "server_private_key.pem"
PUBLIC_KEY = "server_public_key.pem"

def server_conn(server_address, server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=PRIVATE_KEY, keyfile=PUBLIC_KEY)
    secure_socket = context.wrap_socket(server_socket, server_hostname=server_address)

    try:
        tabData = []
        secure_socket.bind((server_address, server_port))
        secure_socket.listen(5)
        print("Serveur en écoute")

        conn, address_client = secure_socket.accept()
        while True:
            data = conn.recv(1024)
            data_decode = data.decode()
            tabData.append(data_decode)
            if not data:
                filename = tabData[0]
                for i in range(1, len(tabData)):
                    with open(filename, 'a+') as file:
                        file.write(tabData[i])
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        secure_socket.close()

def readfile(option):
    readfile_args = option.split()
    filename = readfile_args[1]
    try:
        with open(filename, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f"Le fichier {filename} n'existe pas sur le serveur.")

def listen(option):
    listen_args = option.split()
    port = int(listen_args[1])
    server_conn("127.0.0.1", port)

def show():
    files = os.listdir(".")
    print("Fichiers sur le serveur :")
    for file in files:
        print(file)

def kill_all_servers():
    print("Arrêt de tous les serveurs en cours...")
    os.kill(os.getpid(), signal.SIGTERM)

if __name__ == "__main__":
    print("Serveur en attente de commandes...")
    while True:
        option = input("Saisissez une commande : ")
        if "-l" in option or "--listen" in option:
            listen(option)
        elif "-r" in option or "--readfile" in option:
            readfile(option)
        elif "-s" in option or "--show" in option:
            show()
        elif option in ["-k", "--kill"]:
            kill_all_servers()
            break
