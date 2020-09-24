
# 命令输出窗口中的多行文本框，此处用于接收语音识别识别出的文本
class OutputLineBox(QLineEdit):
    # 定义一个 QTextEdit 类，写入 print 方法。用于输出显示。
    def __init__(self, parent=None):
        super(OutputLineBox, self).__init__(parent)

