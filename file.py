def encode_ascii(message):
    ascii_values = [ord(char) for char in message]
    return ascii_values

print(ascii(encode_ascii("mesage")))