import sys
import yaml
from PyQt5 import QtCore, QtGui, QtWidgets
from lightshow_gui import Ui_MainWindow

class graphicsItem (QtWidgets.QGraphicsItem):
    def __init__ (self):
        super(graphicsItem, self).__init__()
        self.rectF = QtCore.QRectF(0,0,10,100)
        self.boundingRect = QtCore.QRectF(-5,0,15,100)

    def boundingRect (self):
        return self.boundingRect

    def paint (self, painter=None, style=None, widget=None):
        painter.fillRect(self.rectF, QtCore.Qt.red)
    def mousePressEvent(self, event):
        super(graphicsItem, self).mousePressEvent(event)
        print ("YOU CLICKED ME!")

class MyGraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self):
        QtWidgets.QGraphicsScene.__init__(self)
        # self.setMouseTracking(True)

    def mousePressEvent(self, event):
        super(MyGraphicsScene, self).mousePressEvent(event)
        a = self.items(event.scenePos())
        if not a:
            item = graphicsItem()

            position = QtCore.QPointF(event.scenePos()) - item.rectF.center()
            item.setPos(position.x() + 5, 0)
            self.addItem(item)
class LightshowProgram(Ui_MainWindow):
    def __init__(self, window):
        Ui_MainWindow.__init__(self)
        self.setupUi(window)

        # self.setMouseTracking(True)

        self.scene = MyGraphicsScene()
        # self.scene.setSceneRect(0,0,900,900)
        self.testCanvas.setScene(self.scene)
        self.testCanvas.setSceneRect(0,0,1000,100)

        # self.testCanvas.fitInView(self.scene.sceneRect())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    prog = LightshowProgram(window)

    window.show()

    sys.exit(app.exec_())
