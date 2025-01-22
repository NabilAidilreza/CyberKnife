import os
import importlib
from time import sleep
from InquirerPy import prompt
import scripts.system.log_format as lf

#! Hub for Main Functions #

#? ### Cryptography ###
def try_decrypt_ciphers(ciphertext, key=None):
    results = {}
    for module_name in os.listdir('scripts/ciphers'):
        if module_name.endswith('.py') and module_name != '__init__.py':
            cipher_name = module_name[:-3]  # Remove .py extension
            try:
                cipher_module = importlib.import_module(f'scripts.ciphers.{cipher_name}')
                # Call the decryption function dynamically
                if hasattr(cipher_module, 'decrypt'):
                    decrypted_text = cipher_module.decrypt(ciphertext, key)
                    results[cipher_name] = decrypted_text
            except Exception as e:
                results[cipher_name] = f"fail => {str(e)}"
    return results

def try_encrypt_ciphers(plaintext, key=None):
    results = {}
    for module_name in os.listdir('scripts/ciphers'):
        if module_name.endswith('.py') and module_name != '__init__.py':
            cipher_name = module_name[:-3]  # Remove .py extension
            try:
                cipher_module = importlib.import_module(f'scripts.ciphers.{cipher_name}')
                # Call the decryption function dynamically
                if hasattr(cipher_module, 'encrypt'):
                    encrypted_text = cipher_module.encrypt(plaintext, key)
                    results[cipher_name] = encrypted_text
            except Exception as e:
                results[cipher_name] = f"fail => {str(e)}"
    return results

def execute_ciphers(operation, text, key):
    lf.warning(f"BEGIN {operation.upper()}")
    results = try_encrypt_ciphers(text, key) if operation == "encrypt" else try_decrypt_ciphers(text, key)
    for cipher, result in results.items():
        lf.failure(f"{operation.capitalize()} using {cipher} => {result}") if "fail" in result else lf.success(f"{operation.capitalize()} using {cipher} => {result}")
    lf.warning(f"{operation.upper()} END")

#? ### MISC ###

def read_from_txt(file_name):
    """Reads content from a text file and returns it as a string."""
    script_directory = os.path.dirname(os.path.abspath(__file__))
    sub_directory = os.path.dirname(script_directory)
    main_directory = os.path.dirname(sub_directory)
    file_path = os.path.join(main_directory, file_name)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def multi_prompt(options,msg):
    prompt_option = prompt({"message": f"{msg}: ",
        "type": "fuzzy",
        "choices": options})
    return prompt_option[0]

def get_text_from_source(msg,file_names,target_folder):
    lf.processing("Read via file or text?")
    source = multi_prompt(["From file","From text"],"Options")
    if source == "From file":
        target_file_name = multi_prompt(file_names, "Target file name")
        return read_from_txt(os.path.join(target_folder, target_file_name))
    return lf.question(msg)

def exit_with_countdown(console,seconds=3):
    for i in range(seconds, 0, -1):
        console.print(f"Exiting program in {i}...", end="\r", style="red")
        sleep(1)
    os.system('cls')
    exit()
