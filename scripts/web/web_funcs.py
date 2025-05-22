import requests
import socket
import time

import scripts.system.log_format as lf
from scripts.system.general_funcs import multi_prompt

def get_subdomains(domain: str) -> list:
    """
    Queries crt.sh for subdomains using the certificate transparency log.
    Returns a list of unique subdomains.
    """
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    lf.datain(f"Fetching subdomains for: {domain}")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            subdomains = {entry['name_value'].strip() for entry in data}
            cleaned = set()
            for sub in subdomains:
                if "\n" in sub:
                    cleaned.update(sub.splitlines())
                else:
                    cleaned.add(sub)
            return sorted(cleaned)
        else:
            lf.fatal(f"Error {response.status_code} from crt.sh")
    except Exception as e:
        lf.warning(f"Request failed: {e}")
    return []

def resolve_subdomains(subdomains: list) -> list:
    """
    Attempts DNS resolution to check if the subdomains are live.
    """
    alive = []
    lf.datain("Resolving subdomains...\n")
    for sub in subdomains:
        try:
            ip = socket.gethostbyname(sub)
            lf.success(f"{sub} --> {ip}")
            alive.append((sub, ip))
            time.sleep(0.2)  # polite delay
        except socket.gaierror:
            lf.failure(f"{sub} not resolved.")
    return alive

def urlscan_lookup(domain: str):
    headers = {"Content-Type": "application/json"}
    search_url = f"https://urlscan.io/api/v1/search/?q=domain:{domain}"
    try:
        r = requests.get(search_url, headers=headers, timeout=10)
        results = r.json()
        for item in results.get("results", []):
            lf.print(f"🌐 URLScan result: {item.get('page', {}).get('url')}")
    except Exception as e:
        lf.fatal(f"URLScan lookup failed: {e}")

def check_web_domains(domain):
    subs = get_subdomains(domain)
    live = resolve_subdomains(subs)
    lf.success(f"Found {len(live)} live subdomains out of {len(subs)} total\n")
    urlscan_lookup(domain)

def handle_web():
    choice = multi_prompt(["Domain Enumeration Tool","Back"], "Options")
    if choice == "Back":
        return
    if choice == "Domain Enumeration Tool":
        target_domain = lf.question("Target domain: ")
        check_web_domains(target_domain)



