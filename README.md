# Spyware - Projet Final

Ce projet consiste en la création d'un spyware (logiciel espion) en Python 3, composé d'un client et d'un serveur. Le spyware doit être fonctionnel sur les systèmes Windows et Linux, et peut être utilisé en tant que programme exécutable. Il répond aux exigences suivantes :

## Exigences techniques pour le client :

Le client doit :
- Enregistrer les frappes de clavier dans un fichier caché sur le système de la victime.
- Envoyer le fichier de manière sécurisée au serveur via une socket réseau.
- S'arrêter si l'ordre est reçu du serveur et supprimer le fichier de capture.
- S'arrêter automatiquement après un maximum de 10 minutes de capture si le serveur est injoignable.

## Exigences techniques pour le serveur :

Le serveur doit :
- Réceptionner les données du client via une socket sécurisée.
- Écouter sur un port TCP depuis une machine externe et différente de la victime.
- Réceptionner les données reçues et les enregistrer dans un fichier unique pour chaque victime.
- Envoyer un message au spyware via la socket lui demandant de s'arrêter lorsque le serveur s'éteint.
- Pouvoir se connecter à un reverse shell du spyware.

- Embarquer les arguments suivants :
  - `-h/--help` : Affiche l'aide et les différentes options.
  - `-l <port>/--listen <port>` : Se met en écoute sur le port TCP spécifié par l'utilisateur et attend les données du spyware.
  - `-s/--show` : Affiche la liste des fichiers réceptionnés par le programme.
  - `-r <filename>/--readfile <filename>` : Affiche le contenu du fichier stocké sur le serveur du spyware. Le contenu doit être parfaitement lisible.
  - `-k/--kill` : Arrête toutes les instances de serveurs en cours, avertit le spyware de s'arrêter et de supprimer la capture.
  - `-t/--target` : Affiche toutes les victimes, actuellement connectées.
  - `-v <id>/--victim <id>` : envoie un message shell au spyware pour qu'il se connecte au netcat du serveur (reverse-shell).

## Fonctionnalités supplémentaires :

- Le serveur accepte les connexions multiples de clients et peut gérer plusieurs victimes en même temps. Il peut également gérer plusieurs fichiers de capture pour chaque victime.
- Si un client se connecte un message doit être envoyé à un bot discord grâce à un webhook pour avertir de la connexion.
- Le serveur doit être capable de se connecter à un reverse shell du spyware.
