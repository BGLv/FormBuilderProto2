from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QDragMoveEvent, QMouseEvent, QPixmap
from PySide6.QtCore import Qt
from enum import Enum
import res.LibElementIcons_rc as LibElementIcons_rc

class LibElement(Enum):
    LABEL = "LABEL"
    TEXT_INPUT = "TEXT_INPUT"


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
        if event.button() == Qt.LeftButton :
            self._dragStartPos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if (event.buttons() & Qt.LeftButton) and (self._dragStartPos is not None):
            distance = (event.pos() - self._dragStartPos).manhattanLength()
            if distance > QApplication.startDragDistance() :
                self.startDrag()

    def startDrag(self):
        print("start drag")