import random
import sys

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QTimer, QRect, QCoreApplication, QMetaObject
from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtWidgets import QApplication, QFormLayout, QWidget, QCheckBox, QPushButton, QSlider, QLabel, QMainWindow, \
    QMenuBar, QStatusBar, QMenu, QMessageBox


class Game(object):
    def __init__(self, hight: int, width: int):

        # Create Player, add apple and define size of board
        self.player = Player(round(width / 2), round(hight / 2), 1)
        self.currentApple = []
        self.x = hight
        self.y = width

        self.border = True  # Setting: Boarder kills player or not (Default True)
        self.speedUp = True  # Setting: Player gets faster after eating apple (Default _True)

        self.getFaster = False  # Did the player just ate an apple?

        # Spawn start apple
        self.apple = [0, 0]
        self.spawnApple()

    # Spawns an apple
    def spawnApple(self):
        self.apple[0] = random.randint(1, self.x - 2)
        self.apple[1] = random.randint(1, self.y - 2)

        # Take care that the field is not in use
        if self.apple in self.player.tail or self.apple == self.player.head:
            self.spawnApple()

        # if the player uses Setting speed up tell the gui to refresh faster by setting getFaster on True
        if self.speedUp:
            if self.player.speed <= 110:
                self.player.speed = self.player.speed + 5
                self.getFaster = True

    # Player collects apple
    def collectApple(self):
        apple = [self.player.head[0], self.player.head[1]]  # location of the apple
        self.player.tail.append(apple)  # add one element to the tail
        self.player.score = self.player.score + 5  # increase score
        self.spawnApple()  # spawn a new apple

    # Did the Player hit anything?
    def checkCollision(self):
        temp = self.player.head.copy()  # copy current pos
        if self.player.head[0] <= 0 or self.player.head[0] >= self.x - 1 or self.player.head[1] <= 0 or \
                self.player.head[1] >= self.y - 1:  # did he hit the border?
            if self.border:  # if border rule on -> Dead
                self.player.curDirection = "None"
                self.player.alive = False
            else:  # if border rule off -> show up on the other side
                if self.player.head[0] <= 0:
                    self.player.head[0] = self.y - 2
                elif self.player.head[0] >= self.x - 1:
                    self.player.head[0] = 1
                elif self.player.head[1] <= 0:
                    self.player.head[1] = self.x - 2
                elif self.player.head[1] >= self.y - 1:
                    self.player.head[1] = 1
        elif self.player.head[0] == self.apple[0] and self.player.head[1] == self.apple[1]:  # did he hit the apple?
            self.collectApple()
        elif temp in self.player.tail:  # did he hit the tail?
            self.player.curDirection = "None"
            self.player.alive = False


class Player(object):
    def __init__(self, x: int, y: int, speed: int):
        # setup player
        self.head = [x, y]
        self.tail = []
        self.speed = speed
        self.curDirection = "None"
        self.alive = True
        self.score = 0
        self.initSpeed = 0

    def move(self, direction):  # someone hit a key
        if direction == "UP" and self.curDirection != "DOWN":
            self.curDirection = "UP"
        elif direction == "DOWN" and self.curDirection != "UP":
            self.curDirection = "DOWN"
        elif direction == "LEFT" and self.curDirection != "RIGHT":
            self.curDirection = "LEFT"
        elif direction == "RIGHT" and self.curDirection != "LEFT":
            self.curDirection = "RIGHT"

    def moveTail(self):  # tail is moving
        for i in range(0, len(self.tail)):
            temp = self.tail.copy()
            if i == len(self.tail) - 1:
                self.tail[i] = [self.head[0], self.head[1]]
            else:
                self.tail[i] = temp[i + 1]

    def autoMove(self):  # also moving if nobody hit a key
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


class Window(QWidget, object):  # game-Window
    def __init__(self, game: Game):
        super().__init__()

        # timer for repeat
        self.timer = QTimer()

        # Game-Info
        self.game = game
        self.player = game.player
        self.highscore = [0, 0, 0]

        # Outer win settings
        self.setGeometry(10, 30, 100, 100)
        self.setWindowTitle("Snake")

        self.form = QFormLayout()  # Layout

        # creat board

        board = QtGui.QPixmap(50, 50)
        board.fill(QColor(100, 100, 255))

        # Screen
        self.display = QLabel()

        # Statusbar
        self.statusbar = QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.displayScore = QLabel("Score: 0")
        self.statusbar.addWidget(self.displayScore)

        # Menubar
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName("menubar")
        self.menu = QMenu("Pause")
        self.menubar.addMenu(self.menu)
        self.menu.addAction("Pause", self.pauseGame)
        self.menubar.move(0, 0)

        # Highscore
        self.displayHighScore = QLabel("Highscore: 0 / 0 / 0")

        # Widget und Layout hinzufügen
        self.form.addWidget(self.display)
        self.form.addWidget(self.statusbar)
        self.form.addWidget(self.menubar)
        self.form.addWidget(self.displayHighScore)

        self.setLayout(self.form)

        # timer
        self.checkSettings()

    # pause game
    def pauseGame(self):
        self.player.curDirection = "None"

    # call in loop
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
        if (0 < self.player.head[0] < self.game.x -1) and (0 < self.player.head[1] < self.game.y -1):
            img.setPixelColor(self.player.head[0], self.player.head[1], QColor(100, 155, 0))

        # Apple stuff
        img.setPixelColor(self.game.apple[0], self.game.apple[1], QColor(255, 0, 0))

        # Tail stuff
        for i in self.player.tail:
            img.setPixelColor(i[0], i[1], QColor(0, 255, 0))

        scaledBoardImg = img.scaled(width, hight, Qt.AspectRatioMode.KeepAspectRatio)

        # show map and score
        self.display.setPixmap(QPixmap.fromImage(scaledBoardImg))
        self.displayScore.setText("Score: " + str(self.player.score))

        # check if the time has to be updated
        if self.game.getFaster:
            self.game.getFaster = False
            self.checkSettings()

        # check if the game ist over
        self.checkGameEnd()

    # Check function
    def checkGameEnd(self):
        if not self.player.alive:
            # msg box
            msg = QMessageBox()
            msg.setWindowTitle("GAME OVER")
            msg.setText("Score: " + str(self.player.score))

            self.timer.stop()

            msg.exec()

            # safe highscore
            self.highscore.append(self.player.score)
            self.highscore.sort(reverse=True)
            self.highscore.pop()

            # start new game
            # keep Settings
            temp_boarder = self.game.border
            temp_speedUp = self.game.speedUp
            temp_speed = self.game.player.initSpeed

            self.game = Game(self.game.x, self.game.y)
            self.game.speedUp = temp_speedUp
            self.game.border = temp_boarder
            self.player = self.game.player
            self.player.speed = temp_speed
            self.player.initSpeed = temp_speed
            self.timer.start()
            #

            # update highscore
            self.displayHighScore.setText(
                "Highscore: " + str(self.highscore[0]) + " / " + str(self.highscore[1]) + " / " + str(
                    self.highscore[2]))

    def checkSettings(self):
        # timer
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.setInterval(150 - self.game.player.speed)                # in milliseconds and controls the speed
        self.timer.timeout.connect(self.onRepeat)
        self.timer.start()

    # this function is called when a key is pressed
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key.Key_Up:
            self.player.move("UP")
        elif QKeyEvent.key() == Qt.Key.Key_Down:
            self.player.move("DOWN")
        elif QKeyEvent.key() == Qt.Key.Key_Left:
            self.player.move("LEFT")
        elif QKeyEvent.key() == Qt.Key.Key_Right:
            self.player.move("RIGHT")


# Settings
class Ui_MainWindow(object):
    def __init__(self, winIn: Window):
        super().__init__()
        self.timer = QTimer()
        self.game = winIn

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(343, 321)
        self.centralwidget = QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.checkBoxBorder = QCheckBox(parent=self.centralwidget)
        self.checkBoxBorder.setGeometry(QRect(30, 10, 86, 20))
        self.checkBoxBorder.setObjectName("checkBoxBorder")
        self.checkBoxBorder.setToolTip("Border hit = game over")

        # button
        self.submitSettings = QPushButton(parent=self.centralwidget, clicked=self.submit)  # Button submit settings
        self.submitSettings.setGeometry(QRect(20, 130, 113, 32))
        self.submitSettings.setObjectName("submitSettings")
        self.submitSettings.setToolTip("Press this Button to Submit your Settings and start the game")

        # Slider
        self.SlideSpeed = QSlider(parent=self.centralwidget)
        self.SlideSpeed.setGeometry(QRect(90, 40, 160, 22))
        self.SlideSpeed.setOrientation(Qt.Orientation.Horizontal)
        self.SlideSpeed.setObjectName("SlideSpeed")
        self.SlideSpeed.valueChanged.connect(self.speedSlider)
        self.SlideSpeed.setToolTip("You can chose the speed of your character")

        self.label = QLabel(parent=self.centralwidget)
        self.label.setGeometry(QRect(30, 40, 60, 16))
        self.label.setObjectName("label")

        self.checkBoxFaster = QCheckBox(parent=self.centralwidget)
        self.checkBoxFaster.setGeometry(QRect(30, 70, 161, 20))
        self.checkBoxFaster.setObjectName("checkBoxFaster")
        self.checkBoxFaster.setToolTip("every Apple makes you faster")

        MainWindow.setCentralWidget(self.centralwidget)

        # default val
        if self.game.game.border:
            self.checkBoxBorder.setChecked(True)
        if self.game.game.speedUp:
            self.checkBoxFaster.setChecked(True)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def speedSlider(self, value):
        self.game.game.player.speed = value
        self.game.game.player.initSpeed = value

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
        self.game.show()
        MainWindow.close()

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.checkBoxBorder.setText(_translate("MainWindow", "Border"))
        self.submitSettings.setText(_translate("MainWindow", "Submit"))
        self.label.setText(_translate("MainWindow", "Speed"))
        self.checkBoxFaster.setText(_translate("MainWindow", "becoming faster"))


app = QApplication(sys.argv)

# game
win = Window(Game(60, 60))

# settings
MainWindow = QMainWindow()
ui = Ui_MainWindow(win)
ui.setupUi(MainWindow)
MainWindow.show()

app.exec()
