
# -*- coding: UTF-8 -*-

from PySide2.QtCore import *
import keyboard, time

# 有的语音输入法需要持续不断地收到 press 信号才会认为是在长按一个按键
class PressShortcutKey(QThread):
    shortcutKey = None
    keepPressing = False

    def __init__(self, parent=None):
        super(PressShortcutKey, self).__init__(parent)

    def run(self):
        print('a')
        while self.keepPressing:
            print('press')
            keyboard.press(self.shortcutKey)
            print('sleep')
            time.sleep(0.1)
        print('release')
        keyboard.release(self.shortcutKey)
