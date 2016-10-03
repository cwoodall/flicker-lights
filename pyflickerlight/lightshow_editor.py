import sys
import yaml
from PyQt5 import QtCore, QtGui, QtWidgets
from lightshow_gui import Ui_MainWindow
import math

class FlickerLightItem(QtWidgets.QGraphicsItem):
    def __init__ (self, color):
        super(FlickerLightItem, self).__init__()
        self.boundingRectF = QtCore.QRectF(0,0,10,30)

        self.rectF = QtCore.QRectF(1,0,8,30)
        self.color = color

    def boundingRect (self):
        return self.boundingRectF

    def paint (self, painter=None, style=None, widget=None):
        painter.fillRect(self.rectF, self.color)

    def mousePressEvent(self, event):
        super(FlickerLightItem, self).mousePressEvent(event)
        print ("YOU CLICKED ME!")

class TickPainter(object):
    def __init__(self, tickDistance, numTicksPerMajorTick, minorLen=5, majorLen=8, tickColor=QtGui.QColor(50,50,50,125)):
        self.tickDistance = tickDistance
        self.numTicksPerMajorTick = numTicksPerMajorTick
        self.minorLen = minorLen
        self.majorLen = majorLen
        self.changeColor(tickColor)

    def changeColor(self, color):
        self.tickPen = QtGui.QPen(color)

    def getGridPosition(self, rect):
        cur_pos = math.ceil(rect.left()/self.tickDistance)*self.tickDistance
        return cur_pos

    def getPosition(self, p):
        cur_pos = math.floor(p.x()/self.tickDistance)*self.tickDistance
        return cur_pos

    def isMajorTick(self, pos):
        return not (pos % (self.tickDistance * self.numTicksPerMajorTick))

    def drawTick(self, painter, pos, isMajor=False):
        painter.setPen(self.tickPen)
        dist = 5
        if isMajor:
            dist = 8
        painter.drawLine(pos, 0, pos, dist)

    def draw(self, painter, rect):
        cur_pos = self.getGridPosition(rect)
        while cur_pos < rect.right():
            self.drawTick(painter, cur_pos, self.isMajorTick(cur_pos))
            cur_pos += self.tickDistance

class MyGraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self):
        QtWidgets.QGraphicsScene.__init__(self)
        self.tickPainter = TickPainter(10, 10)
        self.currentColor = QtGui.QColor(0,0,0,255)
    def drawBackground(self, painter, rect):
        QtWidgets.QGraphicsScene.drawBackground(self, painter, rect)
        self.tickPainter.draw(painter, rect)

    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Tab:
            color = QtWidgets.QColorDialog.getColor()
            self.currentColor = color
            print(color)
            print(self.items())
            return False
        return QtWidgets.QGraphicsScene.event(self, event)

    def mousePressEvent(self, event):
        super(MyGraphicsScene, self).mousePressEvent(event)
        item = FlickerLightItem(self.currentColor)
        position = QtCore.QPointF(event.scenePos())
        item.setPos(self.tickPainter.getPosition(position), 10)
        collidingItems = self.collidingItems(item, QtCore.Qt.IntersectsItemShape)
        if not collidingItems:
            self.addItem(item)
        else:
            for collidingItem in collidingItems:
                self.removeItem(collidingItem)

class LightshowProgram(Ui_MainWindow):
    def __init__(self, window):
        Ui_MainWindow.__init__(self)
        self.setupUi(window)
        self.songLength = 60*1
        self.timePerTick = .01
        self.tickDistance = 10

        self.sceneLength = self.tickDistance * (self.songLength/self.timePerTick)
        self.scene = MyGraphicsScene()
        self.testCanvas.setScene(self.scene)
        self.testCanvas.setSceneRect(0,0,self.sceneLength,50)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    prog = LightshowProgram(window)

    window.show()

    sys.exit(app.exec_())
