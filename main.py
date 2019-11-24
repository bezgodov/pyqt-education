import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from datasets.views.Tabs import Tabs
from datasets.views.Table import Table
from datasets.models.Database import Database
from datasets.models.Store import Store

# Chosen dataset: https://www.kaggle.com/corrphilip/numeral-gestures/

class App(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Numeral gestures")
        self.setMinimumSize(640, 480)
        self.setMaximumSize(1200, 1200)

        _tabs = Tabs(self)
        _tabs.make_tabs()

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
