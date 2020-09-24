
# 可拖入文件的单行编辑框
class MyQLine(QLineEdit):
    """实现文件拖放功能"""
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # self.setAcceptDrops(True) # 设置接受拖放动作

    def dragEnterEvent(self, e):
        if True:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):  # 放下文件后的动作
        if platfm == 'Windows':
            path = e.mimeData().text().replace('file:///', '')  # 删除多余开头
        else:
            path = e.mimeData().text().replace('file://', '')  # 对于 Unix 类系统只删掉两个 '/' 就行了
        self.setText(path)
        self.signal.emit(path)
