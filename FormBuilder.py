from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit
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
        if not isinstance(event.mimeData(), LibElementMimeData):
            return
        widget = self.widgetFor(event.mimeData())
        widget.move(event.pos())
        widget.setParent(self)
        widget.show()

    def widgetFor(self, mimeData: LibElementMimeData) -> QWidget:
        result = None
        match mimeData.elementType:
            case LibElementType.LABEL:
                result = QLabel()
                result.setText("test label")
            case LibElementType.TEXT_INPUT:
                result = QLineEdit()
                result.setReadOnly(True)
        return result
    #####################################