
import socket
import random

# Diffie-Hellman parameters
a = random.randint(1, 10)  # Client's private key
p = 11  # Prime number
g = 5   # Generator

def encode_ascii(message):
    ascii_values = [ord(char) for char in message]
    return ascii_values

def decode_ascii(decrypted_array):
    plaintext = ''.join(chr(value) for value in decrypted_array)
    return plaintext

# Encrypting
def encrypt(message_ascii, key):
    encrypted_data = [element * key for element in message_ascii]
    return encrypted_data

# Decrypting
def decrypt(encrypted_message, key):
    decrypted_data = [int(element / key) for element in encrypted_message]
    return decrypted_data

# Diffie-Hellman Key Exchange
def diff_hellman():
    ska = pow(g, a, p)
    return ska

# Creating a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = 'localhost'
server_port = 9998

# Connecting to the server
client_socket.connect((server_ip, server_port))
print(f"Connected to the server at IP - {server_ip}:{server_port}")

# Send client's ska
ska = diff_hellman()
client_socket.send(bytes(str(ska), "utf-8"))

# Receive server's skb
skb_s = client_socket.recv(1024).decode("utf-8")
skb = int(skb_s)
print(f"Server's skb: {skb}")

# Calculate the shared key
shared_key = pow(skb, a, p)
print(f"\nShared key: {shared_key}")

# Begin communication
while True:
    message = input("Client: ")
    if message.lower() == "exit":
        client_socket.send(bytes(message, "utf-8"))  # Send 'exit' without encryption
        client_socket.close()
        print(f"Closed connection with server {server_ip}:{server_port}")
        break
    else:
        encrypted_message = encrypt(encode_ascii(message), shared_key)
        client_socket.send(bytes(str(encrypted_message), "utf-8"))

    encrypted_response = client_socket.recv(1024).decode("utf-8")
    encrypted_response = eval(encrypted_response)  # Convert to list
    response = decode_ascii(decrypt(encrypted_response, shared_key))

    if response.lower() == "exit":
        client_socket.close()
        print(f"Closed connection with server {server_ip}:{server_port}")
        break

    print(f"Server: {response}")

