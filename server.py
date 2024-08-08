import socket
import random

# Diffie-Hellman parameters
b = 6
p = 11  # Prime number
g = 5   # Generator

def encode_ascii(response):
    ascii_values = [ord(char) for char in response]
    return ascii_values

def decode_ascii(decrypted_array):
    plaintext = ''.join(chr(value) for value in decrypted_array)
    return plaintext

# Encrypting
def encrypt(response_ascii, key):
    encrypted_data = [element * key for element in response_ascii]
    return encrypted_data

# Decrypting
def decrypt(encrypted_message, key):
    decrypted_data = [int(element / key) for element in encrypted_message]
    return decrypted_data

# Diffie-Hellman Key Exchange
def diff_hellman():
    skb = pow(g, b, p)
    return skb

# Creating a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

# Server IP address and port
server_ip = 'localhost'
server_port = 9998

# Binding server socket to an IP address and a port
server_socket.bind((server_ip, server_port))

# Listen for incoming connections (up to 3 connections)
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

    # Calculate the shared key
    shared_key = pow(ska, b, p)
    print(f"\nShared key: {shared_key}")

    # Begin communication
    while True:
        received_data = client_socket.recv(1024).decode("utf-8")
        
        # Check if the received message is 'exit'
        if received_data.lower() == "exit":
            print(f"\nClosed connection with the client {address} !!\n")
            client_socket.close()
            break

        encrypted_data = eval(received_data)  # Convert to list
        print(f"Recieved message - cipher : {encrypted_data}")
        data = decode_ascii(decrypt(encrypted_data, shared_key))
        print(f"Client: {data}")

        response = input("Server: ")
        if response.lower() == "exit":
            client_socket.send(bytes(response, "utf-8"))  # Send 'exit' without encryption
            client_socket.close()
            print(f"\nClosed connection with the client {address} !!\n")
            break
        else:
            encrypted_response = encrypt(encode_ascii(response), shared_key)
            print(f"encrypted response : {encrypted_response}")
            client_socket.send(bytes(str(encrypted_response), "utf-8"))

    print("Waiting for Connections .... ")
