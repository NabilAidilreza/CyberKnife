import requests
from datetime import datetime
from typing import List
import scripts.system.log_format as lf
from scripts.system.general_funcs import multi_prompt

#! Wayback Machine 
def get_all_snapshots(url: str, from_year: int = 2000, to_year: int = datetime.now().year) -> List[str]:
    """
    Get all snapshots of a URL from the Wayback Machine.
    Returns a list of archive URLs.
    """
    cdx_url = "http://web.archive.org/cdx/search/cdx"
    params = {
        "url": url,
        "from": from_year,
        "to": to_year,
        "output": "json",
        "fl": "timestamp,original",
        "collapse": "timestamp:6"
    }
    lf.processing("Fetching data...")
    response = requests.get(cdx_url, params=params)
    if response.status_code != 200:
        lf.fatal(f"Error: Received status {response.status_code}")
        return []

    data = response.json()
    if len(data) <= 1:
        lf.failure("No snapshots found.")
        return []

    snapshots = [
        f"https://web.archive.org/web/{entry[0]}/{entry[1]}"
        for entry in data[1:]
    ]
    lf.finalok("Success: Received status 200")
    return snapshots

def print_snapshots(snapshots: List[str]):
    lf.success(f"Found {len(snapshots)} snapshots:")
    cn = lf.question("Print all? (Y/n): ")
    if cn.upper() == "Y":
        for snap in snapshots:
            lf.print(snap)
    else:
        lf.print(snapshots[0])

def handle_osint():
    choice = multi_prompt(["Wayback Machine", "Back"], "Options")
    if choice == "Back":
        return
    if choice == "Wayback Machine":
        wb_target_url = lf.question("Target url: ")
        snapshots = get_all_snapshots(wb_target_url)
        print_snapshots(snapshots)  



# Operator	Purpose	Example
# site:	Restrict search to a domain or site	site:example.com
# filetype:	Search specific file types	filetype:txt or filetype:pdf
# inurl:	URLs containing a specific string	inurl:flag or inurl:secret
# intitle:	Page title contains a word	intitle:"index of"
# intext:	Search for text within page content	intext:"flag{" or intext:"CTF{"
# cache:	View cached version of a page	cache:example.com/secret
# -	Exclude terms	site:example.com -inurl:login
# OR	Combine queries	filetype:txt OR filetype:log