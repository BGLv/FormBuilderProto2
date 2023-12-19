from PySide6.QtGui import QDrag, QDragMoveEvent, QPaintEvent, QPixmap, QDragEnterEvent, QDropEvent, QMouseEvent, QPainter, QPen
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit
from PySide6.QtCore import Qt, QRect, QSize
from FormElementsLibrary import FormElementsLibrary
from mimeData.LibElementMimeData import *
from mimeData.MoveWidgetMimeData import *
from DragStartHelper import *

class FormBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.dropPlaceRect = None
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

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.dragStartHelper.canStartDrag(event):
            widgetToDrag = self.widgetToDrag()
            if widgetToDrag is not None:
                self.startDrag(widgetToDrag)

    def paintEvent(self, event: QPaintEvent) -> None:
        if self.dropPlaceRect is not None:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            pen = QPen(Qt.black, 2, Qt.DashLine)
            painter.setPen(pen)
            painter.drawRect(self.dropPlaceRect)


    ####################################

    #####################################
    # Drag and Drop
    def startDrag(self, widget: QWidget):
        widget.setParent(None)
        drag = QDrag(self)
        mimeData = MoveWidgetMimeData()
        mimeData.setWidget(widget)
        pixmap: QPixmap = widget.grab()
        if pixmap is None or mimeData is None:
            return
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        dropAction = drag.exec(Qt.DropAction.MoveAction)             
    
    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if isinstance(event.mimeData(), LibElementMimeData):
            event.acceptProposedAction()
        if isinstance(event.mimeData(), MoveWidgetMimeData):
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        event.accept()
        if isinstance(event.mimeData(), LibElementMimeData):
            widget = self.widgetFor(event.mimeData())
            widget.setParent(self)
            widget.show()
            self.dropPlaceRect = QRect(event.pos(), widget.size())
            widget.setParent(None)
        if isinstance(event.mimeData(), MoveWidgetMimeData):
            widget = event.mimeData().widget
            self.dropPlaceRect = QRect(event.pos(), widget.size())
        if widget is None:
            self.dropPlaceRect = None
        self.update()

    def hideDropPlaceRect(self):
        self.dropPlaceRect = None
        self.update()


    def dropEvent(self, event: QDropEvent) -> None:
        event.accept()
        widget: QWidget
        if isinstance(event.mimeData(), LibElementMimeData):
            widget = self.widgetFor(event.mimeData())
        if isinstance(event.mimeData(), MoveWidgetMimeData):
            widget = event.mimeData().widget
        if widget is None:
            return
        widget.move(event.pos())
        widget.setParent(self)
        widget.show()
        self.hideDropPlaceRect()

    def widgetFor(self, mimeData: LibElementMimeData) -> QWidget:
        result = None
        match mimeData.elementType:
            case LibElementType.LABEL:
                result = QLabel()
                result.setText("test label")
            case LibElementType.TEXT_INPUT:
                result = QLineEdit()
                result.setReadOnly(True)
                result.setEnabled(False)
        return result
    
    def widgetToDrag(self) -> QWidget:
        return self.childAt(self.dragStartHelper.dragStartPos)
    
    #####################################