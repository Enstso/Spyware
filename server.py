import socket
import os
import threading
import signal

PRIVATE_KEY_SERVER = """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDHpmK4ZHXeHfTm+5QGBN3HbMAV44YU4eQpRk6g+RFABp1UIFNe
RvvMktFp8+c6ZFQdvSqsrHNm2Ovr0kh/OlC1uUaOMyE3OstLGb9bWwLEQQkxsnMW
e/
-----END RSA PRIVATE KEY-----
"""
PUBLIC_KEY_SERVER = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADC
-----END PUBLIC KEY-----
"""

def handle_client(client_socket, address_client):
    try:
        tabData = []
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            data_decode = data.decode()
            tabData.append(data_decode)

        filename = tabData[0]
        file_data = ''.join(tabData[1:])

        with open(filename, 'a+') as file:
            file.write(file_data)

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        client_socket.close()

def server_conn(server_address, server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=PRIVATE_KEY_SERVER, keyfile=PUBLIC_KEY_SERVER)
    secure_socket = context.wrap_socket(server_socket, server_hostname=server_address)

    try:
        secure_socket.bind((server_address, server_port))
        secure_socket.listen(5)
        print("Serveur en écoute")

        while True:
            client_socket, address_client = secure_socket.accept()
            print(f"Connexion entrante de {address_client}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket, address_client))
            client_handler.start()

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

def main():
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

if __name__ == "__main__":
    main()
