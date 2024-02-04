def arguments():
    print("Usage: spyware-server.py\n")
    print("Options disponibles:\n")
    print(" -h, --help : Affiche l'aide et les différentes options.")
    print(" -l <port>, --listen <port> : Met en écoute sur le port TCP spécifié et attend les données du spyware.")
    print(" -s, --show : Affiche la liste des fichiers reçus par le programme.")
    print(" -r <filename>, --readfile <filename> : Affiche le contenu du fichier stocké sur le serveur du spyware.")
    print(" -k, --kill : Arrête toutes les instances de serveurs en cours, avertit le spyware de s'arrêter et de supprimer la capture.")
