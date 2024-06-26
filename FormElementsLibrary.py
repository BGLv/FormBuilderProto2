from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit
from PySide6.QtGui import QDrag, QMouseEvent, QPixmap
from PySide6.QtCore import Qt
from StackWidget import StackWidget
import res.LibElementIcons_rc as LibElementIcons_rc
from mimeData.LibElementMimeData import *
from DragStartHelper import *

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

        self.stack_widget_icon_label = QLabel()
        self.stack_widget_icon_label.setText("StackWidget")
        layout.addWidget(self.stack_widget_icon_label)

        layout.addStretch(1)

        self.setLayout(layout)
        self.dragStartHelper = DragStartHelper()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.dragStartHelper.saveDragStartPos(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.dragStartHelper.canStartDrag(event) :
            self.startDrag()

    #################################
    # Drag and Drop
    def startDrag(self):
        drag = QDrag(self)
        mimeData: LibElementMimeData = None
        pixmap: QPixmap = None
        if self.label_icon_label.geometry().contains(self.dragStartHelper.dragStartPos):
            mimeData = LibElementMimeData(LibElementType.LABEL)
            pixmap = self.newLabelPixmap()
        if self.line_edit_icon_label.geometry().contains(self.dragStartHelper.dragStartPos):
            mimeData = LibElementMimeData(LibElementType.TEXT_INPUT)
            pixmap = self.newLineEditPixmap()
        if self.stack_widget_icon_label.geometry().contains(self.dragStartHelper.dragStartPos):
            mimeData = LibElementMimeData(LibElementType.STACK)
            pixmap = self.newStackPixmap()
        if pixmap is None or mimeData is None:
            return
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        dropAction = drag.exec(Qt.DropAction.CopyAction)
    #################################

    # utility
    def newLabelPixmap(self) -> QPixmap:
        label = QLabel()
        label.setStyleSheet("QLabel { background-color : transparent; color : black; }")
        label.setText("label")
        return label.grab()
    
    def newLineEditPixmap(self) -> QPixmap:
        lineEdit = QLineEdit()
        return lineEdit.grab()
    
    def newStackPixmap(self) -> QPixmap:
        stack = StackWidget()
        return stack.grab()