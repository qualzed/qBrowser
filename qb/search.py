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

NationalDomain = [
    ".ru", ".рф", ".su", ".com", ".info", ".ua", ".site", 
    ".ac", ".ad", ".ae", ".af", ".ag", ".ai", ".al", ".am", ".ao", ".aq", ".ar", ".as", ".at", ".au", ".aw", ".ax", ".az",
    ".ba", ".bb", ".bd", ".be", ".bf", ".bg", ".bh", ".bi", ".bj", ".bm", ".bn", ".bo", ".br", ".bs", ".bt", ".bw", ".by", ".bz",
    ".ca", ".cc", ".cd", ".cf", ".cg", ".ch", ".ci", ".ck", ".cl", ".cm", ".cn", ".co", ".cr", ".cu", ".cv", ".cw", ".cx", ".cy", ".cz",
    ".de", ".dj", ".dk", ".dm", ".do", ".dz",
    ".ec", ".ee", ".eg", ".er", ".es", ".et", ".eu",
    ".fi", ".fj", ".fk", ".fm", ".fo", ".fr",
    ".ga", ".gd", ".ge", ".gf", ".gg", ".gh", ".gi", ".gl", ".gm", ".gn", ".gp", ".gq", ".gr", ".gs", ".gt", ".gu", ".gw", ".gy",
    ".hk", ".hm", ".hn", ".hr", ".ht", ".hu",
    ".id", ".ie", ".il", ".im", ".in", ".io", ".iq", ".ir", ".is", ".it",
    ".je", ".jm", ".jo", ".jp",
    ".ke", ".kg", ".kh", ".ki", ".km", ".kn", ".kp", ".kr", ".kw", ".ky", ".kz",
    ".la", ".lb", ".lc", ".li", ".lk", ".lr", ".ls", ".lt", ".lu", ".lv", ".ly",
    ".ma", ".mc", ".md", ".me", ".mg", ".mh", ".mk", ".ml", ".mm", ".mn", ".mo", ".mp", ".mq", ".mr", ".ms", ".mt", ".mu", ".mv", ".mw", ".mx", ".my", ".mz",
    ".na", ".nc", ".ne", ".nf", ".ng", ".ni", ".nl", ".no", ".np", ".nr", ".nu", ".nz",
    ".om",
    ".pa", ".pe", ".pf", ".pg", ".ph", ".pk", ".pl", ".pm", ".pn", ".pr", ".ps", ".pt", ".pw", ".py",
    ".qa",
    ".re", ".ro", ".rs", ".rw",
    ".sa", ".sb", ".sc", ".sd", ".se", ".sg", ".sh", ".si", ".sk", ".sl", ".sm", ".sn", ".so", ".sr", ".st", ".sv", ".sy", ".sz",
    ".tc", ".td", ".tf", ".tg", ".th", ".tj", ".tk", ".tl", ".tm", ".tn", ".to", ".tr", ".tt", ".tv", ".tw", ".tz",
    ".ug", ".uk", ".us", ".uy", ".uz",
    ".va", ".vc", ".ve", ".vg", ".vi", ".vn", ".vu",
    ".wf", ".ws",
    ".ye", ".yt",
    ".za", ".zm", ".zw",
    ".бел", ".қаз", ".мон", ".срб", ".укр", ".бг", ".мкд", ".рус", ".онлайн", ".сайт", ".орг"
]

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

def IsDomain(query: str):
    if any(domain in query for domain in NationalDomain): # Check domain in the query
        return True
    return False
    
# GetSearchEngineName(0)
# SearchEngineList()