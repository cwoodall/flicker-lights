import sys
import yaml
from PyQt5 import QtCore, QtGui, QtWidgets
from lightshow_gui import Ui_MainWindow
import math

class FlickerLightItem(QtWidgets.QGraphicsItem):
    def __init__ (self, position, color, offset_y=10, width=10, height=30):
        super(FlickerLightItem, self).__init__()
        self.position = position
        self.boundingRectF = QtCore.QRectF(0,0,width,height)

        self.rectF = QtCore.QRectF(0,0,width,height)
        self.color = color
        self.setPos(self.position, offset_y)

    def boundingRect (self):
        return self.boundingRectF

    def paint (self, painter=None, style=None, widget=None):
        outlinePen = QtGui.QPen(QtGui.QColor(0,0,0,125))
        outlinePen.setWidth(2)
        painter.setPen(outlinePen)
        painter.drawRect(self.boundingRectF)
        brush = QtGui.QBrush(self.color, QtCore.Qt.SolidPattern);
        painter.fillRect(self.rectF, brush)

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
    def __init__(self, tickDistance=10, numTicksPerMajorTick=10):
        QtWidgets.QGraphicsScene.__init__(self)
        self.tickPainter = TickPainter(tickDistance, numTicksPerMajorTick)
        self.currentColor = QtGui.QColor(0,0,0,255)
        self.shortcut_colors = [self.currentColor for i in range(10)]
        self.shortcut_keys = [
            QtCore.Qt.Key_1,
            QtCore.Qt.Key_2,
            QtCore.Qt.Key_3,
            QtCore.Qt.Key_4,
            QtCore.Qt.Key_5,
            QtCore.Qt.Key_6,
            QtCore.Qt.Key_7,
            QtCore.Qt.Key_8,
            QtCore.Qt.Key_9,
            QtCore.Qt.Key_0]

    def drawBackground(self, painter, rect):
        QtWidgets.QGraphicsScene.drawBackground(self, painter, rect)
        self.tickPainter.draw(painter, rect)

    def event(self, event):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Tab:
            color = QtWidgets.QColorDialog.getColor()
            self.currentColor = color
            return False
        if event.type() == QtCore.QEvent.KeyPress and event.key() in self.shortcut_keys:
            shortcut_idx = self.shortcut_keys.index(event.key())
            if modifiers == QtCore.Qt.ControlModifier:
                self.shortcut_colors[shortcut_idx] = self.currentColor
            else:
                self.currentColor = self.shortcut_colors[shortcut_idx]
            return False

        return QtWidgets.QGraphicsScene.event(self, event)

    def mousePressEvent(self, event):
        super(MyGraphicsScene, self).mousePressEvent(event)
        position = QtCore.QPointF(event.scenePos())
        tick_position = self.tickPainter.getPosition(position)
        item = FlickerLightItem(tick_position, self.currentColor)
        collidingItems = self.collidingItems(item, QtCore.Qt.IntersectsItemShape)
        if not collidingItems:
            self.addItem(item)
        else:
            for collidingItem in collidingItems:
                self.removeItem(collidingItem)

class LightshowProgram(Ui_MainWindow):
    def setupGraphicsScene(self):
            self.sceneLength = self.tickDistance * (self.songLength/self.timePerTick)
            self.scene = MyGraphicsScene(self.tickDistance, 1/self.timePerTick)
            self.testCanvas.setScene(self.scene)
            self.testCanvas.setSceneRect(0,0,self.sceneLength,50)

    def __init__(self, window):
        Ui_MainWindow.__init__(self)
        self.setupUi(window)
        self.songLength = 60*1
        self.timePerTick = .25
        self.tickDistance = 10

        self.setupGraphicsScene()

        self.playButton.clicked.connect(self.save_show_yaml)
        self.playButton.setText("Save SHOW File")
        self.pauseButton.clicked.connect(self.load_show_yaml)
        self.pauseButton.setText("Load SHOW File")

    def load_show_yaml(self):
        file_dialog = QtWidgets.QFileDialog.getOpenFileName()
        if file_dialog[0]:
            show_config = {}
            with open(file_dialog[0],'r') as yaml_file:
                show_config = yaml.load(yaml_file)

            # Clear current canvas
            items = sorted(self.scene.items(), key = lambda item: item.position)
            for item in items:
                self.scene.removeItem(item)

            for show_time_item in show_config['show']:
                position = show_time_item['time']*self.tickDistance / self.timePerTick
                color = show_time_item['commands'][0]['color']
                item = FlickerLightItem(position, QtGui.QColor((color&0xFF0000)>>16, (color & 0x00FF00)>>8, color & 0x0000FF))
                self.scene.addItem(item)
    def save_show_yaml(self):
        file_dialog = QtWidgets.QFileDialog.getSaveFileName()
        if file_dialog[0]:
            items = sorted(self.scene.items(), key = lambda item: item.position)
            show = []

            for item in items:
                show_command = {
                    'time': self.timePerTick*(item.position/self.tickDistance),
                    'commands': [{
                        'group': 0,
                        'type': 'set',
                        'color': int(item.color.name().replace("#", ""),16)}]}
                show.append(show_command)
            metadata = {
                "title": "Yellow Flicker Beat",
                "artist": "Lorde",
                "location": "assets/song.wav",
                "date": "2016-09-10",
                "start_time": 0,
                "speed": 1,
                "volume": 1,
                "show":show
            }

            yaml_str = yaml.dump(metadata, default_flow_style=False)
            yaml_file = open(file_dialog[0],'w')
            yaml_file.write(yaml_str)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    prog = LightshowProgram(window)

    window.show()

    sys.exit(app.exec_())
