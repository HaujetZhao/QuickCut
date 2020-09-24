class Stream(QObject):
    # 用于将控制台的输出定向到一个槽
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))
        QApplication.processEvents()