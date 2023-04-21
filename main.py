import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QFormLayout, QWidget, QCheckBox, QPushButton, QSlider, QLabel, QMainWindow, QMenuBar, QStatusBar
from PyQt6.QtCore import Qt, QTimer, QRect, QCoreApplication, QMetaObject
from PyQt6.QtGui import QBrush, QColor, QPixmap

import random

from PyQt6 import QtGui


class Game(object):
    def __init__(self, hight: int, width: int):
        self.player = Player(25, 25, 1)
        self.currentApple = []
        self.x = hight
        self.y = width

        self.border = True
        self.speedUp = True
        self.getFaster = False

        self.apple = [0, 0]
        self.spawnApple()

    def spawnApple(self):
        self.apple[0] = random.randint(1, self.x - 2)
        self.apple[1] = random.randint(1, self.y - 2)

        if self.apple in self.player.tail or self.apple == self.player.head:
            self.spawnApple()

        if self.speedUp:
            self.player.speed = self.player.speed + 10
            self.getFaster = True

    def collectApple(self):
        apple = [self.player.head[0], self.player.head[1]]
        self.player.tail.append(apple)
        self.spawnApple()

    def checkCollision(self):
        temp = self.player.head.copy()
        if self.player.head[0] <= 0 or self.player.head[0] >= self.x - 1 or self.player.head[1] <= 0 or \
                self.player.head[1] >= self.y - 1:
            if self.border:
                self.player.curDirection = "None"
                self.player.alive = False
            else:
                if self.player.head[0] <= 0:
                    self.player.head[0] = self.y - 1
                elif self.player.head[0] >= self.x - 1:
                    self.player.head[0] = 0
                elif self.player.head[1] <= 1:
                    self.player.head[1] = self.x - 1
                elif self.player.head[1] >= self.y - 1:
                    self.player.head[1] = 0
        elif self.player.head[0] == self.apple[0] and self.player.head[1] == self.apple[1]:
            self.collectApple()
        elif temp in self.player.tail:
            self.player.curDirection = "None"
            self.player.alive = False



class Player(object):
    def __init__(self, x: int, y: int, speed: int):
        self.head = [x, y]
        self.tail = []
        self.speed = speed
        self.curDirection = "None"
        self.alive = True

    def move(self, direction):
        if direction == "UP" and self.curDirection != "DOWN":
            self.curDirection = "UP"
        elif direction == "DOWN" and self.curDirection != "UP":
            self.curDirection = "DOWN"
        elif direction == "LEFT" and self.curDirection != "RIGHT":
            self.curDirection = "LEFT"
        elif direction == "RIGHT" and self.curDirection != "LEFT":
            self.curDirection = "RIGHT"

    def moveTail(self):
        for i in range(0, len(self.tail)):
            temp = self.tail.copy()
            if i == len(self.tail)-1:
                self.tail[i] = [self.head[0], self.head[1]]
            else:
                self.tail[i] = temp[i+1]

    def autoMove(self):
        if self.curDirection != "None":
            self.moveTail()
            if self.curDirection == "UP":
                self.head[1] = self.head[1] - 1
            elif self.curDirection == "DOWN":
                self.head[1] = self.head[1] + 1
            elif self.curDirection == "LEFT":
                self.head[0] = self.head[0] - 1
            elif self.curDirection == "RIGHT":
                self.head[0] = self.head[0] + 1


class Window(QWidget, object):
    def __init__(self, game: Game):
        super().__init__()
        self.timer = QTimer()
        self.game = game
        self.player = game.player
        self.initMe()

    def onRepeat(self):
        # erstellen des Speilfeldes
        width, hight = self.game.x * 10, self.game.y * 10

        board = QtGui.QPixmap(self.game.x, self.game.y)
        board.fill(QColor(100, 100, 255))

        img = board.toImage()

        # border

        if self.game.border:
            for i in range(0, self.game.x):
                img.setPixelColor(i, 0, QColor(255, 0, 0))
                img.setPixelColor(i, self.game.y - 1, QColor(255, 0, 0))

            for i in range(0, self.game.y):
                img.setPixelColor(self.game.x - 1, i, QColor(255, 0, 0))
                img.setPixelColor(0, i, QColor(255, 0, 0))
        else:
            for i in range(0, self.game.x):
                img.setPixelColor(i, 0, QColor(255, 255, 255))
                img.setPixelColor(i, self.game.y - 1, QColor(255, 255, 255))

            for i in range(0, self.game.y):
                img.setPixelColor(self.game.x - 1, i, QColor(255, 255, 255))
                img.setPixelColor(0, i, QColor(255, 255, 255))

        # Set player head
        self.game.checkCollision()
        self.player.autoMove()
        img.setPixelColor(self.player.head[0], self.player.head[1], QColor(100, 155, 0))

        # Apple stuff
        img.setPixelColor(self.game.apple[0], self.game.apple[1], QColor(255, 0, 0))

        # Tail stuff
        for i in self.player.tail:
            img.setPixelColor(i[0], i[1], QColor(0, 255, 0))

        scaledBoardImg = img.scaled(width, hight, Qt.AspectRatioMode.KeepAspectRatio)

        self.display.setPixmap(QPixmap.fromImage(scaledBoardImg))

        if self.game.getFaster:
            self.game.getFaster = False
            self.checkSettings()

    def checkSettings(self):
        # timer
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.setInterval(150 - self.game.player.speed)  # in milliseconds, so 5000 = 5 seconds
        self.timer.timeout.connect(self.onRepeat)
        self.timer.start()


    def initMe(self):
        self.setGeometry(10, 30, 100, 100)  # Position: (10,30) auf dem Bildschirm Größe:  (300,200)
        self.setWindowTitle("Snake")  # Titel setzen

        # in QLabel wird das Bild angezeigt
        self.display = QLabel()
        form = QFormLayout()

        # erstellen des Speilfeldes
        width, hight = 500, 500

        board = QtGui.QPixmap(50, 50)
        board.fill(QColor(100, 100, 255))

        img = board.toImage()

        # Widget und Layout hinzufügen
        form.addWidget(self.display)
        self.setLayout(form)
        self.show()

        # timer
        self.checkSettings()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key.Key_Up:
            self.player.move("UP")
        elif QKeyEvent.key() == Qt.Key.Key_Down:
            self.player.move("DOWN")
        elif QKeyEvent.key() == Qt.Key.Key_Left:
            self.player.move("LEFT")
        elif QKeyEvent.key() == Qt.Key.Key_Right:
            self.player.move("RIGHT")


class Ui_MainWindow(object):
    def __init__(self, win: Window):
        super().__init__()
        self.timer = QTimer()
        self.game = win

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(343, 321)
        self.centralwidget = QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.checkBoxBorder = QCheckBox(parent=self.centralwidget)
        self.checkBoxBorder.setGeometry(QRect(30, 10, 86, 20))
        self.checkBoxBorder.setObjectName("checkBoxBorder")

        #button
        self.submitSettings = QPushButton(parent=self.centralwidget, clicked= self.submit) #Button submit settings
        self.submitSettings.setGeometry(QRect(20, 130, 113, 32))
        self.submitSettings.setObjectName("submitSettings")

        #Slider
        self.SlideSpeed = QSlider(parent=self.centralwidget)
        self.SlideSpeed.setGeometry(QRect(90, 40, 160, 22))
        self.SlideSpeed.setOrientation(Qt.Orientation.Horizontal)
        self.SlideSpeed.setObjectName("SlideSpeed")
        self.SlideSpeed.valueChanged.connect(self.speedSlider)

        self.label = QLabel(parent=self.centralwidget)
        self.label.setGeometry(QRect(30, 40, 60, 16))
        self.label.setObjectName("label")
        self.checkBoxFaster = QCheckBox(parent=self.centralwidget)
        self.checkBoxFaster.setGeometry(QRect(30, 70, 161, 20))
        self.checkBoxFaster.setObjectName("checkBoxFaster")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 343, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        #default val
        if self.game.game.border:
            self.checkBoxBorder.setChecked(True)
        if self.game.game.speedUp:
            self.checkBoxFaster.setChecked(True)


        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def speedSlider(self, value):
        self.game.game.player.speed = value

    def submit(self):
        if self.checkBoxBorder.isChecked():
            self.game.game.border = True
        else:
            self.game.game.border = False

        if self.checkBoxFaster.isChecked():
            self.game.game.speedUp = True
        else:
            self.game.game.speedUp = False

        self.game.checkSettings()

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.checkBoxBorder.setText(_translate("MainWindow", "Border"))
        self.submitSettings.setText(_translate("MainWindow", "Submit"))
        self.label.setText(_translate("MainWindow", "Speed"))
        self.checkBoxFaster.setText(_translate("MainWindow", "becoming faster"))



app = QApplication(sys.argv)

#game
win = Window(Game(60, 60))

#settings
MainWindow = QMainWindow()
ui = Ui_MainWindow(win)
ui.setupUi(MainWindow)
MainWindow.show()

app.exec()
