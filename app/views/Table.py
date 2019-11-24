from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

from app.models.Database import Database
from app.models.Store import Store

class Table(QWidget):

    PERCENT_TO_START_LOADING = 0.9

    def __init__(self):
        QWidget.__init__(self)
        self.setMinimumSize(640, 980)

    def generate_table(self, headers, rows):
        table = self.init_table(headers, rows)

        self.set_table_headers(table, headers)
        self.set_table_rows(table, rows)

        return table

    def init_table(self, headers, rows):
        table = QTableWidgetCustom(self)
        table.setEnabled(True)
        table.setColumnCount(len(headers))
        table.setRowCount(len(rows))

        table.setHorizontalHeaderLabels(headers)
        table.resizeColumnsToContents()

        return table

    def set_table_headers(self, table, headers):
        for i, h in enumerate(headers):
            table.horizontalHeaderItem(i).setToolTip(h)
            table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignLeft)

    def set_table_rows(self, table, rows):
        for i, r in enumerate(rows):
            self.set_row_columns(table, r, i)

    def set_row_columns(self, table, row, rowPosition):
        for j, c in enumerate(row):
            table.setItem(rowPosition, j, QTableWidgetItem(str(c)))

    def add_row_to_table(self, table, row):
        rowPosition = table.rowCount()
        table.insertRow(rowPosition)

        self.set_row_columns(table, row, rowPosition)

    def add_rows_to_table(self, table):
        rows = self.get_data_to_add()
        for r in rows:
            self.add_row_to_table(table, r)

    def get_data_to_add(self):
        db = Database()

        current_tab = Store.get_current_tab()

        last_row = current_tab['last_row_loaded']
        last_row_loaded = last_row + Database.ROWS_PER_LOAD

        data = db.get_table_data(current_tab['title'], last_row)

        Store.set_last_row(Store.get_current_tab(), last_row_loaded)

        return data['rows']

class QTableWidgetCustom(QTableWidget):
    def __init__(self, table):
        QTableWidget.__init__(self)
        self.table = table

    def wheelEvent(self, evt):
        super().wheelEvent(evt)
        scrollbar = self.verticalScrollBar()
        current = scrollbar.value()
        maximum = scrollbar.maximum()

        if current > maximum * self.table.PERCENT_TO_START_LOADING:
            self.table.add_rows_to_table(self)
