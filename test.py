import time


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
from PyQt5 import QtCore

class MyThread(QThread):
    sig = pyqtSignal(int)

    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)

    def run(self):
        n = 0
        while True:
            self.sig.emit(n)
            print("run")
            time.sleep(0.3)
            n += 1


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setCentralWidget(QTextEdit())
        self.show()

        self._thread = MyThread()
        # self._thread.sig.connect(self.outText)
        self._thread.start()

    def outText(self, n):
        print(n)


# 这里进入Qt自身的事件循环机制
app = QApplication([])
main = Main()
app.exec_()
