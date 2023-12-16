from PySide6.QtWidgets import QWidget, QLabel

class FormBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setAcceptDrops(True)

        self.label = QLabel()
        self.label.setWindowTitle("just label")
    
    def closeEvent(self, event):
        self.label.close()
        event.accept()
        
    
    def show(self):
        super().show()
        self.label.show()