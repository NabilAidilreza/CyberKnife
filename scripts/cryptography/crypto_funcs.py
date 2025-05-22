import os
import importlib
from scripts.system import lf, multi_prompt, get_text_from_source, get_bool
from time import sleep

from .freq_analysis import *

#* ### Cryptography ###
def try_decrypt_ciphers(ciphertext, flag_format,key=None):
    results = {}
    for module_name in os.listdir('scripts/ciphers'):
        if module_name.endswith('.py') and module_name != '__init__.py':
            cipher_name = module_name[:-3]  # Remove .py extension
            try:
                cipher_module = importlib.import_module(f'scripts.ciphers.{cipher_name}')
                # Call the decryption function dynamically
                if hasattr(cipher_module, 'decrypt'):
                    decrypted_text = cipher_module.decrypt(ciphertext,flag_format,key)
                    results[cipher_name] = decrypted_text
            except Exception as e:
                results[cipher_name] = f"fail => {str(e)}"
    return results

def try_encrypt_ciphers(plaintext,key=None):
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

def execute_ciphers(operation, text,flag_format, key):
    lf.warning(f"ATTEMPTING {operation.upper()}ION")
    results = try_encrypt_ciphers(text, key) if operation == "encrypt" else try_decrypt_ciphers(text,flag_format, key)
    for cipher, result in results.items():
        sleep(0.1)
        lf.failure(f"{operation.capitalize()} using {cipher} => {result}") if "fail" in result else lf.success(f"{operation.capitalize()} using {cipher} => {result}")
    lf.warning(f"{operation.upper()}ION END")


def handle_crypto(file_names, target_folder,flag_format):
    choice = multi_prompt(["Encryption", "Decryption", "Frequency Analysis", "Back"], "Options")
    if choice == "Back":
        return

    if choice == "Frequency Analysis":
        lf.warning("GET CIPHERTEXT")
        text = get_text_from_source("Ciphertext: ", file_names, target_folder)
        lf.datain(text)
        lf.warning("CLOSE WINDOW TO CONTINUE...")
        output = frequency_analysis_graph(text)
        show_freq_output(output)
        return

    lf.warning("GET TEXT")
    text = get_text_from_source("Ciphertext: " if choice == "Decryption" else "Plaintext: ", file_names, target_folder)
    lf.warning("GET KEY")
    key = get_text_from_source("Key: ", file_names, target_folder) if get_bool("Have a key?: ") else ""

    lf.warning("INPUT READ")
    lf.datain(f"{'Ciphertext' if choice == 'Decryption' else 'Plaintext'}: {text}")
    lf.datain(f"Key: {key}")

    if text or key:
        execute_ciphers("encrypt" if choice == "Encryption" else "decrypt", text, flag_format, key)