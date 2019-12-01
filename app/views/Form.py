from PyQt5.QtWidgets import QLabel, QLineEdit, QGroupBox, QComboBox, QFormLayout, QVBoxLayout, QDialogButtonBox

from app.models.Database import Database
from app.models.Store import Store

class Form():
    db = Database()
    form_layout = None

    @staticmethod
    def make_form(accept, reject):
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(accept)
        buttonBox.rejected.connect(reject)

        fomr_group_box = Form.create_form_froup_box()

        layout = QVBoxLayout()
        layout.addWidget(fomr_group_box)
        layout.addWidget(buttonBox)

        return layout

    @staticmethod
    def create_form_froup_box():
        form_group_box = QGroupBox("Insert a new row")
        layout = QFormLayout()

        current_table = Store.get_current_tab()['title']
        Form.make_custom_fields(layout, current_table)

        form_group_box.setLayout(layout)

        Form.form_layout = form_group_box

        return form_group_box

    @staticmethod
    def make_combobox(items):
        cb = QComboBox()
        for item in items:
            cb.addItem(item)

        return cb

    @staticmethod
    def make_custom_fields(layout, table_name):
        fields = Form.db.get_table_columns_names(table_name)

        for field in fields:
            layout.addRow(QLabel(field), QLineEdit())

    @staticmethod
    def get_all_values():
        return [field.text() for field in Form.form_layout.findChildren(QLineEdit)]
