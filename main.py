from scripts.system import *
from scripts.ciphers import *

import scripts.system.log_format as lf

from pyfiglet import Figlet
from rich.traceback import install
install()

# term-image
# textual


def main():
    #! INITIAL SETUP #
    console = Console()
    f = Figlet()
    target_folder = "default"
    try:
        directory = os.path.abspath(target_folder)
        os.makedirs(directory, exist_ok=True)  # Ensure the directory exists
    except:
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), target_folder))
        os.makedirs(directory, exist_ok=True)
    tree = make_dir_tree(directory)
    file_names = walk_directory(pathlib.Path(directory), tree)

    #! MAIN FUNCTIONS #
    def handle_crypto():
            cry_choice = multi_prompt(["Encrypt text","Decrypt text","Back"],"Options")
            if cry_choice == "Back":
                return
            text = get_text_from_source("Ciphertext: "if cry_choice == "Decrypt text" else "Plaintext: ",file_names,target_folder)
            key = get_text_from_source("Key: ",file_names,target_folder)
            lf.warning("INPUT READ")
            lf.datain(f"Ciphertext: {text}") if cry_choice == "Decrypt text" else lf.datain(f"Plaintext: {text}")
            lf.datain(f"Key: {key}")
            execute_ciphers("encrypt" if cry_choice == "Encrypt text" else "decrypt", text, key)

    def handle_file_analysis():
        pass

    def handle_option_3():
        pass

    def handle_option_4():
        pass

    def handle_settings():
        pass

    def exit_program():
        exit_with_countdown(console)

    def back_to_main():
        os.system('cls')
        return main()
    
    #! MENU ACTIONS #
    menu_actions = {
        "1": lambda: handle_crypto(),
        "2": lambda: handle_file_analysis(),
        "3": lambda: handle_option_3(),
        "4": lambda: handle_option_4(),
        "5": lambda: handle_settings(),
        "6": lambda: exit_program(),
        "clr": lambda: back_to_main()
    }

    #! MAIN LOOP #
    console.print(f.renderText('CTF Basics'))
    console.print(f"[yellow]Current target folder:[/yellow] {target_folder}")
    console.print(tree)
    console.print("\nOptions\n\
    1. [green]Cryptography[/green]\n\
    2. [yellow]File Analysis[/yellow]\n\
    3. [violet]?[/violet]\n\
    4. [magenta]?[/magenta]\n\
    5. [cyan]Change settings[/cyan]\n\
    6. [red]Exit[/red]\n\
    Input 'clr' to clear console\n")
    while True:
        choice = input("Input: ")
        menu_actions.get(choice, lambda: None)()

if __name__ == "__main__":
    main()