import sys
from PyQt5.QtWidgets import QAction, qApp

from app.views.Dialog import Dialog

class Menu():

    @staticmethod
    def init_menu(app):
        main_menu = app.menuBar()

        Menu.init_file_menu(main_menu, app)
        Menu.init_table_menu(main_menu, app)
    
    @staticmethod
    def init_file_menu(menu, app):
        exit_action = QAction("& Exit app", app)
        exit_action.setStatusTip('Close app window')
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(qApp.quit)

        file_menu = menu.addMenu('File')
        file_menu.addAction(exit_action)

    @staticmethod
    def init_table_menu(menu, app):
        add_new_row_action = QAction("& Insert row", app)
        add_new_row_action.setStatusTip('Click to insert a new row to a table')
        add_new_row_action.triggered.connect(Menu.insert_new_row)

        table_menu = menu.addMenu('Table')
        table_menu.addAction(add_new_row_action)

    @staticmethod
    def insert_new_row():
        dialog_title = 'Insert a new row'
        dialog = Dialog(dialog_title)
