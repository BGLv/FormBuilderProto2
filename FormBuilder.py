from PySide6.QtWidgets import QWidget, QLabel
from FormElementsLibrary import FormElementsLibrary

class FormBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setAcceptDrops(True)

        self.library = FormElementsLibrary()
        self.library.setWindowTitle("elements library")
    
    def closeEvent(self, event):
        self.library.close()
        event.accept()
        
    def show(self):
        super().show()
        self.library.show()