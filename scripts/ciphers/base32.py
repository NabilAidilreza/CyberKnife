from scripts.ciphers import base64

def encrypt(plaintext, shift=None):
    encoded_string = base64.b32encode(plaintext.encode())
    message = encoded_string.decode()
    return message

def decrypt(ciphertext, shift=None):
    decrypted_string = base64.b32decode(ciphertext)
    message = decrypted_string.decode()
    return message
