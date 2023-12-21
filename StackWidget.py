from typing import Optional
from PySide6.QtGui import QPaintEvent, QPainter, QPen, QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import QWidget, QBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QSize
from mimeData.LibElementMimeData import LibElementMimeData
from mimeData.MoveWidgetMimeData import MoveWidgetMimeData

class StackWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        from LibElementFactory import LibElementFactory
        self.libFactory = LibElementFactory()
        self.boxLayout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.setLayout(self.boxLayout)
        self.setAcceptDrops(True)

    def addArrangedWidget(self, wgt: QWidget):
        self.boxLayout.addWidget(wgt)
        wgt.show()
    
    def sizeHint(self) -> QSize:
        if self.boxLayout.count() == 0:
            return QSize(100, 50)
        else:
            return super().sizeHint()
    
    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        pen = QPen(Qt.gray, 1, Qt.DashLine)
        painter.setPen(pen)
        painter.drawRect(self.rect().adjusted(1,1,-1,-1))

    ############################
    # Drop
    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if isinstance(event.mimeData(), LibElementMimeData):
            event.acceptProposedAction()
        if isinstance(event.mimeData(), MoveWidgetMimeData):
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        event.accept()
        widget: QWidget
        if isinstance(event.mimeData(), LibElementMimeData):
            widget = self.libFactory.widgetFor(event.mimeData().elementType)
        if isinstance(event.mimeData(), MoveWidgetMimeData):
            widget = event.mimeData().widget
        if widget is None:
            return
        self.addArrangedWidget(widget)
        self.adjustSize()