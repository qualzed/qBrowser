import os
from qb.core import *
from qb import debug

SearchEngine = {
    0: ("Google", "https://google.com"),
    1: ("DuckDuckGo", "https://duckduckgo.com"),
    2: ("Yandex", "https://yandex.ru"),
    3: ("SearXNG", "https://searxng.org"),
    4: ("Brave", "https://search.brave.com"),
    5: ("Bing", "https://bing.com")
}

def SearchEngineList():
    for i in range(len(SearchEngine)):
        print(SearchEngine[i][0]) # Search Engine Names
        print(SearchEngine[i][1]) # Search Engine Links

def GetSearchEngineName(SearchEngineIndex): # Using index
    engineName = SearchEngine[int(SearchEngineIndex)][0]
    return engineName

def GetSearchEngineIndex(SearchEngineName: str):
    for i in range(len(SearchEngine)):
        if(SearchEngine[i][0] == SearchEngineName):
            return i

def GetCurrentSearchEngine(type: int): # 0 - ID, 1 - NAME, 2 - LINK
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("search"):
                    CFG_SEARCHENGINE = line.strip().split("=", 1)[1]
                    if(type == 1):
                        SearchEngineName: str = GetSearchEngineName(CFG_SEARCHENGINE)
                        return SearchEngineName
                    if(type == 2):
                        SearchEngineLink: str = SearchEngine[int(CFG_SEARCHENGINE)][1]
                        return SearchEngineLink

    if(type == 1):
        return SearchEngine[0][0]
    if(type == 2):
        return SearchEngine[0][1]
    else:
        return "0"

def SearchEngines():
    return [SearchEngine[i][0] for i in range(len(SearchEngine))]

def set_search(engine):
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    lines = open(config_path, 'r', encoding='utf-8').readlines() if os.path.exists(config_path) else ['']
    lines[3] = f"search={engine}\n"
    with open(config_path, 'w', encoding='utf-8') as f: f.writelines(lines)

def on_search_changed(Engine):
    EngineIndex = GetSearchEngineIndex(Engine)
    set_search(EngineIndex)
    if(debug.debug_bool): print(f"SearchEngine | {EngineIndex=}")

# GetSearchEngineName(0)
# SearchEngineList()