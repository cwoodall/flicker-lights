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
        zoomInFactor = 1.1
        zoomOutFactor = 1 / zoomInFactor

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())

        # Zoom
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        print(self.currentScale)
        if ((self.currentScale * zoomFactor)>= 1):
            print (self.currentScale)
            self.currentScale *= zoomFactor
            self.scale(zoomFactor, 1)
