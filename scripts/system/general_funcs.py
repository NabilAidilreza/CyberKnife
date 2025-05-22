import os
import scripts.system.log_format as lf
from time import sleep
from InquirerPy import prompt
from PIL import Image

#! Hub for Main Functions #

#? ### GENERAL ###

def is_valid_image_pil(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()  # Verify if it's an actual image
        return True
    except (IOError, SyntaxError):
        return False

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

def get_bool(question):
    lf.processing(question)
    source = multi_prompt(["Yes","No"],"Options")
    if source == "No":
        return False
    return True

def get_string(title,question):
    lf.processing(title)
    data = lf.question(question)
    return data

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
    
def delete_selected_file(file_names,target_folder):
    target_file_name = multi_prompt(file_names, "Target file name")
    file_path = os.path.join(target_folder, target_file_name)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            lf.success(f"File '{target_file_name}' has been deleted successfully.")
        except Exception as e:
            lf.failure(f"Error deleting file '{target_file_name}': {e}")
    else:
        lf.fatal(f"File '{target_file_name}' does not exist in the target folder.")

def handle_exit_with_countdown(console,seconds=3):
    for i in range(seconds, 0, -1):
        console.print(f"Exiting program in {i}...", end="\r", style="red")
        sleep(1)
    os.system('cls')
    exit()

def handle_delete_file(file_names, target_folder):
    if multi_prompt(["Delete file", "Back"], "Options") == "Delete file":
        delete_selected_file(file_names, target_folder)
