import sys
import os
from functools import partial
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QAction, QIcon, QColor
from PyQt6.QtWidgets import QApplication, QColorDialog, QListWidget, QMainWindow, QTabWidget, QComboBox, QWidget, QSizePolicy, QLineEdit, QPushButton, QDialog, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import qInstallMessageHandler, Qt, QTimer
from locales.locale import en, ru
from qb.core import *
from qb.voice import voice
from qb import debug, resolution, tabs, vcheck, search, rpc, args

def message_handler(mode, context, message): # Skip chromium messages
    if "js:" in message or "sandbox" in message:
        pass
    elif " " in message: # Full turned off logs
        pass

qInstallMessageHandler(message_handler)
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-web-security --ignore-certificate-errors"

def get_locale(key): # Checking locale
    global current_language
    locales = {"ru": dict(ru), "en": dict(en)}
    return locales.get(current_language, locales["ru"]).get(key, "не найден")

def get_ui(): # Reading UI
    bg, color, button = "#ffffff", "#000000", "default" 
    with open(ui_path, "r", encoding="utf-8") as f:
        config = dict(line.strip().split("=", 1) for line in f if "=" in line)
        bg = config.get("bg", bg)
        color = config.get("color", color)
        button = config.get("button", button)
    return bg, color, button

def update_ui(): # Update UI after saving
    button_text_color = "#FFFFFF"
    bg, color, button = get_ui()
    if int(button[1:], 16) > int(color[1:], 16): # If the button is white and text white too - it will invert it
        button_text_color = "#000000"
    app.setStyleSheet(f"""
        QWidget {{
            background-color: {bg};
            color: {color};
        }}
        QPushButton {{
            background-color: {button};
            color: {button_text_color};
        }}
    """)

def set_language(lang): # languages
    global current_language
    match lang: 
        case "en": current_language = "en"
        case "ru": current_language = "ru"
        case _: return
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    lines = open(config_path, 'r', encoding='utf-8').readlines() if os.path.exists(config_path) else ['']
    lines[0] = f"language={current_language}\n"
    with open(config_path, 'w', encoding='utf-8') as f: f.writelines(lines)

def set_resolution(x, y): # Save resolution to qb\qb.cfg
    lines = open(config_path, 'r', encoding='utf-8').readlines() if os.path.exists(config_path) else ['']
    lines[1] = f"x={x}\n"
    lines[2] = f"y={y}\n"
    with open(config_path, 'w', encoding='utf-8') as f: f.writelines(lines)

def set_ui(bg, color, button): # set UI function
    lines = open(ui_path, 'r', encoding='utf-8').readlines() if os.path.exists(ui_path) else ['']
    lines[0] = f"bg={bg}\n"
    lines[1] = f"color={color}\n"
    lines[2] = f"button={button}\n"
    with open(ui_path, 'w', encoding='utf-8') as f: f.writelines(lines)

def get_current_language(): # getting current language
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("language="):
                    return line.strip().split("=", 1)[1]
    return "ru"

def get_current_resolution(): # get current resolution and save
    x, y = "400", "200" # Default resolution
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("x="):
                    x = line.strip().split("=", 1)[1]
                if line.startswith("y="):
                    y = line.strip().split("=", 1)[1]
    return int(x), int(y)

class SettingsWindow(QDialog): # Settings UI menu
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(get_locale("settings") if get_locale("settings") != "не найден" else "Settings")
        self.setGeometry(200, 200, 300, 200)
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        language_label = QLabel("Language:")
        layout.addWidget(language_label)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Русский"])
        self.language_combo.setCurrentText("Русский" if current_language == "ru" else "English")
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        layout.addWidget(self.language_combo)

        self.search_engine = QComboBox()
        self.search_engine.addItems(search.SearchEngines())
        self.search_engine.setCurrentText(search.GetCurrentSearchEngine(1))
        self.search_engine.currentTextChanged.connect(search.on_search_changed)
        layout.addWidget(self.search_engine)

        self.discordrpc = QComboBox()
        self.discordrpc.addItems(["RPC (On)", "RPC (Off)"])
        self.discordrpc.setCurrentText("RPC (On)" if rpc.get_rpc() == 1 else "RPC (Off)")
        self.discordrpc.currentTextChanged.connect(rpc.on_rpc_changed)
        layout.addWidget(self.discordrpc)

        self.github_button = QPushButton("Source Code")
        self.github_button.clicked.connect(partial(self.openlink, "https://github.com/qualzed/qBrowser"))
        layout.addWidget(self.github_button)

        self.history_button = QPushButton(get_locale("hst"))
        self.history_button.clicked.connect(self.OpenHistory)
        layout.addWidget(self.history_button)

        self.uicustom_button = QPushButton(get_locale("uic"))
        self.uicustom_button.clicked.connect(self.OpenCustom)
        layout.addWidget(self.uicustom_button)

        self.support_button = QPushButton("Support me (donationalerts.com)")
        self.support_button.clicked.connect(partial(self.openlink, "https://www.donationalerts.com/r/qualzed"))
        layout.addWidget(self.support_button)

        self.debug_button = QPushButton(get_locale("dbg"))
        self.debug_button.clicked.connect(self.LaunchDebug)
        layout.addWidget(self.debug_button)
        
        layout.addStretch()
        
        self.setLayout(layout)
    
    def LaunchDebug(self):
        if(debug.debug_bool):
            debug.debug_bool = False
            debug.DebugSwitch(debug.debug_bool)
            os.system("qb\sendMessage.exe \"DEBUG LOG\" \"You turned off debuging\" 0")
        else:
            debug.debug_bool = True
            debug.DebugSwitch(debug.debug_bool)
            os.system("qb\sendMessage.exe \"DEBUG LOG\" \"You turned on debuging\" 0")

    def OpenHistory(self):
        main_window = self.parent()
        if main_window:
            history_window = HistoryWindow(main_window, self)
            history_window.exec()

    def OpenCustom(self):
        main_window = self.parent()
        if main_window:
            ui_window = uiWindow(main_window, self)
            ui_window.exec()

    def openlink(self, link):
        main_window = self.parent()
        if main_window:
            main_window.add_new_tab(QUrl(link))
    
    def on_language_changed(self, text):
        lang_map = {"English": "en", "Русский": "ru"}
        new_lang = lang_map.get(text)
        if new_lang:
            set_language(new_lang)
            main_window = self.parent()
            if main_window:
                main_window.update_ui_texts()

class HistoryWindow(QDialog): # Default history
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.currentTab = None

        self.main_window = main_window
        self.setWindowTitle("History")
        self.setGeometry(100, 100, 600, 600)
        self.setModal(True)
        layout = QVBoxLayout()

        lines = open(history_path, 'r', encoding='utf-8').readlines() if os.path.exists(history_path) else []
        self.hst = QListWidget()
        self.hst.addItems([line.strip() for line in lines])
        self.hst.currentTextChanged.connect(self.text_changed)
        layout.addWidget(self.hst)

        self.setLayout(layout)

        self.delete_button = QPushButton(get_locale("del"))
        self.delete_button.clicked.connect(lambda: self.deleteHistoryTab(self.currentTab))
        layout.addWidget(self.delete_button)

        self.clear_button = QPushButton(get_locale("clr"))
        self.clear_button.clicked.connect(lambda: self.clearHistory())
        layout.addWidget(self.clear_button)

    def deleteHistoryTab(self, tab: str):
        with open(history_path, "r") as f:
            lines = f.readlines()
        with open(history_path, "w") as f:
            [f.write(l) for l in lines if tab not in l]
        self.hst.takeItem(self.hst.currentRow())

    def clearHistory(self):
        open(history_path, 'w').close()
        self.hst.clear()

    def text_changed(self, s):
        if self.main_window and s:
            self.currentTab = s # 10.05.2026
            # self.main_window.add_new_tab(QUrl(s)) # 10.05.2026
            
class uiWindow(QDialog): # UI settings
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setWindowTitle("UI Edit")
        self.setGeometry(100, 100, 400, 100)
        self.setModal(True)

        self.bg = getattr(main_window, 'bg', '#ffffff')
        self.color = getattr(main_window, 'color', '#000000')
        self.button = getattr(main_window, 'button', "#101010")

        layout = QVBoxLayout()

        self.btn_bg = QPushButton(get_locale("redactbg"))
        self.btn_color = QPushButton(get_locale("redactcolor"))
        self.btn_button = QPushButton(get_locale("redactbutton"))
        
        self.btn_bg.clicked.connect(lambda: self.open_color_picker('bg'))
        self.btn_color.clicked.connect(lambda: self.open_color_picker('color'))
        self.btn_button.clicked.connect(lambda: self.open_color_picker('button'))

        layout.addWidget(self.btn_bg)
        layout.addWidget(self.btn_color)
        layout.addWidget(self.btn_button)

        self.setLayout(layout)

    def open_color_picker(self, param):
        color = QColorDialog.getColor(QColor(getattr(self, param)), self, get_locale("selectcolor"))
        if color.isValid():
            setattr(self, param, color.name())
            set_ui(self.bg, self.color, self.button)
            update_ui()

    def accept(self):
        self.main_window.bg = self.bg
        self.main_window.color = self.color
        self.main_window.button = self.button
        super().accept()        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Cookies
        base_dir = os.path.dirname(os.path.abspath(__file__))
        storage_path = os.path.join(base_dir, "user", "data")
        os.makedirs(storage_path, exist_ok=True)
        self.profile = QWebEngineProfile("StorageData", self)
        self.profile.setPersistentStoragePath(storage_path)
        self.profile.setCachePath(storage_path)
        self.profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies
        )
        


        # Download 29.04.2026
        self.profile.downloadRequested.connect(self.on_download_requested)
        self.web_page = QWebEnginePage(self.profile, self)
        self.browser = QWebEngineView()
        self.browser.setPage(self.web_page) 
        settings = self.browser.settings()
        settings.setAttribute(settings.WebAttribute.JavascriptCanOpenWindows, True)
        settings.setAttribute(settings.WebAttribute.LocalStorageEnabled, True)

        self.statusBar().setVisible(False)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False) # Скрыт по умолчанию
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #333;
                border-radius: 4px;
                text-align: center;
                background-color: #111;
                color: white;
                max-height: 14px;
            }
            QProgressBar::chunk {
                background-color: #18ca27;
            }
        """)
        self.statusBar().addPermanentWidget(self.progress_bar, 1)
        self.dl_timer = QTimer(self)
        self.dl_timer.timeout.connect(self._track_dl)

        self.cancel_btn = QPushButton("✕")
        self.cancel_btn.setFixedSize(20, 20)
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: white;
                border-radius: 10px;
                font-weight: bold;
                font-size: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #ff3333;
            }
        """)
        self.cancel_btn.clicked.connect(self.cancel_download)
        self.cancel_btn.setVisible(False)
        self.statusBar().addPermanentWidget(self.cancel_btn)


        
        # Fix window resolution
        self.setWindowTitle("qBrowser")
        x,y = get_current_resolution()
        if x > resolution.width-65 or y > resolution.height-65:
            x = int(resolution.width / 2)
            y = int(resolution.height / 2)
        self.setGeometry(100, 100, x, y)

        self.setWindowIcon(QIcon("icon.png"))
        
        global current_language
        current_language = get_current_language()
        
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tab_widget)

        self.toolbar = self.addToolBar("Navigation")
        
        self.back_action = QAction(get_locale("bk"), self)
        self.back_action.triggered.connect(self.on_back)
        
        self.forward_action = QAction(get_locale("fw"), self)
        self.forward_action.triggered.connect(self.on_forward)
        
        self.toolbar.addAction(self.back_action)
        self.toolbar.addAction(self.forward_action)
        
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.toolbar.addWidget(left_spacer)
        
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText(get_locale("gstr"))
        self.search_bar.returnPressed.connect(self.on_search)
        self.toolbar.addWidget(self.search_bar)
        
        self.search_button = QPushButton(get_locale("gsearch"), self)
        self.search_button.clicked.connect(self.on_search)
        self.toolbar.addWidget(self.search_button)

        self.voice_button = QPushButton("🎙️", self)
        self.voice_button.clicked.connect(self.callvoice)
        self.toolbar.addWidget(self.voice_button)
        
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.toolbar.addWidget(right_spacer)
        
        self.home_action = QAction(get_locale("home"), self)
        self.home_action.triggered.connect(self.on_home)
        
        self.new_tab_action = QAction(get_locale("ntab"), self)
        self.new_tab_action.triggered.connect(self.on_new_tab)
        
        self.settings_action = QAction("⚙️", self)
        self.settings_action.triggered.connect(self.opensettings)
        
        self.toolbar.addAction(self.home_action)
        self.toolbar.addAction(self.new_tab_action)
        self.toolbar.addAction(self.settings_action)
        
        self.tab_widget.currentChanged.connect(self.update_actions)
        
        saved_tabs = tabs.ReadTabs()
        if vcheck.NEW_VERSION_AVIABLE(): # Checking current version
            self.add_new_tab(QUrl.fromLocalFile(os.path.abspath(update_path)))
            
            if saved_tabs is None:
                self.add_new_tab()
            else:
                for link in saved_tabs:
                    self.add_new_tab(QUrl(link))
        else:
            if saved_tabs is None:
                self.add_new_tab()
            else:
                for link in saved_tabs:
                    self.add_new_tab(QUrl(link))
    


    def on_download_requested(self, download):
        self._current_download = download 
        path, _ = QFileDialog.getSaveFileName(self, "Save File", download.suggestedFileName())
        
        if path:
            download.setDownloadDirectory(os.path.dirname(path))
            download.setDownloadFileName(os.path.basename(path))
            download.accept()

            self.statusBar().setVisible(True)
            self.progress_bar.setVisible(True)
            self.cancel_btn.setVisible(True)
            
            self.progress_bar.setValue(0)
            self.statusBar().showMessage(f"Downloading: {download.suggestedFileName()}")
            self.dl_timer.start(200) 
        else:
            download.cancel()

    def _track_dl(self):
        if self._current_download:
            received = self._current_download.receivedBytes()
            total = self._current_download.totalBytes()
            
            if total > 0:
                p = int((received / total) * 100)
                self.progress_bar.setValue(p)
            else:
                self.progress_bar.setRange(0, 0)

            state = self._current_download.state().value
            if state >= 2:
                self.dl_timer.stop()
                self.statusBar().setVisible(False)
                self.cancel_btn.setVisible(False)
                self._current_download = None
        else:
            self.dl_timer.stop()
            self.progress_bar.setVisible(False)

    def cancel_download(self):
        if self._current_download:
            self._current_download.cancel() # Отменяем в движке
            self.dl_timer.stop()
            self.statusBar().setVisible(False)
            self.cancel_btn.setVisible(False)
            self._current_download = None
            self.statusBar().showMessage("Download canceled", 2000)


    def add_new_tab(self, url=None):
        browser = QWebEngineView()

        new_page = QWebEnginePage(self.profile, browser) # For cookies
        browser.setPage(new_page)

        browser.setUrl(url if url else QUrl(search.GetCurrentSearchEngine(2)))
        browser.titleChanged.connect(self.update_tab_title)
        browser.loadFinished.connect(self.update_actions)
        index = self.tab_widget.addTab(browser, get_locale("ntab"))
        self.tab_widget.setCurrentIndex(index)
    
    def update_tab_title(self, title):
        if len(title) > 16: # No long titles
            title = title[:16] + "..."
            
        browser = self.sender()
        if browser:
            index = self.tab_widget.indexOf(browser)
            if index != -1:
                self.tab_widget.setTabText(index, title if title else get_locale("ntab"))
    
    def update_actions(self):
        current_browser = self.tab_widget.currentWidget() # Current tab

        if current_browser:
            for i in range(self.tab_widget.count()):
                current_title = self.tab_widget.tabText(i)
                if(rpc.get_rpc() == 1): # if RPC On
                    try: # Crash fix 23.04.2026
                        rpc.UpdateRPC(f"Browsing {current_title}") # RPC Current tab
                    except:
                        pass

            self.back_action.setEnabled(current_browser.history().canGoBack())
            self.forward_action.setEnabled(current_browser.history().canGoForward())            
        else:
            self.back_action.setEnabled(False)
            self.forward_action.setEnabled(False)
    
    def on_back(self):
        current_browser = self.tab_widget.currentWidget()
        if current_browser and current_browser.history().canGoBack():
            current_browser.history().back()
            self.update_actions()
    
    def on_forward(self):
        current_browser = self.tab_widget.currentWidget()
        if current_browser and current_browser.history().canGoForward():
            current_browser.history().forward()
            self.update_actions()
    
    def on_home(self):
        current_browser = self.tab_widget.currentWidget()
        if current_browser:
            current_browser.setUrl(QUrl(search.GetCurrentSearchEngine(2)))
            self.update_actions()
    
    def on_new_tab(self):
        self.add_new_tab()
    
    def on_search(self):
        current_browser = self.tab_widget.currentWidget()
        query = self.search_bar.text().strip()
        if current_browser and query:

            if not search.IsDomain(query): # Domain Fix 29.04.2026
                search_url = f"{search.GetCurrentSearchEngine(2)}/search?q={query}"
            else:
                if not query.startswith(('http://', 'https://')):
                    search_url = f"https://{query}"
                else:
                    search_url = f"{query}"

            debug.debug("Search debug", query)

            current_browser.setUrl(QUrl(search_url))
            self.AddHistory(search_url)
            self.update_actions()
    
    def AddHistory(self, url):
        with open(history_path, 'a+', encoding='utf-8') as f: 
            f.write(url + "\n")

    def callvoice(self):
        query = voice()
        current_browser = self.tab_widget.currentWidget()
        if current_browser and query:
            current_browser.setUrl(QUrl(f"{search.GetCurrentSearchEngine(2)}/search?q={query}"))
            self.update_actions()

    def close_tab(self, index):
        if self.tab_widget.count() == 1:
            exit(0)
        self.tab_widget.removeTab(index)
        self.update_actions()
    
    def opensettings(self):
        settings_window = SettingsWindow(self)
        settings_window.exec()
    
    def update_ui_texts(self):
        sett = SettingsWindow(self)
        ui = uiWindow(self)
        self.back_action.setText(get_locale("bk"))
        self.forward_action.setText(get_locale("fw"))
        self.search_bar.setPlaceholderText(get_locale("gstr"))
        self.search_button.setText(get_locale("gsearch"))
        self.home_action.setText(get_locale("home"))
        self.new_tab_action.setText(get_locale("ntab"))
        sett.history_button.setText(get_locale("hst"))
        ui.btn_bg.setText(get_locale("redactbg"))
        ui.btn_color.setText(get_locale("redactbutton"))
        ui.btn_button.setText(get_locale("redactcolor"))
        for i in range(self.tab_widget.count()):
            browser = self.tab_widget.widget(i)
            current_title = self.tab_widget.tabText(i)
            if current_title == "Loading..." or current_title == get_locale("ntab"):
                self.tab_widget.setTabText(i, get_locale("ntab"))

    def closeEvent(self, a0): # Close window
        tab_list = []
        for i in range(self.tab_widget.count()):
            browser = self.tab_widget.widget(i)
            tab_url = browser.url().toString()
            tab_list.append(tab_url)
            final_tab_list = "\n".join(tab_list)
            tabs.SaveTabs(final_tab_list)

        x = self.width()
        y = self.height()
        set_resolution(x,y)
        return super().closeEvent(a0)

    def resizeEvent(self, a0):
        x = self.width()
        y = self.width()
        self.search_bar.setMinimumWidth(int(x / 2.0))
        self.search_bar.setMaximumWidth(int(x))

        if(x < 500):
            self.setGeometry(100, 100, 500, y)

        return super().resizeEvent(a0)

if __name__ == '__main__':
    if rpc.get_rpc() == 1: rpc.StartRPC()
    args.CheckArguments()
    app = QApplication(sys.argv)
    window = MainWindow()
    update_ui()
    window.show()
    app.exec()