import sys
import os
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QComboBox, QWidget, QSpacerItem, QSizePolicy, QLineEdit, QPushButton, QDialog, QVBoxLayout, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from locales.ru import ru
from locales.en import en


search_system = 'https://google.com'
current_language = "ru"


def get_locale(key):
    global current_language
    locales = {"ru": dict(ru), "en": dict(en)}
    return locales.get(current_language, locales["ru"]).get(key, "не найден")


def set_language(lang, config_path="config/qb.cfg"):
    global current_language
    match lang:
        case "en":
            current_language = "en"
        case "ru":
            current_language = "ru"
        case _:
            return
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(f"language={current_language}\n")


def get_current_language(config_path="config/qb.cfg"):
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("language="):
                    return line.strip().split("=", 1)[1]
    return "ru"


class SettingsWindow(QDialog):
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
        
        self.github_button = QPushButton("Open Source")
        self.github_button.clicked.connect(self.opensrc)
        layout.addWidget(self.github_button)
        
        layout.addStretch()
        
        self.setLayout(layout)
    
    def opensrc(self):
        main_window = self.parent()
        if main_window:
            main_window.add_new_tab(QUrl("https://github.com/qualzed/qBrowser"))
    
    def on_language_changed(self, text):
        lang_map = {"English": "en", "Русский": "ru"}
        new_lang = lang_map.get(text)
        if new_lang:
            set_language(new_lang)
            main_window = self.parent()
            if main_window:
                main_window.update_ui_texts()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("qb")
        self.setGeometry(100, 100, 800, 600)
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
        self.search_bar.setFixedWidth(400)
        self.search_bar.returnPressed.connect(self.on_search)
        self.toolbar.addWidget(self.search_bar)
        
        self.search_button = QPushButton(get_locale("gsearch"), self)
        self.search_button.clicked.connect(self.on_search)
        self.toolbar.addWidget(self.search_button)
        
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.toolbar.addWidget(right_spacer)
        
        self.home_action = QAction(get_locale("home"), self)
        self.home_action.triggered.connect(self.on_home)
        
        self.new_tab_action = QAction(get_locale("ntab"), self)
        self.new_tab_action.triggered.connect(self.on_new_tab)
        
        self.settings_action = QAction("⚙️", self)
        self.settings_action.triggered.connect(self.changelocale)
        
        self.toolbar.addAction(self.home_action)
        self.toolbar.addAction(self.new_tab_action)
        self.toolbar.addAction(self.settings_action)
        
        self.tab_widget.currentChanged.connect(self.update_actions)
        
        self.add_new_tab()
    
    def add_new_tab(self, url=None):
        browser = QWebEngineView()
        browser.setUrl(url if url else QUrl(search_system))
        browser.titleChanged.connect(self.update_tab_title)
        browser.loadFinished.connect(self.update_actions)
        index = self.tab_widget.addTab(browser, get_locale("ntab"))
        self.tab_widget.setCurrentIndex(index)
    
    def update_tab_title(self, title):
        browser = self.sender()
        if browser:
            index = self.tab_widget.indexOf(browser)
            if index != -1:
                self.tab_widget.setTabText(index, title if title else get_locale("ntab"))
    
    def update_actions(self):
        current_browser = self.tab_widget.currentWidget()
        if current_browser:
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
            current_browser.setUrl(QUrl(search_system))
            self.update_actions()
    
    def on_new_tab(self):
        self.add_new_tab()
    
    def on_search(self):
        current_browser = self.tab_widget.currentWidget()
        query = self.search_bar.text().strip()
        if current_browser and query:
            search_url = f"https://www.google.com/search?q={query}"
            current_browser.setUrl(QUrl(search_url))
            self.update_actions()
    
    def close_tab(self, index):
        if self.tab_widget.count() == 1:
            exit()
        self.tab_widget.removeTab(index)
        self.update_actions()
    
    def changelocale(self):
        settings_window = SettingsWindow(self)
        settings_window.exec()
    
    def update_ui_texts(self):
        self.back_action.setText(get_locale("bk"))
        self.forward_action.setText(get_locale("fw"))
        self.search_bar.setPlaceholderText(get_locale("gstr"))
        self.search_button.setText(get_locale("gsearch"))
        self.home_action.setText(get_locale("home"))
        self.new_tab_action.setText(get_locale("ntab"))
        for i in range(self.tab_widget.count()):
            browser = self.tab_widget.widget(i)
            current_title = self.tab_widget.tabText(i)
            if current_title == "Loading..." or current_title == get_locale("ntab"):
                self.tab_widget.setTabText(i, get_locale("ntab"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()