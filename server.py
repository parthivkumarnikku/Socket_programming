import socket
import random

b = 6
p = 11
g = 5

# Diffie-Hellman - KEP
def diff_hellman():
    print(f"My random value is {b}")
    skb = (pow(g, b)) % p
    return skb

# Creating a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

# Server IP address and the server port
server_ip = 'localhost'
server_port = 9998

# Binding server socket to an IP address and a port
server_socket.bind((server_ip, server_port))

print(server_socket)
# Listen for incoming connections (up to 3 queued connections)
server_socket.listen(3)
print("Waiting for connections")

while True:
    # Accept a connection
    client_socket, address = server_socket.accept()
    print(f"{address} connected !!")

    # Receiving client's ska
    ska = int(client_socket.recv(1024).decode("utf-8"))
    print(f"Client's ska: {ska}")

    # Generate and send server's skb
    skb = diff_hellman()
    client_socket.send(bytes(str(skb), "utf-8"))

    print(f"\nI HAVE BOTH THE KEYS ska - client's : {ska} and skb - mine : {skb}")

    # Calculate the shared key
    key = (ska * b) % p

    # Begin communication
    while True:
        data = client_socket.recv(1024).decode("utf-8")
        print(f"Client: {data}")

        if data.lower() == "exit":
            print(f"\nClosed connection with the client {address} !!\n")
            client_socket.close()
            break

        response = input("Server: ")
        client_socket.send(bytes(response, "utf-8"))

        if response.lower() == "exit":
            print(f"\nClosed connection with the client {address} !!\n")
            client_socket.close()
            break
