from PyQt5.QtWidgets import QAction, qApp

from app.views.Tabs import Tabs

class App():
    def __init__(self, parent):
        self.init_exit_action(parent)

        _tabs = Tabs(parent)
        _tabs.make_tabs()

    def init_exit_action(self, parent):
        exit_action = QAction('&Exit', parent)
        exit_action.setShortcut('Ctrl+C')
        exit_action.triggered.connect(qApp.quit)
