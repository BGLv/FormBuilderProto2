from PySide6.QtGui import QDragEnterEvent, QDropEvent, QMouseEvent
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit
from FormElementsLibrary import FormElementsLibrary
from LibElementMimeData import *
from DragStartHelper import *

class FormBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setAcceptDrops(True)

        self.library = FormElementsLibrary()
        self.library.setWindowTitle("elements library")
        self.dragStartHelper = DragStartHelper()

    #####################################
    # Lifecycle
    def closeEvent(self, event):
        self.library.close()
        event.accept()
        
    def show(self):
        super().show()
        self.library.show()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.dragStartHelper.saveDragStartPos(event)
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
    
    ######## we can drag widget which are currently on canvas
    

    

    #####################################