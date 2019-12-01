import sys
from PyQt5.QtWidgets import QAction, qApp

from app.views.Tabs import Tabs
from app.models.Store import Store

class App():
    def __init__(self, parent):
        Store.app = parent

        _tabs = Tabs(parent)
        _tabs.make_tabs()

        self.initUI(parent)
        parent.setCentralWidget(_tabs)

    def initUI(self, parent):
        Store.show_message_in_status_bar('Ready')

        exit_action = QAction("& Exit app", parent)
        exit_action.setStatusTip('Close app window')
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(qApp.quit)

        main_menu = parent.menuBar()
        file_menu = main_menu.addMenu('File')
        file_menu.addAction(exit_action)
