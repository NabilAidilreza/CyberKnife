def create_substitution_dict(key):
    if len(key) < 26:
        raise ValueError
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower()
    substitution_dict = {alphabet[i]: key[i] for i in range(len(alphabet))}
    return substitution_dict

def encrypt(plaintext, key):
    substitution_dict = create_substitution_dict(key)
    ciphertext = ''
    for char in plaintext:
        if char.isalpha():  # Encrypt only alphabetic characters
            # Convert char to uppercase to match the dictionary (optional)
            #char = char.upper()
            ciphertext += substitution_dict.get(char, char)  # Keep non-alphabetic unchanged
        else:
            ciphertext += char
    return ciphertext

def decrypt(ciphertext, flag_format, key):
    substitution_dict = create_substitution_dict(key)
    # Reverse the substitution dictionary for decryption
    reverse_dict = {v: k for k, v in substitution_dict.items()}
    plaintext = ''
    for char in ciphertext:
        if char.isalpha():
            #char = char.upper()
            plaintext += reverse_dict.get(char, char)
        else:
            plaintext += char
    if flag_format in plaintext:
        return f"[+] Flag found: {plaintext}"
    return plaintext