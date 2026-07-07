import threading
import socket

# Thawin2551 Practice Networking Project
# in networking every data was sent as a bit bytes 0101010101
# this is the reason why i have to encode or decode everytime when i try to send or receive message from each client

host = "127.0.0.1" # local host
port = 10489

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creatae server
server.bind((host, port)) # bind server to host and port
server.listen() # listening for incoming connection

# e.g. {'username': <socket>}
clients = {} # to keep username for send the private message to each other
member_nickname = []

# broadcast sent all request to all client (include client itself)
def broadcast(message):
    for nickname, client in clients.items():
        client.send(message) # send the message to every connected client

def send_private(sender_nickname, target_nickname, message):
    target = clients.get(target_nickname)
    if target is None:
        # told the sender user only not found
        clients[sender_nickname].send(
            f"[SERVER] User '{target_nickname}' not found".encode("ascii")
        )
        # if server found target user (target nickname) return with [PRIVATE_MESSAGE] NOTATION
        # to the target user
        return # return nothing
    # message is already the text, encode once here
    private_message = f"[PRIVATE MESSAGE] from {sender_nickname}: {message}".encode("ascii")
    target.send(private_message) # private_message is already bytes, don't encode again
    # send message back to sender user
    clients[sender_nickname].send(f"[PRIVATE MESSAGE to {target_nickname}: {message}]".encode("ascii"))

# run on individual client
def handle(client, nickname):
    while True:
        try:
            message = client.recv(1024).decode("ascii") # decode bytes to string before comparing
            if message.startswith("/pm "):
                parts = message.split(" ", 2)
                if len(parts) < 3:
                    client.send("[SERVER] Please send in the correct format: /pm <nickname> <message>".encode("ascii"))
                    continue
                target_nickname = parts[1]
                target_message = parts[2]
                send_private(nickname, target_nickname, target_message)
            else: # if the message doesn't start with /pm keyword that mean is the public message
                broadcast(message.encode("ascii")) # encode back to bytes and broadcast to all client
        except:
            del clients[nickname]
            client.close()
            broadcast(f"{nickname} has left the chat".encode("ascii"))
            break

def receive_connection():
    while True:
        client, address_client = server.accept()
        print(f"Connected with {str(address_client)}") # alert the server that connected successfully
        client.send('NICK'.encode("ascii")) # send a NICK keyword to server and encode to ascii
        nickname = client.recv(1024).decode("ascii") # recv a client send NICK keyword and decode to ascii

        clients[nickname] = client # nickname is the target

        print(f"Nickname of the client is {nickname}.")
        broadcast(f"{nickname} joined the chat, wait before everyone join the group before start the conversation".encode("ascii"))
        client.send("Connected to the Server successfully !".encode("ascii"))
        print("="*40)

        # for multithreading when many client send a message in the same time
        thread = threading.Thread(target=handle, args=(client, nickname))
        thread.start() # use the start method to run thread

print("Server is listening . . .")
receive_connection()