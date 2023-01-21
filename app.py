from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5 import QtWidgets
import breeze_resources
import os
import sys
import platform 
 
class MainWindow(QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        self.setWindowIcon(QIcon('ir.png'))
        self.tabs = QTabWidget()
 
        self.tabs.setDocumentMode(True)
 
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
 
        self.tabs.currentChanged.connect(self.current_tab_changed)
 
        self.tabs.setTabsClosable(True)
 
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
 
        self.setCentralWidget(self.tabs)
 
        self.status = QStatusBar()
 
        self.setStatusBar(self.status)
 
        navtb = QToolBar("Navigation")
 
        self.addToolBar(navtb)
 
        back_btn = QAction(QIcon('b.png'), "Back to previous page", self)
 
 
 
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
 
        navtb.addAction(back_btn)
 
        next_btn = QAction(QIcon('f.png'), "Forward to next page", self)
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)
 
        reload_btn = QAction(QIcon('r.png'), "Reload page", self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)
 
        home_btn = QAction(QIcon('h.png'),"Go home", self)
 
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)
 
        navtb.addSeparator()
 
        self.urlbar = QLineEdit()
        
        self.urlbar.returnPressed.connect(self.navigate_to_url)
 

        navtb.addWidget(self.urlbar)
 
        stop_btn = QAction(QIcon('c.png'), "Stop loading current page", self)
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)
 
        self.add_new_tab(QUrl('http://www.searx.work'), 'Homepage')
 
        self.show()
 
        self.setWindowTitle("CorgiWeb")
 
    def add_new_tab(self, qurl = None, label ="Blank"):
    
        if qurl is None:
            qurl = QUrl('http://www.searx.work')
 
        browser = QWebEngineView()
        
        version = "1.32"
        browser.page().profile().setHttpUserAgent("Mozilla/5.0 (" + platform.system() + " " + platform.machine() + "; " + platform.version().split('.')[2] + ") CorgiWeb " + version)
 
        browser.setUrl(qurl)
 
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
 
        browser.urlChanged.connect(lambda qurl, browser = browser:
                                   self.update_urlbar(qurl, browser))
 
        browser.loadFinished.connect(lambda _, i = i, browser = browser:
                                     self.tabs.setTabText(i, browser.page().title()))
 
    def tab_open_doubleclick(self, i):
 
        if i == -1:
            self.add_new_tab()
 
    def current_tab_changed(self, i):
 
        qurl = self.tabs.currentWidget().url()
 
        self.update_urlbar(qurl, self.tabs.currentWidget())
 
        self.update_title(self.tabs.currentWidget())
 
    def close_current_tab(self, i):
 
        if self.tabs.count() < 2:
            return
 
        self.tabs.removeTab(i)
 
    def update_title(self, browser):
 
        if browser != self.tabs.currentWidget():
            return
 
        title = self.tabs.currentWidget().page().title()
 
        self.setWindowTitle("% s - CorgiWeb" % title)
 
    def navigate_home(self):
 
        self.tabs.currentWidget().setUrl(QUrl("http://www.searx.work"))
 
    def navigate_to_url(self):
 
        q = QUrl(self.urlbar.text())
 
        if q.scheme() == "":
            q.setScheme("http")
 
        self.tabs.currentWidget().setUrl(q)
 
    def update_urlbar(self, q, browser = None):
 
        if browser != self.tabs.currentWidget():
 
            return
 
        self.urlbar.setText(q.toString())
 
        self.urlbar.setCursorPosition(0)
 
app = QApplication(sys.argv)

file = QFile(":/dark/stylesheet.qss")
file.open(QFile.ReadOnly | QFile.Text)
stream = QTextStream(file)
app.setStyleSheet(stream.readAll())

app.setApplicationName("CorgiWeb")
 
window = MainWindow()
 
app.exec_()