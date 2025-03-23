import socket 
import select 


HEADER_LENGTH = 10
HOST = ("localhost", 4589)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

server.bind(HOST) 
server.listen() 
print("Listening connection!")


sockets_list = [server] 
clients = {} 


def receive_message(client: socket.socket): 
    message_header = client.recv(HEADER_LENGTH)
    if not len(message_header): 
        return False 
    
    message_length = int(message_header.decode("utf-8").strip()) 
    return {
        "header": message_header, 
        "data": client.recv(message_length).decode("utf-8")
    }


while True: 
    rs, _, xs = select.select(sockets_list, [], sockets_list)
    for _socket in rs: 
        if _socket == server: 
            client, addr = server.accept() 

            message = receive_message(client)
            
            if message is False: 
                continue 

            print(f"{message['data']} joined to the chat!")
            
            sockets_list.append(client) 
            clients[client] = message
        else: 
            message = receive_message(client)
            if not message: 
                sockets_list.remove(client) 
                clients.pop(client) 
            
            print(f"{clients[client]['data']}: {message['data']}")

        for _socket in xs: 
            sockets_list.remove(_socket) 
            clients.pop(_socket)
