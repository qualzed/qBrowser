from pypresence import Presence
import os, time
from qb.core import *
from qb import debug

client_id = ""
RPC = Presence(client_id)
RPC.connect()

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

def on_rpc_changed(rpc_text):
    if(rpc_text == "RPC (On)"):
        set_rpc(True)
        StartRPC()
        if(debug.debug_bool): print(f"RPC: RPC ON | {rpc_text=} ")
    else:
        set_rpc(False)
        if(debug.debug_bool): print(f"RPC: RPC OFF | {rpc_text=}")

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