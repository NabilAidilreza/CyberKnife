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

def decrypt(ciphertext, flag_format,shift=None):
    for shift in range(1, 26):
        shift = int(shift)
        plaintext = ''
        for char in ciphertext:
            if char.isalpha():
                shift_base = 65 if char.isupper() else 97
                decrypted_char = chr((ord(char) - shift_base - shift) % 26 + shift_base)
                plaintext += decrypted_char
            else:
                plaintext += char 
        if flag_format in plaintext:
            return f"[+] Flag found: {plaintext} | Shift of {shift}"
    return plaintext

