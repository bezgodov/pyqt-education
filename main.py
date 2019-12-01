import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from app import App

# Chosen dataset: https://www.kaggle.com/corrphilip/numeral-gestures/

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Numeral gestures")
        self.setMinimumSize(640, 480)
        self.setMaximumSize(1200, 1200)

        App(self)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main()
    sys.exit(app.exec_())
