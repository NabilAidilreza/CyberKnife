import os
import time
import pathlib

from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.traceback import install

import scripts.system.log_format as lf
from scripts.system import *
from scripts.ciphers import *
from scripts.cryptography import *
from scripts.forensics import *
from scripts.osint import *
from scripts.crackers import *

install()
console = Console()
version = "1.0"

#! Menu
#? Cryptography
# Decoder Bin/Hex/Base64
# Encryption
# Decryption add in flag format
# Freq Analysis
#? Forensics
# EXIF Tool
# Hex View
# Text Extract
# Aperisolve
# Wireshark
#? OSINT
# Wayback Machine
# Reverse Search Image
# Acct Finder
#? Crackers
# Bcrypt Cracker
#? Attack Vectors
#? Misc
# Connect via netcat

def setup():
    console.print(Panel.fit(
        f"CyberKnife v{version} - Python Multitool for CTFs", 
        title="[bold cyan]Initializer", 
        border_style="bright_blue"
    ))

    boot_msgs = [
        "[green]Loading scripts...[/]",
        "[green]Loading main menu...[/]"
    ]

    for msg in boot_msgs:
        console.print(msg)
        time.sleep(0.1)

    console.print("\n[bold green]Boot sequence complete.[/]\n")
    time.sleep(1)

def initialize_directory(target_folder="default"):
    try:
        directory = os.path.abspath(target_folder)
        os.makedirs(directory, exist_ok=True)
    except:
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), target_folder))
        os.makedirs(directory, exist_ok=True)
    
    tree = make_dir_tree(directory)
    file_names = walk_directory(pathlib.Path(directory), tree)
    return target_folder, tree, file_names

def handle_crypto(file_names, target_folder):
    cry_choice = multi_prompt(["Encryption", "Decryption", "Frequency Analysis", "Back"], "Options")
    if cry_choice == "Back":
        return

    if cry_choice == "Frequency Analysis":
        lf.warning("GET CIPHERTEXT")
        text = get_text_from_source("Ciphertext: ", file_names, target_folder)
        lf.datain(text)
        lf.warning("CLOSE WINDOW TO CONTINUE...")
        output = frequency_analysis_graph(text)
        show_freq_output(output)
        return

    lf.warning("GET TEXT")
    text = get_text_from_source("Ciphertext: " if cry_choice == "Decryption" else "Plaintext: ", file_names, target_folder)
    lf.warning("GET KEY")
    key = get_text_from_source("Key: ", file_names, target_folder) if get_bool("Have a key?: ") else ""

    lf.warning("INPUT READ")
    lf.datain(f"{'Ciphertext' if cry_choice == 'Decryption' else 'Plaintext'}: {text}")
    lf.datain(f"Key: {key}")

    if text or key:
        execute_ciphers("encrypt" if cry_choice == "Encryption" else "decrypt", text, key)

def handle_forensics(file_names, target_folder):
    choice = multi_prompt(["Hex Viewer", "EXIF Image", "Text Image Extract", "Back"], "Options")
    match choice:
        case "Hex Viewer":
            hex_reader(file_names, target_folder)
        case "EXIF Image":
            exif_tool(file_names, target_folder)
        case "Text Image Extract":
            extract_text_from_image()
        case "Back":
            return

def handle_osint():
    # Placeholder for OSINT functionality
    pass

def handle_crackers(file_names, target_folder):
    choice = multi_prompt(["Bcrypt Cracker", "Back"], "Options")
    if choice == "Back":
        return

    if choice == "Bcrypt Cracker":
        lf.warning("GET BCRYPT HASH")
        bcrypt_hash = get_text_from_source("Bcrypt Hash: ", file_names, target_folder)

        if not is_valid_bcrypt(bcrypt_hash):
            lf.fatal("Invalid Bcrypt Hash")
            return

        start = get_string("Start Range", "Enter start of range (i.e 0,100): ")
        end = get_string("End Range", "Enter end of range (i.e 50000,99999): ")

        lf.datain(bcrypt_hash)
        lf.warning("BEGIN SESSION")

        try:
            password = decrypt_bcrypt(bcrypt_hash.encode(), int(start), int(end))
            lf.success(password) if "failed" not in password else lf.failure(password)
        except Exception:
            lf.fatal("Something went wrong...")
        finally:
            lf.warning("SESSION END")
        
def handle_attacks():
    pass

def handle_misc():
    pass

def handle_delete_file(file_names, target_folder):
    if multi_prompt(["Delete file", "Back"], "Options") == "Delete file":
        delete_selected_file(file_names, target_folder)

def exit_program():
    exit_with_countdown(console)

def clear_screen_and_restart():
    os.system('cls' if os.name == 'nt' else 'clear')
    main()

def show_menu_options(options):
    console.print("\n[bold green]Available Modules:[/]")
    for key, opt in options.items():
        console.print(f"[{opt['color']}]{key}[/{opt['color']}]: {opt['title']}")

def core():
    target_folder, tree, file_names = initialize_directory()
    
    options = {
        "1": {"title": "Cryptography", "color": "green", "action": lambda: handle_crypto(file_names, target_folder)},
        "2": {"title": "Forensics", "color": "yellow", "action": lambda: handle_forensics(file_names, target_folder)},
        "3": {"title": "OSINT", "color": "violet", "action": handle_osint},
        "4": {"title": "Crackers", "color": "magenta", "action": lambda: handle_crackers(file_names, target_folder)},
        "5": {"title": "Attack Vectors", "color": "violet", "action": handle_attacks},
        "6": {"title": "Misc", "color": "violet", "action": handle_misc},
        "7": {"title": "Delete file", "color": "cyan", "action": lambda: handle_delete_file(file_names, target_folder)},
        "8": {"title": "Exit", "color": "red", "action": exit_program},
        "clr": {"title": "Input 'clr' to clear console", "color": "yellow", "action": clear_screen_and_restart},
    }

    return target_folder, tree, options

def menu(target_folder, tree, options):
    console.print(f"[green]Current target folder:[/green] {target_folder}")
    console.print(tree)
    show_menu_options(options)

    while True:
        choice = Prompt.ask("\n[bold green]Select an option[/]", choices=options.keys(), default="5")
        options[choice]["action"]()
        show_menu_options(options)

def main():
    setup()
    target_folder, tree, options = core()
    menu(target_folder, tree, options)

if __name__ == "__main__":
    main()
