import sys, os
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from formBuilder import FormBuilder

app = QApplication(sys.argv)

builder = FormBuilder()
builder.show()

sys.exit(app.exec_())