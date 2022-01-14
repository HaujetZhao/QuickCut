# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *


# 可以状态栏提示的 ComboBox
class HintCombobox(QComboBox):

    hint = None

    def __init__(self):
        super().__init__()

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

