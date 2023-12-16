import sys, os
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class FormBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setAcceptDrops(True)

app = QApplication(sys.argv)

builder = FormBuilder()
builder.show()

sys.exit(app.exec_())