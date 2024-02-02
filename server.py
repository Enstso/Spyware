import socket
import ssl

def server_conn(server_address, server_port, certificate_file):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_verify_locations(certificate_file)
    secure_socket = context.wrap_socket(server_socket, server_hostname=server_address)

    try:
        secure_socket.bind((server_address,server_port))
        secure_socket.listen(1)
        print("serveur sur écoute")
        conn,address_client = secure_socket.accept()
        data = conn.recv(1024)
    except Exception as e:
        print(f"error: {e}")
    finally:
        server_socket.close()


