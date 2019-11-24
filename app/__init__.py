from app.views.Tabs import Tabs

class App():
    def __init__(self, parent):
        _tabs = Tabs(parent)
        _tabs.make_tabs()
