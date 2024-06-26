from PySide6.QtGui import QDrag, QDragMoveEvent, QPaintEvent, QPixmap, QDragEnterEvent, QDragLeaveEvent, QDropEvent, QMouseEvent, QPainter, QPen
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit
from PySide6.QtCore import Qt, QRect, QPoint, QSize, QFile, QTextStream, QXmlStreamWriter
from FormElementSelectionHelper import FormElementSelectionHelper
from FormElementsLibrary import FormElementsLibrary
from LibElementFactory import LibElementFactory
from StackWidget import StackWidget
from metaClasses.SingletonMeta import SingletonMeta
from mimeData.LibElementMimeData import *
from mimeData.MoveWidgetMimeData import *
from DragStartHelper import *
from PySide6.QtXml import QDomDocument, QDomElement, QDomNode

class FormStorage(metaclass=SingletonMeta):
    def saveGeometry(self, geometry: QRect):
        print("geom saved")

class FormBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.formStorage = FormStorage()
        self.libFactory = LibElementFactory()
        self.cachedElementSize = {}
        self.dropPlaceRect = None
        self.selectionHelper = FormElementSelectionHelper()
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
        libXPos = self.geometry().topRight().x() + 5
        libYPos = self.geometry().topRight().y()
        self.library.move(QPoint(libXPos, libYPos))
        self.library.show()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.dragStartHelper.saveDragStartPos(event)
        self.selectionHelper.handleMousePressEvent(self, event)
        self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.dragStartHelper.canStartDrag(event):
            widgetToDrag = self.widgetToDrag()
            if widgetToDrag is not None:
                self.startDrag(widgetToDrag)

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Delete, Qt.Key_Backspace] and self.selectionHelper.selectedWidget is not None:
           self.selectionHelper.removeSelected()
           self.update()
        if event.key() == Qt.Key.Key_V and isinstance(self.selectionHelper.selectedWidget, StackWidget):
            self.selectionHelper.selectedWidget.setAxis(StackWidget.Axis.VERTICAL)
            self.update()
        if event.key() == Qt.Key.Key_H and isinstance(self.selectionHelper.selectedWidget, StackWidget):
            self.selectionHelper.selectedWidget.setAxis(StackWidget.Axis.HORIZONTAL)
            self.update()
        super().keyPressEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.handleDropPlaceRectDrawing(painter)
        self.selectionHelper.handleSelectedWidgetDrawing(painter)

    ####################################
    # drawing
    def handleDropPlaceRectDrawing(self, painter: QPainter):
        if self.dropPlaceRect is not None:
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

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.hideDropPlaceRect()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        event.accept()
        self.updateDropPlaceRectFor(event)

    def dropEvent(self, event: QDropEvent) -> None:
        event.accept()
        widget: QWidget
        if isinstance(event.mimeData(), LibElementMimeData):
            widget = self.libFactory.widgetFor(event.mimeData().elementType)
        if isinstance(event.mimeData(), MoveWidgetMimeData):
            widget = event.mimeData().widget
        if widget is None:
            return
        widget.move(event.pos())
        widget.setParent(self)
        widget.show()
        self.hideDropPlaceRect()
    
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
        widget = self.libFactory.widgetFor(mimeData.elementType)
        if widget is None:
            return
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
            self.storeWidgetToDomElement(widget, window, domDocument)
            
        fileName = "form.xml"
        file = QFile(fileName)
        if file.open(QFile.WriteOnly | QFile.Text):
            text_stream = QTextStream(file)
            domDocument.save(text_stream, 4)
            file.close()

    def storeWidgetToDomElement(self, widget: QWidget, domElement: QDomElement, domDocument: QDomDocument):
        if isinstance(widget, QLabel):
            labelDom = domDocument.createElement("label") 
            self.appendGeometryAttributesTo(labelDom, widget.geometry())
            domElement.appendChild(labelDom)
        if isinstance(widget, QLineEdit):
            lineEditDom = domDocument.createElement("lineEdit")
            self.appendGeometryAttributesTo(lineEditDom, widget.geometry())
            domElement.appendChild(lineEditDom)
        if isinstance(widget, StackWidget):
            stackDom = domDocument.createElement("stackWidget")
            stackDom.setAttribute("x", widget.geometry().x())
            stackDom.setAttribute("y", widget.geometry().y())
            stackDom.setAttribute("axis", widget.axis().value)
            domElement.appendChild(stackDom)
            for child in widget.arrangedWidgets():
                if isinstance(child, QWidget):
                    self.storeWidgetToDomElement(child, stackDom, domDocument)
    
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
                self.restoreWidgetGeometry(self, root)
                self.restoreFromDomElementAsChildOf(root, self)
                

    def restoreFromDomElementAsChildOf(self, root: QDomElement, parent: QWidget):
        childNodes = root.childNodes()
        for i in range(childNodes.count()):
            element = childNodes.item(i).toElement()
            widget = None
            if element is None:
                return
            if element.nodeName() == "label":
                widget = self.libFactory.widgetFor(LibElementType.LABEL)
                self.restoreWidgetGeometry(widget, element)
            if element.nodeName() == "lineEdit":
                widget = self.libFactory.widgetFor(LibElementType.TEXT_INPUT)
                self.restoreWidgetGeometry(widget, element)
            if element.nodeName() == "stackWidget":
                widget = self.libFactory.widgetFor(LibElementType.STACK)
                self.restoreWidgetOrigin(widget, element)
                self.restoreWidgetAxis(widget, element)
                self.restoreFromDomElementAsChildOf(element, widget)
            if isinstance(parent, StackWidget):
                parent.addArrangedWidget(widget)
            else:
                widget.setParent(parent)
                

    def restoreWidgetOrigin(self, widget: QWidget, domElement: QDomElement):
        try:
            widget.move(
                int(domElement.attribute("x", str(widget.geometry().x()))),
                int(domElement.attribute("y", str(widget.geometry().y()))),
            )
        except ValueError as e:
            pass 

    def restoreWidgetAxis(self, widget: QWidget, domElement: QDomElement):
        try:
            allowedAxis = [StackWidget.Axis.HORIZONTAL.value, StackWidget.Axis.VERTICAL.value]
            if domElement.attribute("axis") in allowedAxis:
                widget.setAxis(StackWidget.Axis[domElement.attribute("axis")])
        except AttributeError as e:
            pass
        except ValueError as e:
            pass
                    
    def restoreWidgetGeometry(self, widget: QWidget, domElement: QDomElement):
        try:
            widget.setGeometry(
                int(domElement.attribute("x", str(widget.geometry().x()))),
                int(domElement.attribute("y", str(widget.geometry().y()))),
                int(domElement.attribute("width", str(widget.geometry().width()))),
                int(domElement.attribute("height", str(widget.geometry().height())))
            )
        except ValueError as e:
            pass             