import socket 


HEADER_LENGTH = 10

HOST = ("localhost", 4589)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

username = input("Enter yout username: ").encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")

client.connect(HOST) 
client.setblocking(0) 

# Send username to the server 
client.send(username_header + username)


# Send messages
while True: 
    message = input("Enter your message: ").encode("utf-8")
    
    if message: 
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
        client.send(message_header + message)
    else: 
        break
