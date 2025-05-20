import io
from rich.console import Console
import log_format as log_format

def test_function(func, text, expected_value):
    console_output = io.StringIO()
    console = Console(file=console_output, force_terminal=True)
    func(text, console)
    output = console_output.getvalue().strip()

    if output == expected_value:
        print(f"Test Passed: {output}")
    else:
        print(f"Test Failed: Expected '{expected_value}', but got '{output}'")

def run_tests():
    test_cases = [
        (log_format.success, "Success Message", "[+] Success Message"),
        (log_format.failure, "Failure Message", "[-] Failure Message"),
        (log_format.question, "Question Message", "[?] Question Message"),
        (log_format.warning, "Warning Message", "[!] Warning Message"),
        (log_format.processing, "Processing Message", "[*] Processing Message"),
        (log_format.approx, "Approx Message", "[~] Approx Message"),
        (log_format.user, "User Message", "[@] User Message"),
        (log_format.progress, "Progress Message", "[%] Progress Message"),
        (log_format.comment, "Comment Message", "[#] Comment Message"),
        (log_format.dataout, "Data Output", "[>] Data Output"),
        (log_format.datain, "Data Input", "[<] Data Input"),
        (log_format.fatal, "Fatal Error", "[X] Fatal Error"),
        (log_format.finalok, "Final OK", "(OK) Final OK"),
        (log_format.finalstop, "Final Stop", "(FAIL) Final Stop"),
    ]
    
    for func, text, value in test_cases:
        test_function(func, text, value)

if __name__ == "__main__":
    run_tests()