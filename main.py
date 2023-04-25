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
        self.setGeometry(100, 100, 300, 150)

        # Border CheckBox
        borderCB = qw.QCheckBox()
        borderCB.setChecked(False)
        borderCB.setToolTip("Checked: Die when hitting the border")

        # Speed Slider
        speedSL = qw.QSlider(qc.Qt.Horizontal)
        speedSL.setMinimum(1)
        speedSL.setMaximum(10)
        speedSL.setValue(5)
        speedSL.setToolTip("Decide how fast the game is")

        # Fruits Slider
        fruitsSL = qw.QSlider(qc.Qt.Horizontal)
        fruitsSL.setMinimum(1)
        fruitsSL.setMaximum(10)
        fruitsSL.setValue(5)
        fruitsSL.setToolTip("Decide how often fruits spawn")

        startBU = qw.QPushButton("Start")
        startBU.setToolTip("Start the game with your settings")

        # Layout of Main Menu
        layout = qw.QFormLayout()
        layout.addRow(qw.QLabel("border:"), borderCB)
        layout.addRow(qw.QLabel("speed: "), speedSL)
        layout.addRow(qw.QLabel("fruits: "), fruitsSL)
        layout.addRow(startBU)
        self.setLayout(layout)

class Snake(qw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snake")
        self.setGeometry(100,100,500,500)

        self.moving = False
        self.lastDir = None

        self.borders = False

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
        rndNum = random.randint(0,11)
        if rndNum == 0:
            rndX = random.randint(0,32)
            rndY = random.randint(0,32)
            while ((rndX,rndY) in self.snakeLoc or (rndX,rndY) in self.fruits):
                rndX = random.randint(0, 32)
                rndY = random.randint(0, 32)

            self.fruits.append((rndX,rndY))

if __name__=="__main__":
    app = qw.QApplication(sys.argv)
    win = MainWindow()
    #win = Snake()
    win.show()
    sys.exit(app.exec_())


# Bugs die noch gefixt werden müssen:
# 1. Rückwärts laufen beim schnellen Richtungswechsel

# To do:
# Main Menü ans Spiel anknüpfen (Beim klick auf "Start" öffnet sich das Spiel)
# Fruit Spawn Rait
# Speed
# Border (Funktionalität schon umgesetzt
# Tooltips
# Menüleiste (Pausieren, beenden, Punkte)
# defead Funktion (Endpunktestart restart?)
# Highscore der vergangenen Spiele