from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit
from PySide6.QtGui import QDragMoveEvent, QDrag, QMouseEvent, QPixmap, QScreen
from PySide6.QtCore import Qt, QMimeData
from enum import Enum
import res.LibElementIcons_rc as LibElementIcons_rc
from LibElementMimeData import *

class FormElementsLibrary(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(200, 300)
        layout = QVBoxLayout()

        label_icon = QPixmap(":/libElements/labelIcon.png")
        self.label_icon_label = QLabel()
        self.label_icon_label.setPixmap(label_icon)
        layout.addWidget(self.label_icon_label)

        line_edit_icon = QPixmap(":/libElements/lineEditIcon.png")
        self.line_edit_icon_label = QLabel()
        self.line_edit_icon_label.setPixmap(line_edit_icon)
        layout.addWidget(self.line_edit_icon_label)

        layout.addStretch(1)

        self.setLayout(layout)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.saveDragStartPos(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.canStartDrag(event) :
            self.startDrag()

    #################################
    # Drag and Drop
    def saveDragStartPos(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton :
            self._dragStartPos = event.pos()

    def canStartDrag(self, event: QMouseEvent) -> bool:
        result: bool = False
        if (event.buttons() & Qt.MouseButton.LeftButton) and (self._dragStartPos is not None):
            distance = (event.pos() - self._dragStartPos).manhattanLength()
            if distance > QApplication.startDragDistance() :
                result = True
        return result

    def startDrag(self):
        drag = QDrag(self)
        mimeData: LibElementMimeData = None
        pixmap: QPixmap = None
        if self.label_icon_label.geometry().contains(self._dragStartPos):
            mimeData = LibElementMimeData(LibElementType.LABEL)
            pixmap = self.newLabelPixmap()
        if self.line_edit_icon_label.geometry().contains(self._dragStartPos):
            mimeData = LibElementMimeData(LibElementType.TEXT_INPUT)
            pixmap = self.newLineEditPixmap()
        if pixmap is None or mimeData is None:
            return
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        dropAction = drag.exec(Qt.DropAction.CopyAction) 
        print("start drag")
    #################################

    # utility
    def newLabelPixmap(self) -> QPixmap:
        label = QLabel()
        label.setGeometry(0, 0, 50, 15)
        label.setStyleSheet("QLabel { background-color : transparent; color : black; }")
        label.setText("label")
        return label.grab()
    
    def newLineEditPixmap(self) -> QPixmap:
        lineEdit = QLineEdit()
        lineEdit.setGeometry(0, 0, 60, 15)
        return lineEdit.grab()