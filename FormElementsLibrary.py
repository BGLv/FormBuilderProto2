from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
import res.LibElementIcons_rc as LibElementIcons_rc

class FormElementsLibrary(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(200, 300)
        layout = QVBoxLayout()

        label_icon = QPixmap(":/libElements/labelIcon.png")
        label_icon_label = QLabel()
        label_icon_label.setPixmap(label_icon)
        layout.addWidget(label_icon_label)

        line_edit_icon = QPixmap(":/libElements/lineEditIcon.png")
        line_edit_icon_label = QLabel()
        line_edit_icon_label.setPixmap(line_edit_icon)
        layout.addWidget(line_edit_icon_label)

        layout.addStretch(1)

        self.setLayout(layout)
