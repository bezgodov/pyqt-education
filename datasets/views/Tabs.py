from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QTabWidget
from datasets.views.Table import Table
from PyQt5.QtCore import pyqtSlot
from datasets.models.Database import Database
from datasets.models.Store import Store

class Tabs(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.tabs = []
        self.parent = parent

    def make_tabs(self):
        tabs = []

        db = Database()
        for table in db.get_all_tables():
            data = db.get_table_data(table, 0)

            _tab = {
                'title': table,
                'content': data,
            }
            tabs.append(_tab)

            Store.add_tab({
                'title': table,
                'last_row_loaded': Database.ROWS_PER_LOAD,
            })

        self.tabs = self.init_tabs()
        self.add_tabs(self.tabs, tabs)

    def init_tabs(self):
        tabs_layout = QVBoxLayout(self)

        tabs = QTabWidget()
        tabs.resize(900, 900)
        tabs.setMinimumSize(640, 480)

        tabs.currentChanged.connect(self.tab_click)

        tabs_layout.addWidget(tabs)
        self.parent.setLayout(tabs_layout)

        return tabs

    def add_tabs(self, tabs_widget, tabs):
        for _tab in tabs:
            tab = QWidget()

            layout = QGridLayout(self)

            _table = Table()
            table = _table.generate_table(
                list(map(lambda t: str(t), _tab['content']['headers'])),
                _tab['content']['rows']
            )

            tabs_widget.addTab(tab, _tab['title'])
            layout.addWidget(table)
            tab.setLayout(layout)

    @pyqtSlot()
    def tab_click(self):
        current_tab = self.tabs.currentIndex()
        Store.set_current_tab(current_tab)
