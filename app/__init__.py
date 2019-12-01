from app.views.Tabs import Tabs
from app.views.Menu import Menu
from app.models.Store import Store

class App():
    def __init__(self, parent):
        Store.app = parent

        _tabs = Tabs(parent)
        _tabs.make_tabs()

        self.initUI(parent)
        parent.setCentralWidget(_tabs)

    def initUI(self, parent):
        Menu.init_menu(parent)
