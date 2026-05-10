from pypresence import Presence
import os, time
from qb.core import *
from qb import debug

client_id = "1496895954186670102"
RPC = Presence(client_id)
try:
    RPC.connect()
except:
    pass

start_time = time.time()

def get_rpc():
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("rpc"):
                    rpc = line.strip().split("=", 1)[1]
                    return int(rpc)

def set_rpc(rpc: bool):
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    lines = open(config_path, 'r', encoding='utf-8').readlines() if os.path.exists(config_path) else ['']
    lines[4] = f"rpc={int(rpc)}\n"
    with open(config_path, 'w', encoding='utf-8') as f: f.writelines(lines)
    debug.debug("RPC CFG update", config_path, lines)

def on_rpc_changed(rpc_text):
    state = False
    if(rpc_text == "RPC (On)"):
        state = True
        set_rpc(state)
        StartRPC()
    else:
        set_rpc(state)

    debug.debug("RPC", rpc_text, state)

def StartRPC():
    try:
        RPC.update(
            large_image="icon",
            start=start_time,
            details="Life is sunshine and rainbows.",
            buttons=[{"label":"Source Code", "url":"https://github.com/qualzed/qBrowser"}]
        )
    except Exception as e:
        RPC.connect()

def UpdateRPC(text):
    RPC.update(
        large_image="icon",
        start=start_time,
        details=text,
        buttons=[{"label":"Source Code", "url":"https://github.com/qualzed/qBrowser"}]
    )