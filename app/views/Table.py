from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt

from app.models.Database import Database
from app.models.Store import Store

class Table(QTableWidget):

    PERCENT_TO_START_LOADING = 0.9

    def __init__(self):
        QTableWidget.__init__(self)
        self.db = Database()
        self.setMinimumSize(640, 480)

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
            if (j == 0):
                item.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.setItem(rowPosition, j, item)

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
