
# 根据时长分割视频
class DurationSplitVideoThread(QThread):
    signal = pyqtSignal(str)
    signalForFFmpeg = pyqtSignal(str)

    ffmpegOutputOption = ''

    inputFile = None
    outputFolder = None

    durationPerClip = None

    cutSwitchValue = None
    cutStartTime = 1
    cutEndTime = None

    clipOutputOption = ''
    # clipOutputOption = '-c copy'

    output = None  # 用于显示输出的控件，如一个 QEditBox，它需要有自定义的 print 方法。

    def __init__(self, parent=None):
        super(DurationSplitVideoThread, self).__init__(parent)

    def print(self, text):
        self.signal.emit(text)

    def printForFFmpeg(self, text):
        self.signalForFFmpeg.emit(text)

    def run(self):
        视频的起点时刻 = 0
        视频文件的总时长 = getMediaTimeLength(self.inputFile)  # 得到视频的整个时长

        视频处理的起点时刻 = 视频的起点时刻
        视频处理的总时长 = 视频文件的总时长

        self.ext = os.path.splitext(self.inputFile)[1]  # 得到输出后缀
        每段输出视频的时长 = float(strTimeToSecondsTime(self.durationPerClip))  # 将片段时长从字符串变为浮点数

        # 如果设置了从中间一段进行分段，那么就重新设置一下起始时间和总共时长
        if self.cutSwitchValue == True:
            视频处理的起点时刻 = strTimeToSecondsTime(self.cutStartTime)
            if 视频处理的起点时刻 >= 视频文件的总时长:
                视频处理的起点时刻 = 0
            用户输入的截止时刻 = strTimeToSecondsTime(self.cutEndTime)
            if 用户输入的截止时刻 > 0:
                if 用户输入的截止时刻 > 视频文件的总时长:
                    视频处理的总时长 = 视频文件的总时长 - 视频处理的起点时刻
                else:
                    视频处理的总时长 = 用户输入的截止时刻 - 视频处理的起点时刻
            else:
                视频处理的总时长 = 视频文件的总时长 - 视频处理的起点时刻

        try:
            os.mkdir(self.outputFolder)
        except:
            self.print(self.tr('创建输出文件夹失败，可能是已经创建上了\n'))
        continueToCut = True
        i = 1
        totalClipNumber = math.ceil(视频处理的总时长 / 每段输出视频的时长)
        ffmpegOutputOption = []
        self.print(self.tr('总共要处理的时长：%s 秒      导出的每个片段时长：%s 秒 \n') % (视频处理的总时长, 每段输出视频的时长))
        while continueToCut:
            if 视频处理的总时长 <= 每段输出视频的时长:
                每段输出视频的时长 = 视频处理的总时长  # 当剩余时间的长度已经小于需要的片段时,就将最后这段时间长度设为剩余时间
                continueToCut = False  # 并且将循环判断依据设为否  也就是剪完下面这一段之后，就不要再继续循环了
            self.print(self.tr('总共有 %s 个片段要导出，现在导出第 %s 个……\n') % (totalClipNumber, i))
            # command = ['ffmpeg', 'ss', self.cutStartTime, 't', 每段输出视频的时长, 'i', self.inputFile] + ffmpegOutputOption + [ self.outputFolder + '.' + self.ext]
            command = '''ffmpeg -y -ss %s -t %s -i "%s" %s "%s"''' % (
            视频处理的起点时刻, 每段输出视频的时长, self.inputFile, self.ffmpegOutputOption, self.outputFolder + format(i, '0>6d') + self.ext)
            # self.print(command)
            if platfm == 'Windows':
                self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                universal_newlines=True, encoding='utf-8',
                                                startupinfo=subprocessStartUpInfo)
            else:
                self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                universal_newlines=True, encoding='utf-8')
            for line in self.process.stdout:
                self.printForFFmpeg(line)
                pass
            视频处理的起点时刻 += 每段输出视频的时长
            视频处理的总时长 -= 每段输出视频的时长
            i += 1
        self.print(self.tr('导出完成\n'))
