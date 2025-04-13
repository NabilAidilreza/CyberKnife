from scripts.ciphers import base58

def encrypt(plaintext, shift=None):
    encoded_string = base58.b58encode(plaintext.encode())
    message = encoded_string.decode()
    return message

def decrypt(ciphertext, shift=None):
    decrypted_string = base58.b58decode(ciphertext)
    message = decrypted_string.decode()
    return message
