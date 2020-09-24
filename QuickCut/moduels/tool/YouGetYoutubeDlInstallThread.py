
# 安装 you-get 和 youtube-dl 进程
class YouGetYoutubeDlInstallThread(QThread):
    signal = pyqtSignal(str)
    signalForFFmpeg = pyqtSignal(str)

    output = None  # 用于显示输出的控件，如一个 QEditBox，它需要有自定义的 print 方法。

    outputTwo = None

    command = None

    def __init__(self, parent=None):
        super(YouGetYoutubeDlInstallThread, self).__init__(parent)

    def print(self, text):
        self.signal.emit(text)

    def printForFFmpeg(self, text):
        self.signalForFFmpeg.emit(text)

    def run(self):
        self.print(self.tr('开始执行命令\n'))
        try:
            if platfm == 'Windows':
                self.process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                universal_newlines=True, encoding='utf-8',
                                                startupinfo=subprocessStartUpInfo)
            else:
                self.process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                universal_newlines=True, encoding='utf-8')
        except:
            self.print(self.tr('安装 you-get 和 youtube-dl 失败了。安装教程请看：https://www.bilibili.com/video/BV18T4y1E7FF?p=5'))
        try:
            for line in self.process.stdout:
                self.printForFFmpeg(line)
        except:
            self.print(
                self.tr('''安装 you-get 和 youtube-dl 失败了。安装教程请看：https://www.bilibili.com/video/BV18T4y1E7FF?p=5'''))
        self.print(self.tr('\n命令执行完毕\n'))
        # except:
        #     self.print('\n\n命令执行出错，可能是系统没有安装必要的软件，如 FFmpeg, you-get, youtube-dl 等等')
