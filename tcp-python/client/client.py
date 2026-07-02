import socket
import threading

local_host = '127.0.0.1'
port = 10489

nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((local_host, port))

def receive_message():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICK":
                client.send(nickname.encode("ascii")) # is match keyword send the nickname and encode to ascii to the server
            else: # if the keyword not NICK 
                print(message)
        except:
            # if error occur
            print("An error occured !")
            client.close()
            break

def write_message():
    while True:
        message = f"{nickname}: {input('')}"
        client.send(message.encode("ascii"))
        

receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

write_thread = threading.Thread(target=write_message)
write_thread.start()