from PySide6.QtWidgets import QWidget, QLabel, QLineEdit
from LibElementType import LibElementType
from StackWidget import StackWidget

class LibElementFactory:
    def widgetFor(self, elementType: LibElementType) -> QWidget:
        result = None
        match elementType:
            case LibElementType.LABEL:
                result = QLabel()
                result.setText("test label")
            case LibElementType.TEXT_INPUT:
                result = QLineEdit()
                result.setReadOnly(True)
                result.setEnabled(False)
            case LibElementType.STACK:
                result = StackWidget()
        return result