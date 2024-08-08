import socket
import random
import base64

# Diffe hellman  - KEP
a=4
p=11
g=5

def diff_hellman():
    ska = (pow(g,a))%p
    return ska


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = 'localhost'
server_port = 9998

#connecting to the Client
client_socket.connect((server_ip,server_port))
print(f"Connected to the server at ip - {server_ip}:{server_port}")


#Encoding key - int to ascii
ska = ascii(diff_hellman())
client_socket.send(bytes(ska,"utf-8"))


skb_s = client_socket.recv(1024).decode("utf-8")
skb = int(skb_s)
print(f"Server's skb: {skb}")


print(f"\nI HAVE BOTH THE KEYS ska - mine : {ska} and skb - server : {skb}")

#caliculating the key 
key = (skb*a)%p

while True:

    response = client_socket.recv(1024).decode()
    print(f"Server : {response}")
    if response.lower() == "exit":
        client_socket.close()
        print(f"closed connection with server {server_ip}:{server_port}")
        break
    
    message = input("Client: ")
    client_socket.send(bytes(message,"utf-8"))
    if message.lower() == "exit":
        client_socket.close()
        print(f"closed connection with server {server_ip}:{server_port}")
        break

