def encrypt(text,key=None):
    result = ''
    for char in text:
        if char.isalpha():  # Check if the character is a letter
            shift_base = 65 if char.isupper() else 97
            # Compute the reverse letter (A -> Z, B -> Y, etc.)
            result += chr(shift_base + (25 - (ord(char) - shift_base)))
        else:
            result += char 
    return result

def decrypt(text,key=None):
    result = ''
    for char in text:
        if char.isalpha():  # Check if the character is a letter
            shift_base = 65 if char.isupper() else 97
            # Compute the reverse letter (A -> Z, B -> Y, etc.)
            result += chr(shift_base + (25 - (ord(char) - shift_base)))
        else:
            result += char 
    return result