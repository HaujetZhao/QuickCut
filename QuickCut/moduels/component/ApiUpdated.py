
class ApiUpdated(QObject):
    signal = pyqtSignal(bool)

    def broadCastUpdates(self):
        self.signal.emit(True)

