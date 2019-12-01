from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QTabWidget
from PyQt5.QtCore import pyqtSlot

from app.models.Database import Database
from app.models.Store import Store
from app.views.Table import Table

class Tabs(QTabWidget):
    def __init__(self):
        QTabWidget.__init__(self)

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

        self.init_tabs()
        self.add_tabs(tabs)

    def init_tabs(self):
        self.resize(900, 900)
        self.setMinimumSize(640, 480)

        self.currentChanged.connect(self.tab_click)

    def add_tabs(self, tabs):
        for i, _tab in enumerate(tabs):
            _table = Table()
            table = _table.generate_table(
                list(map(lambda t: str(t), _tab['content']['headers'])),
                _tab['content']['rows']
            )

            Store.add_table(i, _table)

            self.addTab(_table, _tab['title'])

    @pyqtSlot()
    def tab_click(self):
        current_tab = self.currentIndex()
        Store.set_current_tab(current_tab)
