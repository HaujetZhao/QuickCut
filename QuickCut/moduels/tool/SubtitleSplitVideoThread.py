# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from moduels.component.NormalValue import 常量
from moduels.function.strTimeToSecondsTime import strTimeToSecondsTime


import os, re, srt, subprocess, datetime

# 根据字幕分割视频
class SubtitleSplitVideoThread(QThread):
    signal = Signal(str)
    signalForFFmpeg = Signal(str)

    ffmpegOutputOption = ''

    inputFile = None
    subtitleFile = None
    outputFolder = None

    cutSwitchValue = None
    cutStartTime = None
    cutEndTime = None

    subtitleOffset = None

    exportClipSubtitle = None

    clipOutputOption = ''
    subtitleNumberPerClip = 1
    # clipOutputOption = '-c copy'

    output = None  # 用于显示输出的控件，如一个 QEditBox，它需要有自定义的 print 方法。

    inputFile = None

    def __init__(self, parent=None):
        super(SubtitleSplitVideoThread, self).__init__(parent)

    def print(self, text):
        self.signal.emit(text)

    def printForFFmpeg(self, text):
        self.signalForFFmpeg.emit(text)

    def run(self):
        # try:
        subtitleSplit = os.path.splitext(self.subtitleFile)
        subtitleName = subtitleSplit[0]
        subtitleExt = subtitleSplit[1]
        inputFileExt = os.path.splitext(self.inputFile)[1]
        # clipOutputOption = ''

        if self.cutSwitchValue != 0:
            if self.cutStartTime != '':  # 如果开始时间不为空，转换为秒数
                self.cutStartTime = strTimeToSecondsTime(self.cutStartTime)
                print(self.cutStartTime)
            if self.cutEndTime != '':  # 如果结束时间不为空，转换为秒数
                self.cutEndTime = strTimeToSecondsTime(self.cutEndTime)
                print(self.cutEndTime)

        if re.match('\.ass', subtitleExt, re.IGNORECASE):
            self.print(self.tr('字幕是ass格式，先转换成srt格式\n'))
            command = '''ffmpeg -y -hide_banner -i "%s" "%s" ''' % (self.subtitleFile, subtitleName + '.srt')
            self.process = subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                           universal_newlines=True)
            # for line in self.process.stdout:
            #     self.print(line)
            self.print(self.tr('格式转换完成\n'))
            self.subtitleFile = subtitleName + '.srt'
            try:
                f = open(self.subtitleFile, 'r')
                with f:
                    subtitleContent = f.read()
                try:
                    os.remove(self.subtitleFile)
                except:
                    self.print(self.tr('删除生成的srt字幕失败'))
            except:
                f = open(self.subtitleFile, 'r', encoding='utf-8')
                with f:
                    subtitleContent = f.read()
                try:
                    os.remove(self.subtitleFile)
                except:
                    self.print(self.tr('删除生成的srt字幕失败'))
        elif re.match('\.mkv', subtitleExt, re.IGNORECASE):
            self.print(self.tr('字幕是 mkv 格式，先转换成srt格式\n'))
            command = '''ffmpeg -y -hide_banner -i "%s" -an -vn "%s" ''' % (self.subtitleFile, subtitleName + '.srt')
            self.process = subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                           universal_newlines=True)
            # for line in self.process.stdout:
            #     self.print(line)
            self.print(self.tr('格式转换完成\n'))
            self.subtitleFile = subtitleName + '.srt'
            try:
                f = open(self.subtitleFile, 'r')
                with f:
                    subtitleContent = f.read()
                try:
                    os.remove(self.subtitleFile)
                except:
                    self.print(self.tr('删除生成的srt字幕失败'))
            except:
                f = open(self.subtitleFile, 'r', encoding='utf-8')
                with f:
                    subtitleContent = f.read()
                try:
                    os.remove(self.subtitleFile)
                except:
                    self.print(self.tr('删除生成的srt字幕失败'))
        elif re.match('\.vtt', subtitleExt, re.IGNORECASE):
            self.print(self.tr('字幕是 vtt 格式，先转换成srt格式\n'))
            command = '''ffmpeg -y -hide_banner -i "%s" -an -vn "%s" ''' % (self.subtitleFile, subtitleName + '.srt')
            self.process = subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                           universal_newlines=True)
            # for line in self.process.stdout:
            #     self.print(line)
            self.print(self.tr('格式转换完成\n'))
            self.subtitleFile = subtitleName + '.srt'
            try:
                f = open(self.subtitleFile, 'r')
                with f:
                    subtitleContent = f.read()
                try:
                    os.remove(self.subtitleFile)
                except:
                    self.print(self.tr('删除生成的srt字幕失败'))
            except:
                f = open(self.subtitleFile, 'r', encoding='utf-8')
                with f:
                    subtitleContent = f.read()
                try:
                    os.remove(self.subtitleFile)
                except:
                    self.print(self.tr('删除生成的srt字幕失败'))
        elif re.match('\.srt', subtitleExt, re.IGNORECASE):
            try:
                with open(self.subtitleFile, 'r', encoding='utf-8') as f:
                    subtitleContent = f.read()
            except:
                with open(self.subtitleFile, 'r', encoding='gbk') as f:
                    subtitleContent = f.read()
        else:
            self.print(
                self.tr('字幕格式只支持 srt、ass 和 vtt，以及带内置字幕的 mkv 文件，暂不支持您所选的字幕。\n\n如果您的字幕输入是 mkv 而失败了，则有可能您的 mkv 视频没有字幕流，画面中的字幕是烧到画面中的。'))
            return False
        # srt.parse
        srtObject = srt.parse(subtitleContent)
        srtList = list(srtObject)
        totalNumber = len(srtList)
        try:
            os.mkdir(self.outputFolder)
        except:
            self.print(self.tr('创建输出文件夹失败，可能是已经创建上了\n'))
        for i in range(0, totalNumber, self.subtitleNumberPerClip):
            # Subtitle(index=2, start=datetime.timedelta(seconds=11, microseconds=800000), end=datetime.timedelta(seconds=13, microseconds=160000), content='该喝水了', proprietary='')
            self.print(self.tr('总共有 %s 段要处理，现在开始导出第 %s 段……\n') % (int(totalNumber / self.subtitleNumberPerClip), int(
                (i + self.subtitleNumberPerClip) / self.subtitleNumberPerClip)))
            start = srtList[i].start.seconds + (srtList[i].start.microseconds / 1000000) + self.subtitleOffset
            end = srtList[i + self.subtitleNumberPerClip - 1].end.seconds + (
                        srtList[i].end.microseconds / 1000000) + self.subtitleOffset
            duration = end - start
            if start < 0:
                start = 0
            if end < 0:
                end = 0
            if self.cutSwitchValue != 0:  # 如果确定要剪切一个区间
                print
                if self.cutStartTime != '':  # 如果起始时间不为空
                    if end < self.cutStartTime:
                        continue
                if self.cutEndTime != '':
                    if start > self.cutEndTime:
                        continue
            index = format(srtList[i].index, '0>6d')
            command = 'ffmpeg -y -ss %s -to %s -i "%s" %s "%s"' % (
            start, end, self.inputFile, self.ffmpegOutputOption, self.outputFolder + index + inputFileExt)
            if 常量.platfm == 'Windows':
                self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                universal_newlines=True, encoding='utf-8',
                                                startupinfo=常量.subprocessStartUpInfo)
            else:
                self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                universal_newlines=True, encoding='utf-8')
            for line in self.process.stdout:
                self.printForFFmpeg(line)
                pass
            if self.exportClipSubtitle != 0:
                subtitles = []
                for j in range(0, self.subtitleNumberPerClip, 1):
                    startTime = (srtList[i + j].start.seconds + srtList[i + j].start.microseconds / 1000000) - (
                                srtList[i].start.seconds + srtList[i].start.microseconds / 1000000)
                    startSeconds = int(startTime)
                    startMicroseconds = startTime * 1000 % 1000 * 1000
                    duration = (srtList[i + j].end.seconds + srtList[i + j].end.microseconds / 1000000) - (
                                srtList[i + j].start.seconds + srtList[i + j].start.microseconds / 1000000)
                    endTime = startTime + duration
                    endSeconds = int(endTime)
                    endMicroseconds = endTime * 1000 % 1000 * 1000
                    startTime = datetime.timedelta(seconds=startSeconds, microseconds=startMicroseconds)
                    endTime = datetime.timedelta(seconds=endSeconds, microseconds=endMicroseconds)
                    subContent = srtList[i + j].content

                    subtitle = srt.Subtitle(index=j + 1, start=startTime, end=endTime, content=subContent)
                    subtitles.append(subtitle)
                srtSub = srt.compose(subtitles, reindex=True, start_index=1, strict=True)
                srtPath = self.outputFolder + index + '.srt'
                with open(srtPath, 'w+') as srtFile:
                    srtFile.write(srtSub)
                pass

        self.print(self.tr('导出完成\n'))

        # self.print(os.path.splitext(self.subtitleFile)[1])
        # except:
        #     self.print('分割过程出错了')
