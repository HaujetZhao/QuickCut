# -*- coding: UTF-8 -*-


from PySide2.QtCore import *
import subprocess

from moduels.component.NormalValue import 常量
from moduels.component._BufferedReaderForFFmpeg import _BufferedReaderForFFmpeg

class CommandThread(QThread):
    signal = Signal(str)
    signalForFFmpeg = Signal(str)

    output = None  # 用于显示输出的控件，如一个 QEditBox，它需要有自定义的 print 方法。

    outputTwo = None

    command = None

    def __init__(self, parent=None):
        super(CommandThread, self).__init__(parent)

    def print(self, text):
        self.signal.emit(text)

    def printForFFmpeg(self, text):
        self.signalForFFmpeg.emit(text)

    def run(self):
        self.print(self.tr('开始执行命令\n'))
        try:
            if 常量.platfm == 'Windows':
                # command = self.command.encode('gbk').decode('gbk')
                self.process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE,
                                                stderr=subprocess.STDOUT, startupinfo=常量.subprocessStartUpInfo)
            else:
                self.process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                start_new_session=True)
        except:
            self.print(self.tr('出错了，本次运行的命令是：\n\n%s\n\n你可以将上面这行命令复制到 cmd 窗口运行下，看看报什么错，如果自己解决不了，把那个报错信息发给开发者。如果是 you-get 和 youtube-dl 的问题，请查看视频教程：https://www.bilibili.com/video/BV18T4y1E7FF?p=5\n\n') % self.command)
        try:
            stdout = _BufferedReaderForFFmpeg(self.process.stdout.raw)
            while True:
                line = stdout.readline()
                if not line:
                    break
                try:
                    self.printForFFmpeg(line.decode('utf-8'))
                except UnicodeDecodeError:
                    self.printForFFmpeg(line.decode('gbk'))
        except:
            self.print(
                self.tr('''出错了，本次运行的命令是：\n\n%s\n\n你可以将上面这行命令复制到 cmd 窗口运行下，看看报什么错，如果自己解决不了，把那个报错信息发给开发者\n''') % self.command)
        self.print(self.tr('\n命令执行完毕\n'))
