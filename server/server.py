import threading
import socket
import shlex

# Thawin2551 Practice Networking Project
# in networking every data was sent as a bit bytes 0101010101
# this is the reason why i have to encode or decode everytime when i try to send or receive message from each client

host = "127.0.0.1" # local host
port = 10489

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creatae server
server.setsockopt(socket. SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port)) # bind server to host and port
server.listen() # listening for incoming connection

# e.g. {'username': <socket>}
clients = {} # to keep username for send the private message to each other
clients_lock = threading.Lock() # prevent dict change in the same time

# broadcast sent all request to all client (include client itself)

# send line is function that act like send function in socket library
# when client try to send message to other member it require to encode to ascii before
# this function help me to call send_line with sock (client) and message that i want to send directly
def send_line(sock, message):
    try:
        sock.sendall((message + "\n").encode("ascii"))
    except OSError:
        pass
    
def broadcast(message, exclude=None):
    with clients_lock:
        targets = list(clients.items())
    for nickname, client in targets:
        if nickname == exclude: # if nickname match exclude (nickname is None)
            continue
        send_line(client, message)

def send_private(sender_nickname, target_nickname, message):
    with clients_lock:
        target_user = clients.get(target_nickname)
        sender_user = clients.get(sender_nickname)
    if target_user is None:
        # told the sender user only not found
        # if server found target user (target nickname) return with [PRIVATE_MESSAGE] NOTATION
        # to the target user
        send_line(sender_user,  f"[SERVER] User '{target_nickname}' not found")
        return
    private_message = f"[PRIVATE MESSAGE] from {sender_nickname}: {message}"
    send_line(target_user, private_message)
    send_line(sender_user, f"[PRIVATE MESSAGE to {target_nickname}]: {message}")
    
# run on individual client
def handle(client, nickname):
    buffer = ""
    try:
        while True:
            data = client.recv(1024).decode("ascii") # decode bytes to string before comparing
            if not data:
                break
            buffer = buffer + data            
            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                if not message:
                    continue
            # Check Private Message keyword
                if message.startswith("/pm "):
                    parts = message.split(" ", 2)
                    if len(parts) < 3: # if format not correct like [/pm, "nickname", "message"] it will continue and broadcast to all user
                        send_line(client ,"[SERVER] Please send a message in the correct format: /pm <nickname> <message>")
                        continue
                    target_nickname = parts[1]
                    target_message = parts[2]
                    send_private(nickname, target_nickname, target_message)
            # if the message doesn't start with /pm keyword that mean is the public message
                else: 
                    broadcast(message, exclude=nickname) # encode back to bytes and broadcast to all client
        # Prevent error
    except (ConnectionResetError, OSError):
        pass
    finally:
        with clients_lock:
            clients.pop(nickname, None)
        client.close()
        broadcast(f"{nickname} has left the chat")

def receive_connection():
    while True:
        client, address_client = server.accept() 
        print(f"Connected with {(address_client)}") # alert the server that connected successfully
        
        # Checking Duplicate nickname (Nickname handshake loop)
        nickname = None
        try:
            while True:
                send_line(client, "NICK") # send a NICK keyword to server and encode to ascii
                name_requested = client.recv(1024).decode("ascii").strip()
                if not name_requested:
                    raise ConnectionResetError # หลุดตอนใส่ชื่อ
                with clients_lock:
                    taken = name_requested in clients
                if taken:
                    send_line(client, "TAKEN")
                else:
                    nickname = name_requested
                    with clients_lock:
                        clients[nickname] = client # add non duplicate nickname into clients dict to prevent duplicate name in advance
                    send_line(client, "OK")
                    break
        except (ConnectionResetError, OSError):
            client.close()
            continue
        
        # Display the username
        print(f"Nickname of the client is {nickname}.")
        send_line(client, "Connect to Server successfully !")
        broadcast(f"{nickname} joined the chat.", exclude=nickname) # exclude member that joining chat
        print("="*40)

        # for multithreading when many client send a message in the same time
        thread = threading.Thread(target=handle, args=(client, nickname))
        thread.start() # use the start method to run thread

print("Server is listening . . .")
receive_connection()