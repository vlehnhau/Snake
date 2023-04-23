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



if __name__=="__main__":
    app = qw.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


