# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from moduels.component.OutputBox import OutputBox
from moduels.component.NormalValue import 常量
import os, signal, subprocess
import numpy as np

class Console(QMainWindow):
    # 这个 console 是个子窗口，调用的时候要指定父窗口。例如：window = Console(mainWindow)
    # 里面包含一个 OutputBox, 可以将信号导到它的 print 方法。
    thread = None

    def __init__(self, parent=None):
        super(Console, self).__init__(parent)
        self.initGui()

    def initGui(self):
        self.setWindowTitle(self.tr('命令运行输出窗口'))
        self.resize(1300, 700)
        self.consoleBox = OutputBox() # 他就用于输出用户定义的打印信息
        self.consoleBoxForFFmpeg = OutputBox()  # 把ffmpeg的输出信息用它输出
        self.consoleBox.setParent(self)
        self.consoleBoxForFFmpeg.setParent(self)
        # self.masterLayout = QVBoxLayout()
        # self.masterLayout.addWidget(self.consoleBox)
        # self.masterLayout.addWidget(QPushButton())
        # self.setLayout(self.masterLayout)
        # self.masterWidget = QWidget()
        # self.masterWidget.setLayout(self.masterLayout)
        self.split = QSplitter(Qt.Vertical)
        self.split.addWidget(self.consoleBox)
        self.split.addWidget(self.consoleBoxForFFmpeg)
        self.setCentralWidget(self.split)
        self.show()

    def killPid(self, pid):
        if 常量.platfm == 'Windows':
            # 这个方法可以杀死 subprocess 用了 shell=True 开启的子进程，新测好用！
            # https://stackoverflow.com/questions/13243807/popen-waiting-for-child-process-even-when-the-immediate-child-has-terminated/13256908#13256908
            subprocess.call(f'TASKKILL /F /PID {pid} /T', startupinfo=常量.subprocessStartUpInfo)
        else:
            # 这个没新测，但是 Windows 用不了，只能用于 unix 类的系统
            os.killpg(os.getpgid(self.thread.process.pid), signal.SIGTERM)

    def closeEvent(self, a0: QCloseEvent) -> None:

        self.thread.terminate()

        try:# 关闭 Popen
            for pid in self.thread.已打开的PID:
                self.killPid(pid)
        except Exception as e:
            ...

        try: # 关闭 Popen
            self.killPid(self.thread.process.pid)
        except:
            # print('杀死 thread 中的进程失败')
            ...

        try:  # 关闭已打开的 Thread
            for 子线程 in self.thread.已打开的子线程:
                子线程.kill()
        except Exception as e:
            print(e)

        try: # 关闭已打开文件
            for 文件 in self.thread.已打开的文件:
                if type(文件) == np.memmap:
                    文件._mmap.close()
                else:
                    文件.close()
        except Exception as e:
            print(e)


