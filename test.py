import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class TestListView(QListWidget):


    def __init__(self, type, parent=None):
        super(TestListView, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setIconSize(QtCore.QSize(72, 72))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            print('Has drop Event! ')
        else:
            event.ignore()

class MainForm(QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.view = TestListView(self)
        self.view.fileDropped.connect(self.pictureDropped)
        self.setCentralWidget(self.view)

    def pictureDropped(self, l):
        for url in l:
            if os.path.exists(url):
                print(url)
                icon = QtGui.QIcon(url)
                pixmap = icon.pixmap(72, 72)
                icon = QtGui.QIcon(pixmap)
                item = QtGui.QListWidgetItem(url, self.view)
                item.setIcon(icon)
                item.setStatusTip(url)

def main():
    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()