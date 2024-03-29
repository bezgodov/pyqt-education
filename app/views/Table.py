from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QMenu, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

from app.models.Database import Database
from app.models.Store import Store
from app.views.ComboBox import ComboBox

class Table(QTableWidget):

    PERCENT_TO_START_LOADING = 0.9

    def __init__(self, name, foreign_keys):
        QTableWidget.__init__(self)
        self.name = name
        self.foreign_keys = foreign_keys

        self.db = Database()
        self.setMinimumSize(640, 480)
        self.resize(900, 900)

    def init_signals(self):
        self.cellChanged.connect(self.cell_cnanged)

    def get_value_in_cell(self, row, col):
        item = self.item(row, col)

        return item.text()

    def cell_cnanged(self, row, col):
        table = Store.get_current_tab()
        pk_id = self.get_value_in_cell(row, 0)
        value = self.get_value_in_cell(row, col)
        col_name = self.get_col_name(col)

        self.db.update_table_column(table, pk_id, col_name, value)

    def get_col_name(self, col):
        item = self.horizontalHeaderItem(col)
        return item.text()
    def wheelEvent(self, evt):
        super().wheelEvent(evt)
        scrollbar = self.verticalScrollBar()
        current = scrollbar.value()
        maximum = scrollbar.maximum()

        if current > maximum * self.PERCENT_TO_START_LOADING:
            self.add_rows_to_table()

    def generate_table(self, headers, rows):
        self.init_table(headers, rows)

        self.set_table_headers(headers)
        self.set_table_rows(rows)

        self.init_signals()

        return self

    def init_table(self, headers, rows):
        self.setColumnCount(len(headers))
        self.setRowCount(len(rows))

        self.setHorizontalHeaderLabels(headers)
        self.resizeColumnsToContents()
        self.resizeRowsToContents() # this line doesn't work actually, next one span cells to theirs content
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        return self

    def set_table_headers(self, headers):
        for i, h in enumerate(headers):
            self.horizontalHeaderItem(i).setToolTip(h)
            self.horizontalHeaderItem(i).setTextAlignment(Qt.AlignLeft)

    def set_table_rows(self, rows):
        for i, r in enumerate(rows):
            self.set_row_columns(r, i)

    def set_row_columns(self, row, rowPosition):
        for j, c in enumerate(row):
            item = QTableWidgetItem(str(c))
            if j == 0:
                item.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.setItem(rowPosition, j, item)

            if self.is_column_foreign_key(j):
                _column = self.get_col_name(j)
                values = self.get_foreign_key_values(_column)

                pk_id = self.get_value_in_cell(rowPosition, 0)
                comboBox = ComboBox(values, _column, c, self.foreign_keys, pk_id)

                self.setCellWidget(rowPosition, j, comboBox)

    def get_foreign_key_values(self, column):
        table = self.foreign_keys[column]['table']
        column = self.foreign_keys[column]['column']

        res = self.db.get_table_data_by_foreign_key(table)

        return res


    def is_column_foreign_key(self, column):
        if len(self.foreign_keys) > 0:
            return self.get_col_name(column) in self.foreign_keys.keys()

        return False

    def add_row_to_table(self, row):
        rowPosition = self.rowCount()
        self.insertRow(rowPosition)

        self.set_row_columns(row, rowPosition)

    def add_rows_to_table(self):
        rows = self.get_data_to_add()
        for r in rows:
            self.add_row_to_table(r)

    def get_data_to_add(self):
        current_tab = Store.get_current_tab()

        last_row = current_tab['last_row_loaded']
        last_row_loaded = last_row + Database.ROWS_PER_LOAD

        data = self.db.get_table_data(current_tab['title'], last_row)

        Store.set_last_row(Store.get_current_tab(), last_row_loaded)

        return data['rows']

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        edit_action = QAction('Edit cell', self)
        edit_action.triggered.connect(self.edit_cell)
        menu.addAction(edit_action)

        remove_action = QAction('Remove row', self)
        remove_action.triggered.connect(self.remove_row)
        menu.addAction(remove_action)

        menu.popup(QCursor.pos())

    def edit_cell(self):
        cell = self.currentItem()
        self.editItem(cell)

    def remove_row(self):
        row = self.currentRow()

        table = Store.get_current_tab()
        pk_id = self.get_value_in_cell(row, 0)
        self.db.remove_table_row(table, pk_id)

        for tab in Store.get_all_tabs():
            if 'foreign_keys' in tab.keys():
                for key in tab['foreign_keys']:
                    _info = tab['foreign_keys'][key]
                    if _info['table'] == self.name:
                        _connected_table_name = tab['title']
                        self.db.update_table_column(tab, 'NULL', key, pk_id, key)

        self.removeRow(row)
