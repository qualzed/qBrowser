import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineCore import QWebEngineProfile
from pathlib import Path

CookiesPath = Path.cwd().joinpath("user", "savedata").resolve()

def initCookie():
    profile = QWebEngineProfile.defaultProfile()
    profile.setPersistentStoragePath(str(CookiesPath))
    profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)