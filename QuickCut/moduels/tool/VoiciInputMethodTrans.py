# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from moduels.component.NormalValue import 常量
from moduels.tool.PressShortcutKey import PressShortcutKey
from moduels.component._BufferedReaderForFFmpeg import _BufferedReaderForFFmpeg
from moduels.other import auditok
import os, subprocess, srt, time, datetime

class VoiciInputMethodTrans():
    min_dur = 0.2  # 最短时间
    max_dur = 10  # 最长时间
    max_silence = 0.1  # 允许在这个片段中存在的静音片段的最长时间
    energy_threshold = 50  # it is the log energy of the signal computed as: 10 . log10 dot(x, x) / |x|
    inputMethodHotkeySleepTime = 3.5
    timestampFile = ''

    def __init__(self, shortcutKey):
        self.pressShortcutKeyThread = PressShortcutKey()
        self.pressShortcutKeyThread.shortcutKey = shortcutKey


    def regionToSubtitle(self, index, offsetTime, region, 语音输入结果采集框):
        语音输入结果采集框.setFocus()
        语音输入结果采集框.clear()
        self.pressShortcutKeyThread.keepPressing = True
        self.pressShortcutKeyThread.start()
        time.sleep(0.2)
        region.play(progress_bar=False)
        print('release shortcut')
        self.pressShortcutKeyThread.keepPressing = False
        语音输入结果采集框.setFocus()
        time.sleep(self.inputMethodHotkeySleepTime) # 这里需要多休息一下，否则在文字出来后很快再按下快捷键，讯飞输入法有可能反应不过来，不响应快捷键
        subContent = 语音输入结果采集框.text()
        if subContent != '':
            if subContent[-1] == '。' or subContent[-1] == '.' :
                subContent = subContent[0:-1]
        语音输入结果采集框.clear()
        start = region.meta.start + offsetTime  # 真实起始时间（秒数）
        end = start + region.duration # 真实结束时间（秒数）
        startTime = datetime.timedelta(seconds=int(start), microseconds=start * 1000 % 1000 * 1000)
        endTime = datetime.timedelta(seconds=int(end), microseconds=end * 1000 % 1000 * 1000)
        subtitle = srt.Subtitle(index=index, start=startTime, end=endTime, content=subContent)
        return subtitle



    def getRegions(self, wavFile):
        if self.timestampFile != '':
            try:
                regions = []
                srtTimestampFile = os.path.dirname(self.timestampFile) + '/timestamp.srt'
                command = '''ffmpeg -y -hide_banner -i %s %s''' % (self.timestampFilem, srtTimestampFile)
                print(srtTimestampFile)
                print(command)
                try:
                    if 常量.platfm == 'Windows':
                        # command = self.command.encode('gbk').decode('gbk')
                        self.process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE,
                                                        stderr=subprocess.STDOUT, startupinfo=常量.subprocessStartUpInfo)
                    else:
                        self.process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE,
                                                        stderr=subprocess.STDOUT,
                                                        start_new_session=True)
                except:
                    print(self.tr(
                        '出错了，本次运行的命令是：\n\n%s\n\n你可以将上面这行命令复制到 cmd 窗口运行下，看看报什么错，如果自己解决不了，把那个报错信息发给开发者。\n\n') % scommand)
                try:
                    stdout = _BufferedReaderForFFmpeg(self.process.stdout.raw)
                    while True:
                        line = stdout.readline()
                        if not line:
                            break
                        try:
                            print(line.decode('utf-8'))
                        except UnicodeDecodeError:
                            print(line.decode('gbk'))
                except:
                    print(
                        self.tr(
                            '''出错了，本次运行的命令是：\n\n%s\n\n你可以将上面这行命令复制到 cmd 窗口运行下，看看报什么错，如果自己解决不了，把那个报错信息发给开发者\n''') % command)

                with open(srtTimestampFile, 'r') as f:
                    timestampSubtitles = srt.parse(f.read())
                    print(timestampSubtitles)
                for timestampSubtitle in timestampSubtitle:
                    start = timestampSubtitle.start.seconds + (timestampSubtitle.start.microseconds / 1000000)
                    end = timestampSubtitle.end.seconds + (timestampSubtitle.end.microseconds / 1000000)
                    region = auditok.AudioRegion()
            except:
                    print('索引文件无效，继续使用 auditok 依据声音做分段')
        else:
            self.drop_trailing_silence = False  # 是否切除尾随的静音片段，如果切除可能会导致话末断音
            self.strict_min_dur = False
            try:
                regions = auditok.split(wavFile, self.min_dur, self.max_dur, self.max_silence,
                                        self.drop_trailing_silence, self.strict_min_dur,
                                        energy_threshold=self.energy_threshold)
            except:
                return False
            # print(len(list(regions))) # 好奇怪，在这里 len 可以显示正确数值，但是在返回后用 len 返回的结果是0
            return list(regions)


