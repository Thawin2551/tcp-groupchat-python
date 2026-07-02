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

clients = []
member_nickname = []
 
# broadcast sent all request to all client (include client itself)
def broadcast(message):
    for client in clients:
        client.send(message) # client send a message
    
# run on individual client
def handle(client): 
    while True:
        try:
            message = client.recv(1024) # each client receive message
            broadcast(message) # and broadcast to all client
        except:
            index = clients.index(client) # if error at index i remove that index from process
            clients.remove(client) # remove the client from sending process
            client.close()
            nickname = member_nickname[index] # declare the remove member_nickname to nickname
            broadcast(f"{nickname} are left the chat".encode("ascii")) # when the member left chat broadcast to all member to acknowledge
            member_nickname.remove(nickname) # remove the member_nickname out of the chat after remove it
            break

def receive_connection():
    while True:
        client, address_client = server.accept()
        print(f"Connected with {str(address_client)}") # alert the server that connected successfully
        client.send('NICK'.encode("ascii")) # send a NICK keyword to server and encode to ascii 
        nickname = client.recv(1024).decode("ascii") # recv a client send NICK keyword and decode to ascii
        member_nickname.append(nickname) # append the new user with their nickname to member nickname list
        clients.append(client) # appned the new client to the client (s) list
        
        print(f"Nickname of the client is {nickname}.")
        broadcast(f"{nickname} joined the chat, wait before everyone join the group before start the conversation".encode("ascii"))
        client.send("Connected to the Server successfully !".encode("ascii"))
        print("="*40)

        # for multithreading when many client send a message in the same time
        thread = threading.Thread(target=handle, args=(client, ))
        thread.start() # use the start method to run thread

print("Server is listening . . .")    
receive_connection()