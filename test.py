# 托盘参考：
# https://blog.csdn.net/wukai_std/article/details/67639985
# https://blog.csdn.net/daiyinger/article/details/52700738
# 重写关闭事件参考：
# https://blog.csdn.net/u010139869/article/details/79483274

from PyQt5.QtWidgets import QWidget, QAction, QSystemTrayIcon, QMenu, QApplication, QDialog
from PyQt5.QtGui import QIcon, QPixmap, QColor
import sys


class Tray(QWidget):

    def __init__(self):
        super(self.__class__, self).__init__()

        self.winIconPix = QPixmap(16, 16)
        self.winIconPix.fill(QColor(0, 0, 100))
        self.setWindowIcon(QIcon(self.winIconPix))

        self.tray = QSystemTrayIcon(self)
        self.trayIconPix = QPixmap(16, 16)
        self.trayIconPix.fill(QColor(100, 0, 0))
        self.tray.setIcon(QIcon(self.trayIconPix))

        minimizeAction = QAction("Mi&nimize", self, triggered = self.hide)
        maximizeAction = QAction("Ma&ximize", self, triggered = self.showMaximized)
        restoreAction = QAction("&Restore", self, triggered = self.showNormal)
        quitAction = QAction("&Quit", self, triggered = QApplication.instance().quit)  # 退出APP
        self.trayMenu = QMenu(self)
        self.trayMenu.addAction(minimizeAction)
        self.trayMenu.addAction(maximizeAction)
        self.trayMenu.addAction(restoreAction)
        self.trayMenu.addSeparator()
        self.trayMenu.addAction(quitAction)
        self.tray.setContextMenu(self.trayMenu)

        self.tray.show()
        self.show()

    def closeEvent(self, event):
        event.ignore()  # 忽略关闭事件
        self.hide()  # 隐藏窗体


app = QApplication(sys.argv)
win = Tray()
sys.exit(app.exec_())

# class TrayDlg(QDialog):
#
#     def __init__(self):
#         super(self.__class__, self).__init__()
#
#         self.winIconPix = QPixmap(16, 16)
#         self.winIconPix.fill(QColor(0, 0, 100))
#         self.setWindowIcon(QIcon(self.winIconPix))
#
#         self.tray = QSystemTrayIcon(self)
#         self.trayIconPix = QPixmap(16, 16)
#         self.trayIconPix.fill(QColor(100, 0, 0))
#         self.tray.setIcon(QIcon(self.trayIconPix))
#
#         minimizeAction = QAction("Mi&nimize", self, triggered = self.hide)
#         maximizeAction = QAction("Ma&ximize", self, triggered = self.showMaximized)
#         restoreAction = QAction("&Restore", self, triggered = self.showNormal)
#         quitAction = QAction("&Quit", self, triggered = self.close)
#
#         self.trayMenu = QMenu(self)
#         self.trayMenu.addAction(minimizeAction)
#         self.trayMenu.addAction(maximizeAction)
#         self.trayMenu.addAction(restoreAction)
#         self.trayMenu.addSeparator()
#         self.trayMenu.addAction(quitAction)
#         self.tray.setContextMenu(self.trayMenu)
#
#         self.tray.show()
#         sys.exit(self.exec_())
#
#     def closeEvent(self, event):
#         if self.tray.isVisible():
#             self.tray.hide()
#
# app = QApplication(sys.argv)
# win2 = TrayDlg()
# sys.exit(app.exec_())