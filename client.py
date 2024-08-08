import socket
import random

# Diffie-Hellman - KEP
a = 4
p = 11
g = 5

def encode_ascii(message):
    ascii_values = [ord(char) for char in message]
    return ascii_values

def decode_ascii(decripted_array):
    plaintext = ''.join(chr(value) for value in decripted_array)
    return plaintext

# Encrypting
def encrypt(message_ascii, key):
    encrypted_data = [element*key for element in message_ascii]
    return encrypted_data

# Decrypting
def decrypt(encrypted_message, key):
    decrypted_data = [int(element/key) for element in encrypted_message]
    return decrypted_data


# Diffie-Hellman - KEP
def diff_hellman():
    ska = (pow(g, a)) % p
    return ska

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

print(f"\nI HAVE BOTH THE KEYS ska - mine : {ska} and skb - server : {skb}")

# Calculate the shared key
key = (skb * a) % p

# Begin communication
while True:

    message = input("Client: ")
    if message.lower() == "exit":
        client_socket.close()
        print(f"Closed connection with server {server_ip}:{server_port}")
        break
    message=encrypt(encode_ascii(message),key)
    client_socket.send(bytes(str(message), "utf-8"))


    
    response = client_socket.recv(1024).decode("utf-8")
    response = decode_ascii(decrypt(response,key))
    if response.lower() == "exit":
        client_socket.close()
        print(f"Closed connection with server {server_ip}:{server_port}")
        break
    print(f"Server : {response}")
    


