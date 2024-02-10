import socket
import os
import threading
import signal

PRIVATE_KEY_SERVER = """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDHpmK4ZHXeHfTm+5QGBN3HbMAV44YU4eQpRk6g+RFABp1UIFNe
RvvMktFp8+c6ZFQdvSqsrHNm2Ovr0kh/OlC1uUaOMyE3OstLGb9bWwLEQQkxsnMW
e/sp68YvZZx07nU5w0KcTHf01ID2B3H1/pJwXqaQu7pPtQ206Vlo2p01hQIDAQAB
AoGAO4zpjU6JycLttaf8sv7ol/9cHCtNZxUp1RXfhixEdPCEJP+vXkOV/6MbS5sw
sT4TyPsPq4mUsmypkiGa9jgSslq+VdolmCWbTvTWnNI/IGdefjfs0jx/+q4YMabW
0Dj1pBUtup+ZWxuu4lc1jV8vx4Cr5Gd741xiR9KVFYTHmYECQQDjm16eEjQyj8w8
8sPe/vT/d6Yt1xSN4M1tS8ewHdwJUy1hbxGZT7Q5pkZBS6S0iMUy3T5zMCzAmpTu
c7I+/gDtAkEA4I41tHGe4niD8RqEZ8uejw8JNSfYHEbLJ25OyXJaCZFZt1hxOVAH
VfF/3iSUzWbFnnZvoGIuykJaUwwpaLCr+QJBAKPxt/eYGS0KUwzbuKaZcxPItVRz
hgSkFpRRb2a2O1YkKZ3zCPQrax/TWuuRdvPrSE/Y+TCzVKjvL7OKdqvU/gkCQHq8
oBQRqmNktdFZyhclj3PoJwM71P6Xn0DdJQksjJQAM0Zoe/J0kJ3kExzrZ73hN5DG
cXr7T1HT9KTB1/xV3JkCQQCPGGt5zYm4R8XFrXROo+GDuC5nWpo3P/sQGeS5O19m
MaxhxOFF5Rd5AUQjmbkTbJUPK5f99qpQzXLkRAcqUyqU
-----END RSA PRIVATE KEY-----
"""
PUBLIC_KEY_SERVER = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDHpmK4ZHXeHfTm+5QGBN3HbMAV
44YU4eQpRk6g+RFABp1UIFNeRvvMktFp8+c6ZFQdvSqsrHNm2Ovr0kh/OlC1uUaO
MyE3OstLGb9bWwLEQQkxsnMWe/sp68YvZZx07nU5w0KcTHf01ID2B3H1/pJwXqaQ
u7pPtQ206Vlo2p01hQIDAQAB
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
