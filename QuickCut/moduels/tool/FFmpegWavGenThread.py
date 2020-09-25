# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from moduels.component.NormalValue import 常量
import subprocess, os

# FFmpeg 得到 wav 文件
class FFmpegWavGenThread(QThread):
    signal = Signal(str)
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
        if 常量.platfm == 'Windows':
            self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                            universal_newlines=True, encoding='utf-8',
                                            startupinfo=常量.subprocessStartUpInfo)
        else:
            self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                            universal_newlines=True, encoding='utf-8')
        for line in self.process.stdout:
            pass
        self.signal.emit('%s.wav' % (pathPrefix))
        print('%s.wav' % (pathPrefix))

