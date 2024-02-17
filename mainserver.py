import argsServer
import server
import socket



def get_socket(server_address, server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
    server_socket.bind((server_address, server_port))

    return server_socket

def process_user_input(server_socket, args):
    if args.listen:
        server.listen(server_socket, args.listen)

    elif args.readfile:
        server.readfile(args.readfile)
        
    elif args.show:
        server.show()
        
    elif args.kill:
        server.kill_all_servers(server_socket)

    elif args.prompt:
        server.reverse_shell(server_socket, args.prompt)

    else:
        print("[LOG] No valid option provided.")


def main():
    parser = argsServer.arguments()
    server_socket = get_socket("127.0.0.1", 12345)
    server_socket.listen(5)

    while True:
        cmd = input(">>> ")
        try:
            args = parser.parse_args(cmd.split())
            process_user_input(server_socket, args)
            
        except Exception as e:
            print(f"[EXCEPTION] {e} \n")

if __name__ == "__main__":
    main()
