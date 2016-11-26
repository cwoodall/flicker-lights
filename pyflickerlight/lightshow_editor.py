import sys
import yaml
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import matplotlib
import wave
import numpy as np
from tinytag import TinyTag
matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

import math
import random

import threading

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
        self.tickDistance = tickDistance
        self.numTicksPerMajorTick = numTicksPerMajorTick
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
        item = FlickerLightItem(tick_position, self.currentColor, width=self.tickDistance)
        collidingItems = self.collidingItems(item, QtCore.Qt.IntersectsItemShape)
        if not collidingItems:
            self.addItem(item)
        else:
            for collidingItem in collidingItems:
                self.removeItem(collidingItem)

class LightshowProgram(QtWidgets.QMainWindow):
    def setupGraphicsScene(self):
        self.sceneLength = self.tickDistance * (self.songLength/self.timePerTick)
        self.scene = MyGraphicsScene(self.tickDistance, 1/self.timePerTick)
        self.testCanvas.setScene(self.scene)
        self.testCanvas.setSceneRect(0,0,self.sceneLength,50)

    def setupPlot(self):
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        self.plottingLayout.addWidget(self.canvas)

    def plot(self, event=None):
        ''' plot some random stuff '''
        N = 516

        if self.currentSong:
            if self.loadedSong != self.currentSong:
                spf = wave.open(self.currentSong,'r')
                self.fs = spf.getframerate()
                self.signal = spf.readframes(-1)
                self.signal = np.fromstring(self.signal, 'Int16')
                self.loadedSong = self.currentSong
                self.signa_compressed = self.signal[0:-1:2] # make Mono
                self.signa_compressed = self.signa_compressed[0:-1:N] # Resample

            orig_len = len(self.signal)

            #/2 to account for the stero to mono conversion
            Time=np.linspace(0,orig_len/float(self.fs)/2, num=len(self.signa_compressed))

            # create an axis
            ax = self.figure.add_subplot(111)
            # discards the old graph
            ax.hold(False)

            scene_rect = self.testCanvas.mapToScene(self.testCanvas.viewport().rect()).boundingRect()

            point_to_time = lambda x, w, dt: dt*x/w
            time_start = point_to_time(scene_rect.left(), self.tickDistance, self.timePerTick)
            num_secs = point_to_time(scene_rect.width(), self.tickDistance, self.timePerTick)

            dt = Time[1] - Time[0]
            num = int(num_secs / dt)
            point_start = int(time_start / dt)
            # plot data
            ax.plot(Time[point_start:point_start+num], self.signa_compressed[point_start:point_start+num])

            ax.set_xlabel("Time (s)")
            ax.get_yaxis().set_visible(False)
            self.figure.tight_layout()
            self.figure.subplots_adjust(left=0, right=1, top=1, bottom=0.2)
            ax.relim()
            ax.autoscale_view(True,True,True)
            # refresh canvas
            self.canvas.draw()

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi('lightshow_editor.ui', self)
        # self.setupUi(window)
        self.songLength = 0
        self.timePerTick = .1
        self.tickDistance = 5
        self.currentSong = None
        self.loadedSong = None

        self.setupGraphicsScene()

        self.playButton.clicked.connect(self.save_show_yaml)
        self.playButton.setText("Save SHOW File")
        self.pauseButton.clicked.connect(self.load_show_yaml)
        self.pauseButton.setText("Load SHOW File")
        self.loadSongButton.clicked.connect(self.loadNewSong)
        self.setupPlot()
        self.testCanvas.horizontalScrollBar().valueChanged.connect(self.plot)
        self.resizeEvent = lambda event: self.plot()

    def updateSongInfo(self, title, artist, duration):
        self.titleLabel.setText(title)
        self.artistLabel.setText(artist)
        self.songLength = duration
        self.durationLabel.setText("{:.2f} seconds".format(duration))

    def updateSong(self, file_name):
        self.filenameLabel.setText(file_name)
        self.currentSong = file_name
        tag = TinyTag.get(file_name)
        self.updateSongInfo(tag.title, tag.artist, tag.duration)
        self.setupGraphicsScene()
        self.plot()

    def loadNewSong(self):
        file_dialog = QtWidgets.QFileDialog.getOpenFileName()
        if file_dialog[0]:
            self.updateSong(file_dialog[0])

    def load_show_yaml(self):
        file_dialog = QtWidgets.QFileDialog.getOpenFileName()
        if file_dialog[0]:
            show_config = {}
            with open(file_dialog[0],'r') as yaml_file:
                show_config = yaml.load(yaml_file)

            self.updateSong(show_config["location"])

            self.updateSongInfo(show_config["title"], show_config["artist"], self.songLength)

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
                "title": self.titleLabel.text(),
                "artist": self.artistLabel.text(),
                "location": self.currentSong,
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
    # window = QtWidgets.QMainWindow()

    prog = LightshowProgram()

    prog.show()

    sys.exit(app.exec_())
