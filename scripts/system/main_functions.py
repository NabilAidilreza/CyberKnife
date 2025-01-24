import os
import importlib
from time import sleep

from rich.table import Table
from InquirerPy import prompt
import scripts.system.log_format as lf


#* Sub Libraries #
# Cryptography #


# Forensics #
from PIL import Image
from PIL.ExifTags import TAGS


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
    lf.warning(f"ATTEMPTING {operation.upper()}ION")
    results = try_encrypt_ciphers(text, key) if operation == "encrypt" else try_decrypt_ciphers(text, key)
    for cipher, result in results.items():
        sleep(0.1)
        lf.failure(f"{operation.capitalize()} using {cipher} => {result}") if "fail" in result else lf.success(f"{operation.capitalize()} using {cipher} => {result}")
    lf.warning(f"{operation.upper()}ION END")


#? Forensics ###

def hex_reader(file_names,target_folder):
    target_file_name = multi_prompt(file_names,"Choose File")
    file_path = os.path.join(target_folder, target_file_name)
    data = read_from_file(file_path,"rb")

    hex_table = Table(title="")
    hex_table.add_column("Hex Dump",style="green",justify="left")
    hex_table.add_column("Content",style="blue",justify="center")

    def print_hex(data):
        bytes = 0
        line = []
        line_string = ""
        for b in data:
            bytes += 1
            line.append(b)
            line_string += "{0:0{1}x}".format(b,2) + " " 
            if bytes % 16 == 0:
                line_content = ""
                for b2 in line:
                    if (b2 >= 32) and (b2 <= 126):
                        line_content += chr(b2)
                    else:
                        line_content += "*"
                temp = [line_string,line_content]
                hex_table.add_row(*temp)
                line_string=""
                line=[]
        lf.print(hex_table)
    def preview_file(data):
        lf.processing("File Preview")
        print_hex(data[:500])
    preview_file(data)
    lf.warning("Open file in HexEdit for better viewing.\n")

def exif_tool(file_names,target_folder):
    target_file_name = multi_prompt(file_names,"Choose File")
    file_path = os.path.join(target_folder, target_file_name)
    if is_valid_image_pil(file_path):
        image = Image.open(file_path)
        exif_data = image._getexif()
        if exif_data:
            lf.processing("Retrieving EXIF Data...")
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                sleep(0.1)
                lf.print(f"{tag_name}: {value}")
            lf.warning("End of EXIF Data")
        else:
            lf.fatal("No EXIF Metadata!")
    else:
        lf.failure(f"{file_path} is NOT a valid image.")

def is_valid_image_pil(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()  # Verify if it's an actual image
        return True
    except (IOError, SyntaxError):
        return False



#? ### MISC ###

def read_from_file(file_name,mode):
    """Reads content from a text file and returns it as a string."""
    script_directory = os.path.dirname(os.path.abspath(__file__))
    sub_directory = os.path.dirname(script_directory)
    main_directory = os.path.dirname(sub_directory)
    file_path = os.path.join(main_directory, file_name)
    try:
        with open(file_path, mode) as file:
            data = file.read()
            file.close()
            return data
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
        return read_from_file(os.path.join(target_folder, target_file_name),"r")
    return lf.question(msg)

def exit_with_countdown(console,seconds=3):
    for i in range(seconds, 0, -1):
        console.print(f"Exiting program in {i}...", end="\r", style="red")
        sleep(1)
    os.system('cls')
    exit()
