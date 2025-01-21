from rich.traceback import install

install()

def success(text,console):
    console.print("[bright_green][+] " + text + "[/bright_green]")

def failure(text,console):
    console.print("[bright_red][-] " + text + "[/bright_red]")

def question(text,console):
    console.print("[turquoise2][?] " + text + "[/turquoise2]")

def warning(text,console):
    console.print("[yellow][!] " + text + "[/yellow]")

def processing(text,console):
    console.print("[bright_magenta][*] " + text + "[/bright_magenta]")

def approx(text,console):
    console.print("[dark_red][~] " + text + "[/dark_red]")

def user(text,console):
    console.print("[purple]\[@] " + text + "[/purple]")

def progress(text,console):
    console.print("[green][%] " + text + "[/green]")

def comment(text,console):
    console.print(f"[bright_black]\[#] " + text + "[/bright_black]")

def dataout(text,console):
    console.print("[cyan][>] " + text + "[/cyan]")

def datain(text,console):
    console.print("[blue][<] " + text + "[/blue]")

def fatal(text,console):
    console.print("[bright_red][X] " + text + "[/bright_red]")

def finalok(text,console):
    console.print("[bright_green](OK) " + text + "[/bright_green]")

def finalstop(text,console):
    console.print("[bright_red](FAIL) " + text + "[/bright_red]")

