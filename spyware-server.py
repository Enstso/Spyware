import pyfiglet
import argsServer
import mainserver
import os

if __name__ == "__main__":
    pyfiglet.print_figlet("Spyware")
    argsServer.arguments()
    if not os.path.exists("files"):
        os.mkdir("files")
    mainserver.main()
