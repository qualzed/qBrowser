import requests, os
from header import msg

def NEW_VERSION_AVIABLE():
    response = requests.get("https://raw.githubusercontent.com/qualzed/qBrowser/refs/heads/main/version.txt")

    response.raise_for_status()
    github_version = response.text.strip()

    if(str(msg.CURRENT_VERSION) != str(github_version)):
        return True
    
    return False