from PyQt5 import QtCore, QtGui, QtWidgets

class MyGraphicsView(QtWidgets.QGraphicsView):

    def __init__(self, parent):
        QtWidgets.QGraphicsView.__init__(self, parent)
        self.setMouseTracking(True)
        self.currentScale = 1

    def wheelEvent(self, event):
        """
        Zoom in or out of the view.
        """
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            zoomInFactor = 1.1
            zoomOutFactor = 1 / zoomInFactor

            # Save the scene pos
            oldPos = self.mapToScene(event.pos())

            # Zoom
            if event.angleDelta().y() > 0:
                zoomFactor = zoomInFactor
            else:
                zoomFactor = zoomOutFactor

            if ((self.currentScale * zoomFactor)>= 1) and (self.currentScale * zoomFactor <= 100):
                self.currentScale *= zoomFactor
                self.scale(zoomFactor, 1)
        else:
            if event.angleDelta().y() > 0:
                dx = 25
            else:
                dx = -25

            x = self.horizontalScrollBar().value()
            self.horizontalScrollBar().setValue(x + dx)
