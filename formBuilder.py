from PySide6.QtWidgets import QWidget, QLabel

class FormBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setAcceptDrops(True)