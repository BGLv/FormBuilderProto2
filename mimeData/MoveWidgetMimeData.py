from PySide6.QtCore import QMimeData
from PySide6.QtWidgets import QWidget

class MoveWidgetMimeData(QMimeData):
    def setWidget(self, wgt: QWidget):
        self.widget = wgt