# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *

# 可以状态栏提示的标签
class HintLabel(QLabel):

    hint = None

    def __init__(self, text):
        super().__init__()
        self.setText(text)
        # self.setAlignment(Qt.AlignCenter)

    def enterEvent(self, *args, **kwargs):
        if self.hint != None:
            try:
                mainWindow.状态栏.showMessage(self.hint)
            except:
                pass

    def leaveEvent(self, *args, **kwargs):
        if self.hint != None:
            try:
                mainWindow.状态栏.showMessage('')
            except:
                pass
