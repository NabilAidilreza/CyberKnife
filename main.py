import time
import scripts.system.log_format as lf
from scripts.system import *
from scripts.ciphers import *
from rich.prompt import Prompt
from rich.panel import Panel
from rich.progress import track
from rich.traceback import install
install()

version = "1.0"


console = Console()

def setup():
    global version
    boot_msgs = [
        "[green]Initializing core modules...[/]",
        "[green]Loading memory blocks...[/]",
        "[green]Patching kernel exploits...[/]",
        "[green]Spoofing MAC address...[/]",
        "[green]Bypassing authentication...[/]",
        "[green]Access granted.[/]",
    ]
    console.print(Panel.fit(f"CyberKnife v{version} - Python Multitool for CTFs", title="[bold cyan]Initializer", border_style="bright_blue"))
    for msg in boot_msgs:
        console.print(msg)
        time.sleep(0.3)
    
    console.print("\n[bold green]Boot sequence complete.[/]\n")
    time.sleep(1)

def core():
    #! INITIAL SETUP #
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
        lf.warning("GET TEXT")
        text = get_text_from_source("Ciphertext: "if cry_choice == "Decrypt text" else "Plaintext: ",file_names,target_folder)
        lf.warning("GET KEY")
        key = get_text_from_source("Key: ",file_names,target_folder)
        lf.warning("INPUT READ")
        lf.datain(f"Ciphertext: {text}") if cry_choice == "Decrypt text" else lf.datain(f"Plaintext: {text}")
        lf.datain(f"Key: {key}")
        if text != None or key != None:
            execute_ciphers("encrypt" if cry_choice == "Encrypt text" else "decrypt", text, key)

    def forensics():
        foren_choice = multi_prompt(["Hex Viewer","EXIF Image","Back"],"Options")
        match foren_choice:
            case "Back":
                return
            case "Hex Viewer":
                hex_reader(file_names,target_folder)
            case "EXIF Image":
                exif_tool(file_names,target_folder)

    def osint():
        pass

    def misc():
        misc_choice = multi_prompt(["Extract Text From Image","Back"],"Options")
        match misc_choice:
            case "Back":
                return
            case "Extract Text From Image":
                extract_text_from_image()

    def delete_file():
        settings_choice = multi_prompt(["Delete file","Back"],"Options")
        match settings_choice:
            case "Back":
                return
            case "Delete file":
                delete_selected_file(file_names,target_folder)

    def exit_program():
        exit_with_countdown(console)

    def back_to_main():
        os.system('cls')
        return main()
    
    #! MENU ACTIONS #
    options = {
        "1": {
            "title": "Cryptography",
            "color":"green",
            "action": lambda: handle_crypto()
        },
        "2": {
            "title": "Forensics",
            "color":"yellow",
            "action": lambda: forensics()
        },
        "3": {
            "title": "OSINT",
            "color":"violet",
            "action": lambda: osint()
        },
        "4": {
            "title": "Misc",
            "color":"magenta",
            "action": lambda: misc()
        },
        "5": {
            "title": "Delete file",
            "color":"cyan",
            "action": lambda: delete_file()
        },
        "6": {
            "title": "Exit",
            "color":"red",
            "action": lambda: exit_program()
        },
        "clr": {
            "title": "Input 'clr' to clear console",
            "color":"yellow",
            "action": lambda: back_to_main()
        }
    }
    return target_folder, tree, options

def menu(target_folder, tree, options):
    #! MAIN LOOP #
    console.print(f"[green]Current target folder:[/green] {target_folder}")
    console.print(tree)
    console.print("\n[bold green]Available Modules:[/]")
    for key, dict in options.items():
        color = dict["color"]
        title = dict["title"]
        console.print(f"[{color}]{key}[/{color}]: {title}")

    while True:
        choice = Prompt.ask("\n[bold green]Select an option[/]", choices=options.keys(), default="5")
        options[choice]["action"]()

def main():
    setup()
    a,b,c=core()
    menu(a,b,c)

if __name__ == "__main__":
    main()