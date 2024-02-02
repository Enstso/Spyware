import argsServer
import server
import sys

def main():
    try:
        option = ""

        while option not in ["-k", "--kill"]:
            option = input("Choose your flag: ")

            if option == "-h" or option == "--help":
                argsServer.arguments()

            elif "-l" in option or "--listen" in option:
                listenargs = option.split()
                port = int(listenargs[1])
                certificate_file=""
                server.server_conn("127.0.0.1",port,certificate_file)
            elif "-r" in option or "--readfile" in option:
                readfileargs = option.split()
                filename = readfileargs[1]
                with open(filename,'r') as file:
                    print(file.read())
            elif option in ["-k", "--kill"]:
                print("ls")
                sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)