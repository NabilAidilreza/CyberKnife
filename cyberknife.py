import os
import pathlib
import json

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
from scripts.web import *
from scripts.misc import *

install()
version = "1.0"

#! Menu
#? Cryptography
# Encryption
# Decryption
# Freq Analysis
#? Forensics
# EXIF Tool
# Hex View
# Text Extract
# PNG BruteForce Dimensions
#? OSINT
# Wayback Machine
# Reverse Search Image
# Acct Finder
#? Crackers
# Bcrypt Cracker
#? Web
# Domain Enumeration Tool
#? Misc
# Netcat
# Bin/Decimal/Hex to ASCII
# Flag Finder

CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"flag_format": "???"}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

config = load_config()
flag_format = config.get("flag_format")
target_folder_path = config.get("target_folder_path")

console = Console()

def setup():
    console.print(Panel.fit(
        f"CyberKnife v{version} - Python Multitool for CTFs", 
        title="[bold cyan]Initializer", 
        border_style="bright_blue"
    ))

def initialize_directory(target_folder="default"):
    try:
        directory = os.path.abspath(target_folder)
        os.makedirs(directory, exist_ok=True)
    except Exception:
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), target_folder))
        os.makedirs(directory, exist_ok=True)

    tree = make_dir_tree(directory)
    file_names = walk_directory(pathlib.Path(directory), tree)
    return target_folder, tree, file_names

def handle_flag_format():
    global flag_format, config
    choice = multi_prompt(["Change", "Back"], "Options")
    if choice == "Back":
        return
    new_flag_format = get_string("GET FLAG FORMAT", "New flag format? (i.e CDDC2025): ")
    flag_format = new_flag_format
    config["flag_format"] = flag_format
    save_config(config)
    lf.success(f"Flag format set to {flag_format}")

def exit_program():
    handle_exit_with_countdown(console)

def clear_screen_and_restart():
    os.system('cls' if os.name == 'nt' else 'clear')
    main()

def show_menu_options(options):
    console.print("\n[bold green]Available Modules:[/]")
    for key, opt in options.items():
        title = opt["title"]() if callable(opt["title"]) else opt["title"]
        console.print(f"[{opt['color']}]{key}[/{opt['color']}]: {title}")

def core(target_folder_path):
    target_folder, tree, file_names = initialize_directory(target_folder_path)
    options = {
        "0": {"title": lambda: f"Flag Format => {flag_format}", "color": "white", "action": handle_flag_format},
        "1": {"title": "Cryptography", "color": "green", "action": lambda: handle_crypto(file_names, target_folder)},
        "2": {"title": "Forensics", "color": "yellow", "action": lambda: handle_forensics(file_names, target_folder)},
        "3": {"title": "OSINT", "color": "violet", "action": handle_osint},
        "4": {"title": "Crackers", "color": "magenta", "action": lambda: handle_crackers(file_names, target_folder)},
        "5": {"title": "Web", "color": "violet", "action": handle_web},
        "6": {"title": "Misc", "color": "violet", "action": lambda: handle_misc(file_names, target_folder)},
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
    global flag_format, target_folder_path
    setup()
    target_folder, tree, options = core(target_folder_path)
    menu(target_folder, tree, options)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Program interrupted by user.")
        input("Press Enter to exit...")
