import os,re
import sys
import socket
import threading

from scripts.system.general_funcs import *

#? ### Misc ###


    
def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("\n[!] Server closed connection.")
                break
            # Force output immediately even if no newline
            sys.stdout.write(data.decode())
            sys.stdout.flush()
        except:
            break

def connect_with_netcat(cmd_string):
    parts = cmd_string.strip().split()
    if len(parts) != 3 or parts[0].lower() != "nc":
        print("[!] Invalid format. Use: nc <host> <port>")
        return

    _, HOST, PORT = parts

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, int(PORT)))
        lf.warning(f"[NEW CONNECTION] {(HOST, int(PORT))} connected")

        # Start thread to listen to server messages
        threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

        while True:
            user_input = input()
            client.sendall(user_input.encode() + b'\n')  # send newline if required
            if user_input.lower() in ['q', 'quit', 'exit']:
                break


    except Exception as e:
        lf.warning(f"Connection error: {e}")
    finally:
        client.close()
        lf.warning("Session Ended")

def auto_ascii(s):
    try:
        s = s.strip().replace(",", " ").replace("0x", "").lower()
        parts = s.split()
        if all(set(p) <= {'0', '1'} and len(p) == 8 for p in parts):  # binary
            output = ''.join(chr(int(b, 2)) for b in parts)
        elif all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):  # decimal
            output = ''.join(chr(int(d)) for d in parts)
        elif all(len(p) == 2 and all(c in "0123456789abcdef" for c in p) for p in parts):  # hex
            output = ''.join(chr(int(h, 16)) for h in parts)
        else:
            lf.warning("Could not detect format.")
        if output:
            flag = re.search(r'CDDC2025\{.*?\}', output)
            lf.success("Flag found: " + flag.group(0)) if flag else lf.dataout(output)
    except Exception as e:
        lf.failure(e)

def find_flag_in_file(path,flag_format):
    try:
        with open(path, 'rb') as f:
            data = f.read().decode('utf-8', 'ignore')
        m = re.search(fr'{flag_format}\{{.*?\}}', data)
        lf.success("Flag found: " + m.group(0)) if m else lf.failure("No flag(s) in sight...")
        return m.group(0) if m else  ''
    except Exception as e:
        lf.warning(f"Error: {e}")
        return ''

def find_flags_in_folder(folder_path,flag_format):
    results = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            path = os.path.join(root, file)
            flag = find_flag_in_file(path,flag_format)
            if flag:
                results.append(f"{path}: {flag}")
    lf.success(str(results)) if results!=[] else lf.failure("No flags found.")