from PySide6.QtGui import QMouseEvent, QPainter, QPen
from PySide6.QtCore import Qt, QRect
from PySide6.QtWidgets import QWidget

class FormElementSelectionHelper:
    def __init__(self) -> None:
        self.selectedWidget = None

    def handleMousePressEvent(self, eventTarget: QWidget, event: QMouseEvent) -> None:
        self.selectedWidget = None
        if event.button() == Qt.MouseButton.LeftButton :
            widgetAtPos = eventTarget.childAt(event.pos())
            if widgetAtPos is not None:
                self.selectedWidget = widgetAtPos

    def removeSelected(self):
        self.selectedWidget.setParent(None)
        self.selectedWidget = None

    def handleSelectedWidgetDrawing(self, painter: QPainter):
        if self.selectedWidget is not None and self.selectedWidget.parent() is not None:
           pen = QPen(Qt.blue, 1, Qt.SolidLine)
           painter.setPen(pen)
           rootParent = self.rootParentOf(self.selectedWidget)
           origin = self.selectedWidget.parent().mapTo(rootParent, self.selectedWidget.geometry().topLeft())
           selectionRect = QRect(origin, self.selectedWidget.geometry().size())
           painter.drawRect(selectionRect)

    def rootParentOf(self, widget: QWidget) -> QWidget:
        result: QWidget = widget.parentWidget()
        tmpParent = result
        while tmpParent is not None:
            result = tmpParent
            tmpParent = tmpParent.parentWidget()
        return result