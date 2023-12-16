import sys, os
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from FormBuilder import FormBuilder

if __name__ == "__main__":
    app = QApplication(sys.argv)

    builder = FormBuilder()
    builder.show()

    sys.exit(app.exec_())