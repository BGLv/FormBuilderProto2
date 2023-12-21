from PySide6.QtGui import QPaintEvent, QPainter, QPen
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QSize

class StackWidget(QWidget):
    def sizeHint(self) -> QSize:
        return QSize(100, 50)
    
    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        pen = QPen(Qt.gray, 1, Qt.DashLine)
        painter.setPen(pen)
        painter.drawRect(self.rect().adjusted(1,1,-1,-1))