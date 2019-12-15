from PyQt5.QtWidgets import QComboBox

from app.models.Database import Database
from app.models.Store import Store

class ComboBox(QComboBox):

    def __init__(self, values, _column, c, foreign_keys, pk_id):
        QComboBox.__init__(self)

        self.db = Database()
        self.pk_id = pk_id
        self.column = _column

        self.init(values, _column, c, foreign_keys)

    def init(self, values, _column, c, foreign_keys):
        headers = values['headers']
        foreign_key_position = headers.index(foreign_keys[_column]['column'])

        is_found_value = False
        for val_index, v in enumerate(values['rows']):
            val = " | ".join([str(_v) for _v_index, _v in enumerate(v) if _v_index != foreign_key_position])
            val = (val[:35] + '..') if len(val) > 35 else val

            foreign_key_value = v[foreign_key_position]

            self.addItem(val, foreign_key_value)
            if v[foreign_key_position] == c:
                self.setCurrentIndex(val_index)
                is_found_value = True

        self.insertItem(0, 'NULL', 'NULL')

        if not is_found_value:
            self.setCurrentIndex(0)

        self.currentIndexChanged.connect(self.combobox_changed)

    def combobox_changed(self, item):
        table = Store.get_current_tab()
        new_val = self.currentData()

        self.db.update_table_column(table, self.pk_id, self.column, new_val)
