import pyfiglet
import argsServer
import mainserver
import os

pyfiglet.print_figlet("Spyware")
argsServer.arguments()

if __name__ == "__main__":
    os.system('nohup python3 server.py &')