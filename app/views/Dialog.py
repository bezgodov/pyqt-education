from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QSize

from app.views.Form import Form
from app.views.Table import Table
from app.models.Database import Database


class Dialog(QDialog):
    def __init__(self, title=None, minsize=QSize(640,480), maxsize=QSize(1200,1200)):
        QDialog.__init__(self)

        self.db = Database()

        self.setWindowTitle(title)
        self.setMinimumSize(minsize)
        self.setMaximumSize(maxsize)

        self.init_layout()

        accepted = self.exec_()

        if accepted == QDialog.Accepted:
            values = Form.get_all_values()
            self.db.insert_row_to_table(values)

    def init_layout(self):
        layout = Form.make_form(self.accept, self.reject)

        self.setLayout(layout)
