from PySide6.QtGui import QDrag, QDragMoveEvent, QPaintEvent, QPixmap, QDragEnterEvent, QDropEvent, QMouseEvent, QPainter, QPen
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit
from PySide6.QtCore import Qt, QRect, QSize, QFile, QTextStream, QXmlStreamWriter
from FormElementsLibrary import FormElementsLibrary
from metaClasses.SingletonMeta import SingletonMeta
from mimeData.LibElementMimeData import *
from mimeData.MoveWidgetMimeData import *
from DragStartHelper import *
from PySide6.QtXml import QDomDocument, QDomElement

class FormStorage(metaclass=SingletonMeta):
    def saveGeometry(self, geometry: QRect):
        print("geom saved")

class FormBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.formStorage = FormStorage()
        self.cachedElementSize = {}
        self.dropPlaceRect = None
        self.resize(400, 400)
        self.setAcceptDrops(True)

        self.library = FormElementsLibrary()
        self.library.setWindowTitle("elements library")
        self.dragStartHelper = DragStartHelper()
        self.restoreBuilderState()

    #####################################
    # Lifecycle
    def closeEvent(self, event):
        self.library.close()
        self.saveBuilderState()
        event.accept()
        
    def show(self):
        super().show()
        self.library.show()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.dragStartHelper.saveDragStartPos(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.dragStartHelper.canStartDrag(event):
            widgetToDrag = self.widgetToDrag()
            if widgetToDrag is not None:
                self.startDrag(widgetToDrag)

    def paintEvent(self, event: QPaintEvent) -> None:
        if self.dropPlaceRect is not None:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            pen = QPen(Qt.black, 2, Qt.DashLine)
            painter.setPen(pen)
            painter.drawRect(self.dropPlaceRect)

    #####################################
    # Drag and Drop
    def startDrag(self, widget: QWidget):
        widget.setParent(None)
        drag = QDrag(self)
        mimeData = MoveWidgetMimeData()
        mimeData.setWidget(widget)
        pixmap: QPixmap = widget.grab()
        if pixmap is None or mimeData is None:
            return
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        dropAction = drag.exec(Qt.DropAction.MoveAction)             
    
    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if isinstance(event.mimeData(), LibElementMimeData):
            event.acceptProposedAction()
        if isinstance(event.mimeData(), MoveWidgetMimeData):
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        event.accept()
        self.updateDropPlaceRectFor(event)

    def dropEvent(self, event: QDropEvent) -> None:
        event.accept()
        widget: QWidget
        if isinstance(event.mimeData(), LibElementMimeData):
            widget = self.widgetFor(event.mimeData())
        if isinstance(event.mimeData(), MoveWidgetMimeData):
            widget = event.mimeData().widget
        if widget is None:
            return
        widget.move(event.pos())
        widget.setParent(self)
        widget.show()
        self.hideDropPlaceRect()

    def widgetFor(self, mimeData: LibElementMimeData) -> QWidget:
        result = None
        match mimeData.elementType:
            case LibElementType.LABEL:
                result = QLabel()
                result.setText("test label")
            case LibElementType.TEXT_INPUT:
                result = QLineEdit()
                result.setReadOnly(True)
                result.setEnabled(False)
        return result
    
    def widgetToDrag(self) -> QWidget:
        return self.childAt(self.dragStartHelper.dragStartPos)
    
    # Drop place hint rectangle
    def updateDropPlaceRectFor(self, event: QDragMoveEvent):
        size: QSize
        if isinstance(event.mimeData(), LibElementMimeData):
            mimeData: LibElementMimeData = event.mimeData()
            if mimeData.elementType in self.cachedElementSize:
                size = self.cachedElementSize[mimeData.elementType]
            else:
                size = self.calculateDropPlaceSizeFrom(mimeData)
                self.cachedElementSize[mimeData.elementType] = size
     
        if isinstance(event.mimeData(), MoveWidgetMimeData):
            widget = event.mimeData().widget
            size = widget.size()
        
        if size is None:
            self.dropPlaceRect = None
        else:
            self.dropPlaceRect = QRect(event.pos(), size)
        self.update()


    def calculateDropPlaceSizeFrom(self, mimeData: LibElementMimeData):
        widget = self.widgetFor(mimeData)
        widget.setParent(self)
        widget.show()
        size = widget.size()
        widget.setParent(None)
        return size

    def hideDropPlaceRect(self):
        self.dropPlaceRect = None
        self.update()
    
    #####################################
        
    ####################################
    # Save
    def saveBuilderState(self):
        domDocument = QDomDocument()
        window = domDocument.createElement("window")
        self.appendGeometryAttributesTo(window, self.geometry())
        domDocument.appendChild(window)
        for widget in self.children():
            if isinstance(widget, QLabel):
                labelDom = domDocument.createElement("label") 
                self.appendGeometryAttributesTo(labelDom, widget.geometry())
                window.appendChild(labelDom)
            if isinstance(widget, QLineEdit):
                lineEditDom = domDocument.createElement("lineEdit")
                self.appendGeometryAttributesTo(lineEditDom, widget.geometry())
                window.appendChild(lineEditDom)
        
        fileName = "form.xml"
        file = QFile(fileName)
        if file.open(QFile.WriteOnly | QFile.Text):
            text_stream = QTextStream(file)
            domDocument.save(text_stream, 4)
            file.close()

        
        #self.formStorage.saveGeometry(self.geometry())
    def appendGeometryAttributesTo(self, window: QDomElement, geometry: QRect):
        window.setAttribute("x", geometry.x())
        window.setAttribute("y", geometry.y())
        window.setAttribute("width", geometry.width())
        window.setAttribute("height", geometry.height())

    ####################################
    # restore
    def restoreBuilderState(self):
        fileName = "form.xml"
        file = QFile(fileName)
        domDocument = QDomDocument()
        if file.open(QFile.ReadOnly | QFile.Text):
            if domDocument.setContent(file):
                root = domDocument.documentElement()
                self.setGeometry(
                    int(root.attribute("x")),
                    int(root.attribute("y")),
                    int(root.attribute("width")),
                    int(root.attribute("height"))
                )