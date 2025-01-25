# Function to perform XOR operation on two binary strings
def binary_xor(bin1, bin2):
    result = ""
    for i in range(8):
        result += '1' if bin1[i] != bin2[i] else '0'
    return result

# Function to convert a character to binary and pad with 0s
def char_to_binary(char):
    binary = bin(ord(char))[2:]
    return binary.zfill(8)  # Pad with 0s to make it 8 bits long

# Encryption function
def encrypt(plaintext, key):
    encryption_steps = []
    encrypted_text = ""
    for i in range(len(plaintext)):
        binary_plain = char_to_binary(plaintext[i])
        binary_key = char_to_binary(key[i % len(key)])
        result_binary = binary_xor(binary_plain, binary_key)
        hex_value = hex(int(
            result_binary, 2)
            )[2:].zfill(2)
        encryption_steps.append([plaintext[i], 
                                 ord(plaintext[i]), 
                                 binary_plain, 
                                 binary_key, 
                                 result_binary, 
                                 hex_value])
        encrypted_text += hex_value

    return encrypted_text#, encryption_steps

# Decryption function
def decrypt(encrypted_text, key):
    decryption_steps = []
    decrypted_text = ""
    for i in range(0, len(encrypted_text), 2):
        hex_value = encrypted_text[i:i+2]
        binary_plain = bin(int(hex_value, 16))[2:].zfill(8)
        binary_key = char_to_binary(key[i // 2 % len(key)])
        result_binary = binary_xor(binary_plain, binary_key)
        char = chr(int(result_binary, 2))
        decryption_steps.append([hex_value, 
                                 binary_plain, 
                                 binary_key, 
                                 result_binary, 
                                 char, 
                                 ord(char)])
        decrypted_text += char

    return decrypted_text#, decryption_steps


### Credit to HKTITAN (Harshit Khemani) ###