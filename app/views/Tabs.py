from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QTabWidget
from PyQt5.QtCore import pyqtSlot

from app.models.Database import Database
from app.models.Store import Store
from app.views.Table import Table

class Tabs(QTabWidget):
    def __init__(self):
        QTabWidget.__init__(self)
        self.db = Database()

    def make_tabs(self):
        tabs = []

        for table in self.db.get_all_tables():
            data = self.db.get_table_data(table, 0)

            _tab = {
                'title': table,
                'content': data,
            }
            tabs.append(_tab)

            Store.add_tab({
                'title': table,
                'last_row_loaded': Database.ROWS_PER_LOAD,
            })

        self.init_tabs()
        self.add_tabs(tabs)

    def init_tabs(self):
        self.resize(900, 900)
        self.setMinimumSize(640, 480)

        self.currentChanged.connect(self.tab_click)

    def add_tabs(self, tabs):
        for i, _tab in enumerate(tabs):
            name = _tab['title']

            table_foreign_keys = self.db.get_foreign_keys(name)
            Store.add_foreign_keys(i, table_foreign_keys)

            _table = Table(name, table_foreign_keys)
            table = _table.generate_table(
                list(map(lambda t: str(t), _tab['content']['headers'])),
                _tab['content']['rows']
            )

            Store.add_table(i, _table)

            self.addTab(_table, name)

    @pyqtSlot()
    def tab_click(self):
        current_tab = self.currentIndex()
        Store.set_current_tab(current_tab)
