# -*- coding: UTF-8 -*-

from PySide2.QtCore import *

class ApiUpdated(QObject):
    signal = Signal(bool)

    def broadCastUpdates(self):
        self.signal.emit(True)

