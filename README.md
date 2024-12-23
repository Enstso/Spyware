# Spyware 

This project involves the creation of a spyware (spy software) in Python 3, consisting of a client and a server. The spyware must be functional on both Windows and Linux systems and can be used as an executable program. It meets the following requirements :

## Technical Requirements for the Client :

The client must :

- Record keystrokes in a hidden file on the victim's system.
- Send the file securely to the server via a network socket.
- Stop if the command is received from the server and delete the capture file.
- Automatically stop after a maximum of 10 minutes of capture if the server is unreachable.

## Technical Requirements for the Server :

The server must :

- Receive data from the client via a secure socket.
- Listen on a TCP port from an external machine, different from the victim's machine.
- Receive the data and save it in a unique file for each victim.
- Send a message to the spyware via the socket, instructing it to stop when the server shuts down.
- Be able to connect to a reverse shell of the spyware.

- Embed the following arguments :
  - `-h/--help` : Displays help and available options.
  - `-l <port>/--listen <port>` : Listens on the specified TCP port provided by the user and waits for data from the spyware.

  - `-s/--show` : Displays the list of files received by the program.
  - `-r <filename>/--readfile <filename>` : Displays the content of the file stored on the server from the spyware. The content must be perfectly readable.
  - `-k/--kill` : Stops all running server instances, notifies the spyware to stop and delete the capture.
  - `-t/--target` : Displays all victims currently connected.
  - `-v <id>/--victim <id>` :  Sends a shell message to the spyware to connect to the server’s netcat (reverse-shell).

## Additional Features :

- The server accepts multiple client connections and can manage multiple victims at the same time. It can also handle multiple capture files for each victim.
- When a client connects, a message should be sent to a Discord bot via a webhook to notify about the connection.
- The server must be able to connect to a reverse shell of the spyware.
