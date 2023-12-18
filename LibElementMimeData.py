from enum import Enum
from PySide6.QtCore import QMimeData

class LibElementType(Enum):
    LABEL = "LABEL"
    TEXT_INPUT = "TEXT_INPUT"

class LibElementMimeData(QMimeData):
    def __init__(self, type: LibElementType) -> None:
        super().__init__()
        self.elementType = type
        