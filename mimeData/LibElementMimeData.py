from PySide6.QtCore import QMimeData
from LibElementType import LibElementType

class LibElementMimeData(QMimeData):
    def __init__(self, type: LibElementType) -> None:
        super().__init__()
        self.elementType = type
        