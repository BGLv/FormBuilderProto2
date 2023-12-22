from typing import Optional
from enum import Enum
from PySide6.QtGui import QPaintEvent, QPainter, QPen, QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import QWidget, QBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QSize, QChildEvent
from mimeData.LibElementMimeData import LibElementMimeData
from mimeData.MoveWidgetMimeData import MoveWidgetMimeData

class StackWidget(QWidget):
    class Axis(Enum):
        HORIZONTAL = "HORIZONTAL"
        VERTICAL = "VERTICAL"

    def __init__(self) -> None:
        super().__init__()
        from LibElementFactory import LibElementFactory
        self.libFactory = LibElementFactory()
        self.boxLayout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self._axis = StackWidget.Axis.VERTICAL
        self.setLayout(self.boxLayout)
        self.setAcceptDrops(True)

    def axis(self) -> Axis:
        return self._axis
    
    def setAxis(self, axis: Axis):
        self._axis = axis
        match axis:
            case StackWidget.Axis.HORIZONTAL:
                self.boxLayout.setDirection(QBoxLayout.Direction.LeftToRight)
            case StackWidget.Axis.VERTICAL:
                self.boxLayout.setDirection(QBoxLayout.Direction.TopToBottom)
        self.adjustSize()

    def addArrangedWidget(self, wgt: QWidget):
        self.boxLayout.addWidget(wgt)
        wgt.show()

    def arrangedWidgets(self) -> [QWidget]:
        result = []
        for i in range(self.boxLayout.count()):
            item = self.boxLayout.itemAt(i)
            if item.widget():
                result.append(item.widget())
        return result
    
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

    ################################################
    # for correct sizing by adding or removing sub widgets
    def childEvent(self, event: QChildEvent) -> None:
        self.adjustSize()
        return super().childEvent(event)
    
    def adjustSize(self) -> None:
        super().adjustSize()
        if isinstance(self.parent(), StackWidget):
            self.parent().adjustSize()
    ################################################

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