# 打赏对话框
class SponsorDialog(QDialog):
    def __init__(self, parent=None):
        super(SponsorDialog, self).__init__(parent)
        self.resize(784, 890)
        if platfm == 'Darwin':
            self.setWindowIcon(QIcon('misc/icon.icns'))
        else:
            self.setWindowIcon(QIcon('misc/icon.ico'))
        self.setWindowTitle(self.tr('打赏作者'))
        self.exec()

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap('./sponsor.jpg')
        painter.drawPixmap(self.rect(), pixmap)