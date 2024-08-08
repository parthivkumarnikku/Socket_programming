import socket
import random

b=6
p=11
g=5

# Diffe hellman  - KEP
def diff_hellman():
    print(f"My random value is {b}")
    skb = (pow(g,b))%p
    return skb

def encryption(response,key):
    return response*key

def decryption(message, key):
    return message/key

# Creating a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

# server ip address and the server port
server_ip = 'localhost'
server_port = 9998

# Binding server socket to an ip address and a port
server_socket.bind((server_ip , server_port))

print(server_socket)
# Listen for incoming connections (up to 3 queued connections)
server_socket.listen(3)
print("Waiting for connections")

while True:
    # Accept a connection
    client_socket, address = server_socket.accept()
    print(f"{address} connected !!")
    
    #revieveing clients
    ska = int(client_socket.recv(1024).decode("utf-8"))
    print(f"Client's ska: {ska}")
    
    #Encoding key - int to ascii
    skb = ascii(diff_hellman())
    client_socket.send(bytes(skb,"utf-8"))

    print(f"\nI HAVE BOTH THE KEYS ska - client's : {ska} and skb - mine : {skb}")

    #caliculate key 
    key = (ska*b)%p

    client_socket.send(bytes("hello","utf-8"))


    while True:
        
        data = client_socket.recv(1024).decode("utf-8")
        print(f"Client: {data}")
        
        if data.lower() == "exit":
            print(f"\nClosed connection with the client {address} !!\n")
            client_socket.close()
            break
        response = input("server: ")
        client_socket.send(bytes(response, "utf-8"))
        
        if response.lower() == "exit":
            print(f"\nClosed connection with the client {address} !!\n")
            client_socket.close()
            break 
