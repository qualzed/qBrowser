import requests, os
from header import msg

def CHECK_UPDATE():
    response = requests.get("https://raw.githubusercontent.com/qualzed/qBrowser/refs/heads/main/version.txt")
    response.raise_for_status()
    github_version = response.text.strip()
    if(str(msg.CURRENT_VERSION) != str(github_version)):
        os.system("cls")
        print(msg.UPDATE_TEXT)