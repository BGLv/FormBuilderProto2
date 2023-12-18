from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt, QMimeData
from FormElementsLibrary import FormElementsLibrary
from LibElementMimeData import *

class FormBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setAcceptDrops(True)

        self.library = FormElementsLibrary()
        self.library.setWindowTitle("elements library")

    #####################################
    # Lifecycle
    def closeEvent(self, event):
        self.library.close()
        event.accept()
        
    def show(self):
        super().show()
        self.library.show()
    ####################################

    #####################################
    # Drag and Drop
    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if isinstance(event.mimeData(), LibElementMimeData):
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        return super().dropEvent(event)
    #####################################