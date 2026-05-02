import os
from qb.core import *

MAX_TABS = 25

def SaveTabs(TAB_HISTORY_STRING: str):
    os.makedirs(os.path.dirname(TAB_HISTORY_PATH), exist_ok=True)
    with open(f"{TAB_HISTORY_PATH}", "w+", encoding="utf-8") as tab_file:
        tab_file.write(TAB_HISTORY_STRING)

def ReadTabs():
    os.makedirs(os.path.dirname(TAB_HISTORY_PATH), exist_ok=True)
    if os.path.exists(TAB_HISTORY_PATH):
        with open(TAB_HISTORY_PATH, "r", encoding="utf-8") as f:
            links = [line.strip() for line in f if line.strip()]
            return links if links else None
    return None