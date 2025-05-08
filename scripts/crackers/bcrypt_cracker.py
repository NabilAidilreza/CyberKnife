import re
import bcrypt
from multiprocessing import Event, Manager
from concurrent.futures import ProcessPoolExecutor, as_completed

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
