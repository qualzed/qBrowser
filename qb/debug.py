import os

debug_bool = False
debug_version = 1 # 1 - Source code Version, 2 - Builded Version

section = """
________________
"""

paths = {
    1: "main.py",
    2: "qBrowser.exe"
}

def debug(msg: str, *var: str): # * for endless args
    if debug_bool:
        print(f"{section}\nDEBUG: {msg} | {var}{section}\n")

def DebugSwitch(state: bool):
    if(state):
        os.system(f"start cmd /c {paths[debug_version]} --debug")
    else:
        os.system(f"start {paths[debug_version]}") # With source code it will open console

    exit(0) # Close previous window cause new window was created