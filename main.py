import sys
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
        self.timer.setInterval(300)  # Timer-Reset alle 300ms

        scaledPic = self.pic.scaled(500, 500)
        game.setPixmap(qg.QPixmap.fromImage(scaledPic))
    def keyPressEvent(self, e):
        if self.moving == False: self.moving = True
        if e.key() == qc.Qt.Key.Key_Up:
            self.move("Up")
        if e.key() == qc.Qt.Key.Key_Down:
            self.move("Down")
        if e.key() == qc.Qt.Key.Key_Left:
            self.move("Left")
        if e.key() == qc.Qt.Key.Key_Right:
            self.move("Right")


    def move(self, dir):
        self.pic.setPixelColor(self.headX, self.headY, qc.Qt.gray)
        if dir == "Up":
            self.headY -= 1
        if dir == "Down":
            self.headY += 1
        if dir == "Left":
            self.headX -= 1
        if dir == "Right":
            self.headX += 1
        self.lastDir = dir
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


