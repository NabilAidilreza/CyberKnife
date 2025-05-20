
def encrypt(plain_text, key):
   encrypted = ''
   # Repeat key to match the length of the plaintext.
   keys_text = (key * (len(plain_text) // len(key))) + key[:len(plain_text) % len(key)]
   for i in range(len(plain_text)):
       # Check if alphabet letter.
       if plain_text[i].isalpha():
           # Calculate shift based on corresponding key letter.
           shift = ord(keys_text[i].upper()) - ord('A')
           # Encrypt uppercase and lowercase letters separately.
           if plain_text[i].isupper():
               encrypted += chr((ord(plain_text[i]) + shift - ord('A')) % 26 + ord('A'))
           else:
               encrypted += chr((ord(plain_text[i]) + shift - ord('a')) % 26 + ord('a'))
       else:
           encrypted += plain_text[i]
   return encrypted

def decrypt(cipher_text, flag_format, key):
    decrypted = ''
    key_index = 0  # Track index only for alphabetic characters

    for char in cipher_text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)].upper()) - ord('A')
            if char.isupper():
                decrypted += chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
            else:
                decrypted += chr((ord(char) - shift - ord('a')) % 26 + ord('a'))
            key_index += 1  # Only advance key index for letters
        else:
            decrypted += char  # Non-letters stay unchanged

    if flag_format in decrypted:
        return f"[+] Flag found: {decrypted}"
    return decrypted

