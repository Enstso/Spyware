# 🕵️ Spyware

This project is a **Python 3 spyware** system consisting of a **client** and a **server**. The spyware is cross-platform, functional on both **Linux** and **Windows**, and can be compiled into executables.

---

## 🚀 Setup & Usage

### 1. Create Docker Network

#### On Linux (Bash)
```bash
docker network create spyware-net
```

#### On Windows (PowerShell)
```powershell
docker network create spyware-net
```

---

### 2. Build Docker Image

#### On Linux (Bash)
```bash
docker build -t spyware .
```

#### On Windows (PowerShell)
```powershell
docker build -t spyware .
```

---

### 3. Run Server Container

#### On Linux (Bash)
```bash
docker run -dit --name spyware-server -v $(pwd):/app --network spyware-net spyware
```

#### On Windows (PowerShell)
```powershell
docker run -dit --name spyware-server -v ${PWD}:/app --network spyware-net spyware
```

---

### 4. Run Client Container

#### On Linux (Bash)
```bash
docker run -dit --name spyware-client -v $(pwd):/app --network spyware-net spyware
```

#### On Windows (PowerShell)
```powershell
docker run -dit --name spyware-client -v ${PWD}:/app --network spyware-net spyware
```

---

### 5. Access Docker Containers

#### On Linux (Bash)
```bash
docker exec -it spyware-server bash
docker exec -it spyware-client bash
```

#### On Windows (PowerShell)
```powershell
docker exec -it spyware-server bash
docker exec -it spyware-client bash
```

---

### 6. Configure IP Address

Retrieve the **server container's IP address**:
```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' spyware-server
```
Update the `ip_server` variable in **client.py** and **server.py** with this IP.

---

### 7. Start the Spyware

#### Server
```bash
python3 spyware-server.py
```

#### Client
```bash
python3 client.py
```

---

## ⚙️ Project Specifications

### 🖥️ Client Features

The client:

- Records keystrokes in a hidden file on the victim's machine.
- Sends the captured keystrokes securely to the server over a network socket.
- Stops and deletes the capture file when receiving a shutdown command from the server.
- Automatically stops after **10 minutes** if the server is unreachable.

---

### 🖥️ Server Features

The server:

- Receives data securely from the client over a network socket.
- Listens on a **TCP port** from an external machine.
- Stores received data in a unique file for each victim.
- Sends a stop command to the client when the server shuts down.
- Allows connection to a **reverse shell** of the client.
- Manages multiple client connections simultaneously.

---

### 🧩 Command-Line Arguments

| Argument | Description |
|-------|-------|
| `-h, --help` | Show help and available options. |
| `-l <port>, --listen <port>` | Listen on a specified TCP port and wait for data. |
| `-s, --show` | Display the list of received files. |
| `-r <filename>, --readfile <filename>` | Display the content of a stored file. |
| `-k, --kill` | Stop all server instances, notify clients to stop and delete captures. |
| `-t, --target` | Show all currently connected victims. |
| `-v <id>, --victim <id>` | Send a reverse shell command to a specific victim. |

---

### 📬 Additional Features

- **Multiple Victim Management**: Handles multiple connections and capture files.
- **Discord Notification**: Sends a message via a **Discord Webhook** when a victim connects.
- **Reverse Shell Access**: Server can open a reverse shell on the client machine.

