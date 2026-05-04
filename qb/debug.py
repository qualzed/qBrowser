import os

debug_bool = False
debug_version = 1 # 1 - Source code Version, 2 - Builded Version

paths = {
    1: "main.py",
    2: "qBrowser.exe"
}

def DebugSwitch(state: bool):
    if(state):
        os.system(f"start cmd /c {paths[debug_version]} --debug")
    else:
        os.system(f"start {paths[debug_version]}") # With source code it will open console

    exit(0) # Close previous window cause new window was created