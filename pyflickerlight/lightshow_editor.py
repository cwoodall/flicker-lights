import sys
import yaml
from PyQt5 import QtCore, QtGui, QtWidgets
from lightshow_gui import Ui_MainWindow
import math

class graphicsItem (QtWidgets.QGraphicsItem):
    def __init__ (self):
        super(graphicsItem, self).__init__()
        self.rectF = QtCore.QRectF(0,0,9,60)

    def boundingRect (self):
        return self.rectF

    def paint (self, painter=None, style=None, widget=None):
        painter.fillRect(self.rectF, QtCore.Qt.green)

    def mousePressEvent(self, event):
        super(graphicsItem, self).mousePressEvent(event)
        print ("YOU CLICKED ME!")

class MyGraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self):
        QtWidgets.QGraphicsScene.__init__(self)
        # self.setMouseTracking(True)

    def drawBackground(self, painter, rect):
        QtWidgets.QGraphicsScene.drawBackground(self, painter, rect)
        print (rect.left(), rect.right())
        n = 10
        major = n*10
        cur_pos = math.ceil(rect.left()/n)*n
        while cur_pos < rect.right():
            if not int(cur_pos)%major:
                painter.setPen(QtGui.QPen(QtGui.QColor(50,50,50,125)))
                painter.drawLine(cur_pos, 0, cur_pos, 15)
                painter.drawLine(cur_pos, 100, cur_pos, 100-15)

            else:
                painter.setPen(QtGui.QPen(QtGui.QColor(100,100,100,125)))
                painter.drawLine(cur_pos, 0, cur_pos, 10)
                painter.drawLine(cur_pos, 100, cur_pos, 100-10)

            cur_pos += n

    def mousePressEvent(self, event):
        n = 10
        super(MyGraphicsScene, self).mousePressEvent(event)
        item = graphicsItem()
        position = QtCore.QPointF(event.scenePos())
        item.setPos(math.floor((position.x()/n)) * n, 20)
        a = self.collidingItems(item, QtCore.Qt.IntersectsItemShape)

        print(a)
        if not a:
            print("adding")
            self.addItem(item)
        else:
            print("collision")

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
