
# FFmpeg 得到 wav 文件
class FFmpegWavGenThread(QThread):
    signal = pyqtSignal(str)
    mediaFile = None
    startTime = None
    endTime = None


    def __init__(self, parent=None):
        super(FFmpegWavGenThread, self).__init__(parent)


    def run(self):
        # 得到输入文件除了除了扩展名外的名字
        pathPrefix = os.path.splitext(self.mediaFile)[0]
        # ffmpeg 命令
        command = 'ffmpeg -hide_banner -y -ss %s -to %s -i "%s" -ac 1 -ar 16000 "%s.wav"' % (
            self.startTime, self.endTime, self.mediaFile, pathPrefix)
        if platfm == 'Windows':
            self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                            universal_newlines=True, encoding='utf-8',
                                            startupinfo=subprocessStartUpInfo)
        else:
            self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                            universal_newlines=True, encoding='utf-8')
        for line in self.process.stdout:
            pass
        self.signal.emit('%s.wav' % (pathPrefix))

