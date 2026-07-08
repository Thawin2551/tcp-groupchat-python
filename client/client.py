import socket
import threading
import os

local_host = '127.0.0.1'
port = 10489

# Create a client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect condition
try:
    client.connect((local_host, port))
except ConnectionRefusedError:
    print("Cannot connect to the SERVER [server.py], Server might not start or incorrect port")
    raise SystemExit(1)

# receive buffer from server
recv_buffer = ""
def recv_line(): # receive send_line from server.py
    global recv_buffer
    while "\n" not in recv_buffer:
        data = client.recv(1024).decode("ascii")
        if not data:
            return None # Server close
        recv_buffer = recv_buffer + data
    line, recv_buffer = recv_buffer.split("\n", 1)
    return line
    
# set default nickname to none 
nickname = None
while True:
    signal = recv_line()
    if signal is None: # No signal (No message send to)
        print("Connection was closed")
        raise SystemExit(1)
    if signal == "NICK": # if server sent the NICK keyword
        name = input("Enter your name: ").strip()
        client.sendall((name + "\n").encode("ascii"))
        result = recv_line()
        if result == "OK":
            nickname = name # if result = "OK" set the name for new user
            break
        else:
            print(f"This name '{name}' has been taken")

# windows is name nt if not use clear (Mac, Linux)
os.system("cls" if os.name == "nt" else "clear")
print("Connected to the server successfully!")
print("Please wait for others to join before starting the conversation...\n")

# receive_message from client
def receive_message():
    while True:
        line = recv_line()
        if line is None:
            print("Connection to the Server was closed")
            break
        print(line) 
        
def write_message():
    while True:
        try:
            message = input("") # user type message to other
        except EOFError:
            break
        if not message:
            continue # if no message continue and loop till the end (user leave)
        if message.startswith("/pm "):
            client.sendall((message + "\n").encode("ascii"))
        else:
            client.sendall((f"{nickname}: {message}\n").encode("ascii"))
        
# create new thread after receive message
threading.Thread(target=receive_message, daemon=True).start()

# create new thread after user write the message 
write_thread = threading.Thread(target=write_message)
write_thread.start()
write_thread.join()