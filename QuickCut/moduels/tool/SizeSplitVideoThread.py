
# 根据大小分割视频
class SizeSplitVideoThread(QThread):
    signal = pyqtSignal(str)
    signalForFFmpeg = pyqtSignal(str)

    ffmpegOutputOption = ''

    inputFile = None
    outputFolder = None

    sizePerClip = None

    cutSwitchValue = None
    cutStartTime = 1
    cutEndTime = None

    clipOutputOption = ''
    # clipOutputOption = '-c copy'

    output = None  # 用于显示输出的控件，如一个 QEditBox，它需要有自定义的 print 方法。

    def __init__(self, parent=None):
        super(SizeSplitVideoThread, self).__init__(parent)

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
        每段输出视频的大小 = int(float(self.sizePerClip) * 1024 * 1024)

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

        总共应导出的时长 = 视频处理的总时长
        try:
            os.mkdir(self.outputFolder)
        except:
            self.print(self.tr('创建输出文件夹失败，可能是已经创建上了\n'))
        continueToCut = True
        i = 1
        ffmpegOutputOption = []
        self.print(self.tr('总共要处理的时长：%s 秒      导出的每个片段大小：%sMB \n') % (视频处理的总时长, self.sizePerClip))
        self.print(self.tr('需要知晓的是：最后导出的视频体积一般会略微超过您预设的大小，比如你设置每个片段为 20MB，实际导出的片段可能会达到 21MB 左右。\n'))
        # 视频处理的总时长
        已导出的总时长 = 0
        while continueToCut:

            # command = ['ffmpeg', 'ss', self.cutStartTime, 't', 每段输出视频的时长, 'i', self.inputFile] + ffmpegOutputOption + [ self.outputFolder + '.' + self.ext]
            command = '''ffmpeg -y -ss %s -t %s -i "%s" -fs %s %s "%s"''' % (
                视频处理的起点时刻, 视频处理的总时长, self.inputFile, 每段输出视频的大小, self.ffmpegOutputOption, self.outputFolder + format(i, '0>6d') + self.ext)
            # self.print(command)
            if platfm == 'Windows':
                self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                universal_newlines=True, encoding='utf-8',
                                                startupinfo=subprocessStartUpInfo)
            else:
                self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                universal_newlines=True, encoding='utf-8')
            self.print(self.tr('\n\n\n\n\n\n\n还有 %s 秒时长的片段要导出，总共已经导出 %s 秒的视频，目前正在导出的是第 %s 个片段……\n') % (format(视频处理的总时长, '.1f'), format(已导出的总时长, '.1f'), i))
            for line in self.process.stdout:
                self.printForFFmpeg(line)
                pass
            新输出的视频的长度 = getMediaTimeLength(self.outputFolder + format(i, '0>6d') + self.ext)
            视频处理的起点时刻 += 新输出的视频的长度
            已导出的总时长 += 新输出的视频的长度
            视频处理的总时长 -= 新输出的视频的长度
            i += 1
            if 总共应导出的时长 - 已导出的总时长 < 1:
                continueToCut = False  # 并且将循环判断依据设为否  也就是剪完下面这一段之后，就不要再继续循环了
        self.print(self.tr('导出完成。\n'))
        self.print(self.tr('应导出 %s 秒，实际导出 %s 秒。\n') % (format(总共应导出的时长, '.1f'), format(已导出的总时长, '.1f')))
