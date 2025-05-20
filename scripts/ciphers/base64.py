from scripts.ciphers import base64

def encrypt(plaintext, shift=None):
    encoded_string = base64.b64encode(plaintext.encode())
    message = encoded_string.decode()
    return message

def decrypt(ciphertext, flag_format,shift=None):
    decrypted_string = base64.b64decode(ciphertext)
    message = decrypted_string.decode()
    if flag_format in message:
        return f"[+] Flag found: {message}"
    return message
