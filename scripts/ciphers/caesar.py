def encrypt(plaintext, shift=None):
    shift = int(shift)
    ciphertext = ''
    for char in plaintext:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            encrypted_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
            ciphertext += encrypted_char
        else:
            ciphertext += char 
    return ciphertext

def decrypt(ciphertext, shift=None):
    shift = int(shift)
    plaintext = ''
    for char in ciphertext:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            decrypted_char = chr((ord(char) - shift_base - shift) % 26 + shift_base)
            plaintext += decrypted_char
        else:
            plaintext += char 
    return plaintext
