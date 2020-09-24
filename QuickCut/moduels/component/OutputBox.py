
# 命令输出窗口中的多行文本框
class OutputBox(QTextEdit):
    # 定义一个 QTextEdit 类，写入 print 方法。用于输出显示。
    def __init__(self, parent=None):
        super(OutputBox, self).__init__(parent)
        self.setReadOnly(True)

    def print(self, text):
        try:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(text)
            self.setTextCursor(cursor)
            self.ensureCursorVisible()
        except:
            pass
        pass
