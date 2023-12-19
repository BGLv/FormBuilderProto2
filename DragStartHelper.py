from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Qt

class DragStartHelper:
    def saveDragStartPos(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton :
            self.dragStartPos = event.pos()

    def canStartDrag(self, event: QMouseEvent) -> bool:
        result: bool = False
        if (event.buttons() & Qt.MouseButton.LeftButton) and (self.dragStartPos is not None):
            distance = (event.pos() - self.dragStartPos).manhattanLength()
            if distance > QApplication.startDragDistance() :
                result = True
        return result