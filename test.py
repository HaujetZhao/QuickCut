import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import subprocess

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initGui()
    def initGui(self):
        self.btn1 = QPushButton('btn1')
        self.btn1.clicked.connect(self.command)
        self.setCentralWidget(self.btn1)
        self.show()
    def command(self):
        self.console = Console(self)
        self.console.show()

# class Console(QMainWindow):
#     def __init__(self):
#         super().__init__()
class Console(QMainWindow):
    def __init__(self, parent=None):
        super(Console, self).__init__(parent)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())



#
# class First(QMainWindow):
#     def __init__(self, parent=None):
#         super(First, self).__init__(parent)
#         self.pushButton = QPushButton("click me")
#
#         self.setCentralWidget(self.pushButton)
#
#         self.pushButton.clicked.connect(self.on_pushButton_clicked)
#         # self.dialog = Second(self)
#
#     def on_pushButton_clicked(self):
#         self.dialog = Second(self)
#         self.dialog.show()
# class Second(QMainWindow):
#     def __init__(self, parent=None):
#         super(Second, self).__init__(parent)
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main = First()
#     main.show()
#     sys.exit(app.exec_())