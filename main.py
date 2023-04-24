import random
import sys
import numpy
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc

class MainWindow(qw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")

        cb = qw.QCheckBox()
        cb.setChecked(False)

        layout = qw.QFormLayout()
        layout.addRow(qw.QLabel("name:"), qw.QTextEdit("User"))
        layout.addRow(qw.QLabel("speed:"), qw.QTextEdit("5"))
        layout.addRow(qw.QLabel("border:"), cb)
        layout.addRow(qw.QPushButton("Start"))
        self.setLayout(layout)

class Snake(qw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snake")
        self.setGeometry(100,100,500,500)

        self.moving = False
        self.lastDir = None

        #Bild von Spiel
        game = qw.QLabel(self)
        self.pic = qg.QImage(32,32, qg.QImage.Format_RGBA8888)
        self.pic.fill(qc.Qt.gray)
        # pic.setPixel(10,10, 0x00ff00ff) so färbt man Pixel




        self.headX = 10
        self.headY = 10

        self.pic.setPixelColor(self.headX,self.headY, qc.Qt.darkGreen)

        # Timer
        self.timer = qc.QTimer()
        self.timer.setInterval(1000)  # Timer-Reset alle 300ms
        self.timer.timeout.connect(self.timerFunction)
        self.timer.start(300)

        scaledPic = self.pic.scaled(500, 500)
        game.setPixmap(qg.QPixmap.fromImage(scaledPic))
    def keyPressEvent(self, e):
        if self.moving == False: self.moving = True
        if e.key() == qc.Qt.Key.Key_Up:
            if self.lastDir != "Down":
                self.lastDir = "Up"
        if e.key() == qc.Qt.Key.Key_Down:
            if self.lastDir != "Up":
                self.lastDir = "Down"
        if e.key() == qc.Qt.Key.Key_Left:
            if self.lastDir != "Right":
                self.lastDir = "Left"
        if e.key() == qc.Qt.Key.Key_Right:
            if self.lastDir != "Left":
                self.lastDir = "Right"

    def timerFunction(self):
        if self.moving == True:
            self.pic.setPixelColor(self.headX, self.headY, qc.Qt.gray)
            if self.lastDir == "Up":
                self.headY -=1
            if self.lastDir == "Down":
                self.headY +=1
            if self.lastDir == "Left":
                self.headX -=1
            if self.lastDir == "Right":
                self.headX +=1
            self.pic.setPixelColor(self.headX, self.headY, qc.Qt.darkGreen)
            scaledPic = self.pic.scaled(500, 500)
            game = self.findChild(qw.QLabel)
            game.setPixmap(qg.QPixmap.fromImage(scaledPic))









if __name__=="__main__":
    app = qw.QApplication(sys.argv)
    # win = MainWindow()
    win = Snake()
    win.show()
    sys.exit(app.exec_())


# Bugs die noch gefixt werden müssen:
# 1. Rückwärts laufen beim schnellen Richtungswechsel