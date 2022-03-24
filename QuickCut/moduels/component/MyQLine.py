# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from moduels.component.NormalValue import 常量

# 可拖入文件的单行编辑框
class MyQLine(QLineEdit):
    """实现文件拖放功能"""
    signal = Signal(str)

    def __init__(self):
        super().__init__()
        # self.setAcceptDrops(True) # 设置接受拖放动作

    def dragEnterEvent(self, e):
        if True:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):  # 放下文件后的动作
        path = e.mimeData().urls()[0].toLocalFile()
        self.setText(path)
        self.signal.emit(path)
