import os
import importlib
import scripts.system.log_format as lf
from time import sleep

from .freq_analysis import *

#* ### Cryptography ###
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
    lf.warning(f"ATTEMPTING {operation.upper()}ION")
    results = try_encrypt_ciphers(text, key) if operation == "encrypt" else try_decrypt_ciphers(text, key)
    for cipher, result in results.items():
        sleep(0.1)
        lf.failure(f"{operation.capitalize()} using {cipher} => {result}") if "fail" in result else lf.success(f"{operation.capitalize()} using {cipher} => {result}")
    lf.warning(f"{operation.upper()}ION END")