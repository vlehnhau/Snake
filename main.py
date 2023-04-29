import random
import sys
import numpy
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc


class Snake(qw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snake")
        self.setGeometry(100,100,500,500)

        self.moving = False
        self.lastDir = None

        self.borders = False
        self.speed = 100

        self.fruitsSR = 10  # fruits Spawn-Rate
        self.fruits = []

        #Bild von Spiel
        game = qw.QLabel(self)
        self.pic = qg.QImage(32,32, qg.QImage.Format_RGBA8888)
        self.pic.fill(qc.Qt.gray)



        self.headX = 10
        self.headY = 10
        self.snakeLen = 1
        self.snakeLoc = [(self.headX, self.headY)]

        self.pic.setPixelColor(self.headX,self.headY, qc.Qt.green)

        # Timer
        self.timer = qc.QTimer()
        self.timer.timeout.connect(self.timerFunction)


        scaledPic = self.pic.scaled(500, 500)
        game.setPixmap(qg.QPixmap.fromImage(scaledPic))
    def keyPressEvent(self, e):
        if self.moving == False:
            self.moving = True
            self.timer.setInterval(self.speed)
            self.timer.start()
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
            self.spawnFruit()
            if self.lastDir == "Up":
                self.headY -=1
            if self.lastDir == "Down":
                self.headY +=1
            if self.lastDir == "Left":
                self.headX -=1
            if self.lastDir == "Right":
                self.headX +=1

            if self.borders:
                if self.headX < 0 or self.headX > 31 or self.headY < 0 or self.headY > 31:
                    self.timer.stop()
                    # add Function for ending Game
            else:
                if self.headX < 0:
                    self.headX = 31
                if self.headX > 31:
                    self.headX = 0
                if self.headY < 0:
                    self.headY = 31
                if self.headY > 31:
                    self.headY = 0


            if ((self.headX, self.headY) in self.snakeLoc):
                self.timer.stop()
                # add Function for ending Game

            self.snakeLoc.insert(0, (self.headX, self.headY))

            if self.snakeLoc[0] in self.fruits:
                self.snakeLen += 1
                self.fruits.remove(self.snakeLoc[0])

            if len(self.snakeLoc) > self.snakeLen:
                self.snakeLoc.pop()

            self.pic.fill(qc.Qt.gray)

            for loc in self.snakeLoc:
                self.pic.setPixelColor(loc[0], loc[1], qc.Qt.darkGreen)
            self.pic.setPixelColor(self.headX, self.headY, qc.Qt.green)


            for fruit in self.fruits:
                self.pic.setPixelColor(fruit[0], fruit[1], qc.Qt.red)

            scaledPic = self.pic.scaled(500, 500)
            game = self.findChild(qw.QLabel)
            game.setPixmap(qg.QPixmap.fromImage(scaledPic))

    def spawnFruit(self):
        rndNum = random.randint(0,self.fruitsSR)
        if rndNum == 0:
            rndX = random.randint(0,32)
            rndY = random.randint(0,32)
            while ((rndX,rndY) in self.snakeLoc or (rndX,rndY) in self.fruits):
                rndX = random.randint(0, 32)
                rndY = random.randint(0, 32)

            self.fruits.append((rndX, rndY))

class MainWindow(qw.QWidget):

    def __init__(self, winIn: Snake):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 100, 300, 150)
        self.game = winIn
        self.snake_game = Snake()


        # Border CheckBox
        self.borderCB = qw.QCheckBox()
        self.borderCB.setChecked(False)
        self.borderCB.setToolTip("Check: Die when hitting the border")

        def borderCBTooltip(state):
            if state == qc.Qt.Checked:
                self.borderCB.setToolTip("Uncheck: Allows the snake to continue on the opposite side of the playing field when hitting the border.")
            else:
                self.borderCB.setToolTip("Check: Lose when hitting the border")
        self.borderCB.stateChanged.connect(borderCBTooltip)

        # Speed Slider
        self.speedSL = qw.QSlider(qc.Qt.Horizontal)
        self.speedSL.setMinimum(1)
        self.speedSL.setMaximum(10)
        self.speedSL.setValue(5)
        self.speedSL.setToolTip("Decide how fast the game is")

        # Fruits Slider
        self.fruitsSL = qw.QSlider(qc.Qt.Horizontal)
        self.fruitsSL.setMinimum(1)
        self.fruitsSL.setMaximum(10)
        self.fruitsSL.setValue(5)
        self.fruitsSL.setToolTip("Decide how often fruits spawn")

        # Button
        startBU = qw.QPushButton("Start", self)
        startBU.setToolTip("Start the game with your settings")
        startBU.clicked.connect(self.startSnake)

        # Layout of Main Menu
        layout = qw.QFormLayout()
        layout.addRow(qw.QLabel("border:"), self.borderCB)
        layout.addRow(qw.QLabel("speed: "), self.speedSL)
        layout.addRow(qw.QLabel("fruits: "), self.fruitsSL)
        layout.addRow(startBU)
        self.setLayout(layout)

        # self.game.borders = True

    def startSnake(self):
        self.snakeGame = Snake()
        self.snakeGame.borders = self.borderCB.isChecked()
        self.snakeGame.speed = 125 - (10 * self.speedSL.value())
        self.snakeGame.fruitsSR = 16 - self.fruitsSL.value()
        self.snakeGame.show()
        self.close()



if __name__=="__main__":
    app = qw.QApplication(sys.argv)
    game = Snake()
    win = MainWindow(game)
    win.show()
    sys.exit(app.exec_())


# To do:
# Menüleiste (Pausieren, beenden, Punkte)
# defead Funktion (Endpunktestart restart?)
# Highscore der vergangenen Spiele
# Qt Creator