import socket
import ssl
import os
"""
def server_conn(server_address, server_port, certificate_file):
    print(server_port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_verify_locations(certificate_file)
    secure_socket = context.wrap_socket(server_socket, server_hostname=server_address)

    try:
        tabData = []
        secure_socket.bind((server_address,server_port))
        secure_socket.listen(5)
        print("serveur sur écoute")
        conn,addressClient = secure_socket.accept()
        while True:
            data = conn.recv(1024)
            dataDecode = data.decode()
            tabData.append(dataDecode)
            if not data:
                filename = tabData[0]
                for i in range(1,len(tabData)):
                    with open(filename,'a+') as file:
                        file.write(tabData[i])
    except Exception as e:
        print(f"error: {e}")
    finally:
        server_socket.close()
"""

def readfile(option):
    print(option)
    readfileargs = option.split()
    filename = readfileargs[1]
    with open("./files/"+filename,'r') as file:
        print(file.read())

def listen(option):
    listenargs = option.split()
    port = int(listenargs[1])
    certificate_file=""
    #server_conn("127.0.0.1",port,certificate_file)
    return port

def show():
    files=os.listdir("./files")
    print("files in server")
    for file in files:
        print(file)