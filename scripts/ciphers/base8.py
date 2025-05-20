def encrypt(plaintext, shift=None):
    return plaintext

def decrypt(ciphertext,flag_format, shift=None):
    decrypted_string = bytearray.fromhex(ciphertext)
    message = decrypted_string.decode()
    if flag_format in message:
        return f"[+] Flag found: {message}"
    return message