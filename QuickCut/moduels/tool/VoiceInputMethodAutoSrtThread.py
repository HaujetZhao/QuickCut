
# 根据语音输入法生成自动字幕
class VoiceInputMethodAutoSrtThread(QThread):
    signal = pyqtSignal(str)  # 输出打印提示信号。
    signalOfSubtitle = pyqtSignal(srt.Subtitle) # 说出字幕结果。
    output = None  # 用于显示输出的控件，如一个 QEditBox，它需要有自定义的 print 方法。
    mode = 0 # 0 表示半自动模式， 1 表示全自动模式
    inputFile = None # 输入文件。
    offsetTime = None # 时间轴偏移。
    transEngine = None # 字幕引擎。
    srtIndex = None # 字幕的序号。
    regionsList = None # 音频片段。
    regionIndex = 0 # 音频片段的序号。
    regionsListLength = None
    resultTextBox = None # 用于获取识别结果的输入框。
    shortcutKey = None # 用于激活讯飞输入法的快捷键

    def __init__(self, parent=None):
        super(VoiceInputMethodAutoSrtThread, self).__init__(parent)

    def print(self, text):
        self.signal.emit(text)

    def run(self):
        if self.regionIndex <= len(self.regionsList) - 1:
            subtitle = self.transEngine.regionToSubtitle(self.srtIndex, self.offsetTime, self.regionsList[self.regionIndex], self.resultTextBox)
            self.signalOfSubtitle.emit(subtitle)  # 发出字幕
            self.regionIndex += 1
            self.srtIndex += 1
