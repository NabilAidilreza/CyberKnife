def encrypt(plaintext, shift=None):
    return plaintext

def decrypt(ciphertext, shift=None):
    decrypted_string = bytearray.fromhex(ciphertext)
    message = decrypted_string.decode()
    return message