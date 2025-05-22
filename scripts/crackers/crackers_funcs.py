import re
import bcrypt
from multiprocessing import Event, Manager
from concurrent.futures import ProcessPoolExecutor, as_completed

from scripts.system.general_funcs import lf, multi_prompt, get_string, get_text_from_source

# The bcrypt hash to crack
#target_hash = b"$2b$12$gVjkJtERaPrWjfBw0Lu7aOcoIzZzkm1gaO3SLYV8wXL63CHSMnJfC"

def is_valid_bcrypt(hash_str):
    if type(hash_str) == str:
        bcrypt_pattern = r"^\$2[aby]?\$\d{2}\$[./A-Za-z0-9]{53}$"
        return re.match(bcrypt_pattern, hash_str) is not None
    return False

def check_password_range(start, end, hash_to_crack, stop_event):
    print(f"[~] Worker started: checking range {start:05d}-{end-1:05d}")
    for i in range(start, end):
        if stop_event.is_set():
            print(f"[x] Worker stopping early at {i:05d}")
            return None  # Exit early if stop signal is set
        password = f"{i:05d}".encode('utf-8')
        if bcrypt.checkpw(password, hash_to_crack):
            return password.decode()
    return None

def decrypt_bcrypt(target_hash, range_start, range_end, chunk_size=1000):
    found_password = None
    manager = Manager()
    stop_event = manager.Event()

    with ProcessPoolExecutor() as executor:
        futures = []
        for i in range(range_start, range_end, chunk_size):
            print(f"[>] Submitting chunk: {i:05d}-{min(i + chunk_size, range_end) - 1:05d}")
            futures.append(
                executor.submit(check_password_range, i, min(i + chunk_size, range_end), target_hash, stop_event)
            )

        for future in as_completed(futures):
            result = future.result()
            if result:
                found_password = result
                print(f"[+] Password found: {found_password}")
                stop_event.set()  # Signal other workers to stop
                break

    if not found_password:
        print("[-] Password not found in range.")
        found_password = "Cracking failed..."
    return found_password


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
        