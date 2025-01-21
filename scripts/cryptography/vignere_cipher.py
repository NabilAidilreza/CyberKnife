
def vigenere_encrypt(plain_text, key):
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

def vigenere_decrypt(cipher_text, key):
    decrypted = ''
    # Repeat  key to match the length of the ciphertext.
    keys_text = (key * (len(cipher_text) // len(key))) + key[:len(cipher_text) % len(key)]
    for i in range(len(cipher_text)):
        # Check if alphabet letter
        if cipher_text[i].isalpha():
            # Calculate  shift based on  corresponding key letter.
            shift = ord(keys_text[i].upper()) - ord('A')
            # Decrypt uppercase and lowercase letters separately.
            if cipher_text[i].isupper():
                decrypted += chr((ord(cipher_text[i]) - shift - ord('A')) % 26 + ord('A'))
            else:
                decrypted += chr((ord(cipher_text[i]) - shift - ord('a')) % 26 + ord('a'))
        else:
            # If character is not an alphabet letter, keep it unchanged
            decrypted += cipher_text[i]
    return decrypted




key = "KEY"
plaintext = input('[!] Enter your message: ')
cipher_text = vigenere_encrypt(plaintext, key)
print(f"[+] Plaintext: {plaintext}")
print(f"[+] Ciphertext: {cipher_text}")
ask_to_decrypt = input('\n\n[?] Do you want to decrypt the message?\n[?] Y or N: ').lower()
if ask_to_decrypt == 'y':
   decrypted = vigenere_decrypt(cipher_text, key)
   print(f"[+] Decrypted text: {decrypted}")
elif ask_to_decrypt == 'n':
   pass
else:
   print(f"[-] Invalid input.")