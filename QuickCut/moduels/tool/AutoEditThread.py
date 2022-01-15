# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from moduels.component.NormalValue import 常量
from moduels.tool.AliOss import AliOss
from moduels.tool.TencentOss import TencentOss
from moduels.tool.AliTrans import AliTrans
from moduels.tool.TencentTrans import TencentTrans
from moduels.function.getProgram import getProgram

import os, re, math, time, sqlite3, srt, ffmpeg, threading, av, cv2
import numpy as np
from shutil import rmtree, move
from scipy.io import wavfile
from audiotsm2 import phasevocoder
from audiotsm2.io.array import ArrReader, ArrWriter

from os import path
import json
import subprocess
import shlex
from pathlib import Path
import platform
import io
import tempfile

os.environ['PATH'] += os.pathsep + os.path.abspath('./bin/Windows')  # 将可执行文件的目录加入环境变量
os.environ['PATH'] += os.pathsep + os.path.abspath('./bin/MacOS')  # 将可执行文件的目录加入环境变量


# from moduels.tool.JumpCut import *


def 查找可执行程序(program):
    """
    Return the path for a given executable.
    """

    def is_exe(file_path):
        """
        Checks whether a file is executable.
        """
        return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            import platform
            if platform.system() == 'Windows':
                exe_file += '.exe'
            if is_exe(exe_file):
                return exe_file



# 自动剪辑
class AutoEditThread(QThread):
    signal = Signal(str)
    signalForFFmpeg = Signal(str)

    output = None  # 用于显示输出的控件，如一个 QEditBox，它需要有自定义的 print 方法。

    输入文件 = ''
    输出文件 = ''
    字幕文件 = ''
    静音片段倍速 = 1
    响亮片段倍速 = 2
    片段间缓冲帧数 = 3
    静音阈值 = 0.025
    只处理音频 = False
    提取选项 = '-c:v mjpeg -qscale:v 3'
    输出选项 = ''
    使用辅助字幕 = False
    剪去片段关键词 = ''
    保留片段关键词 = ''

    临时文件夹 = 'TEMP'
    停止循环 = False

    def __init__(self, parent=None):
        super(AutoEditThread, self).__init__(parent)

    def print(self, text):
        self.signal.emit(text)

    def printForFFmpeg(self, text):
        self.signalForFFmpeg.emit(text)

    def 创建文件夹(self, s):
        try:
            os.mkdir(s)
        except:
            return False
        return True

    def 删除文件夹(self, folder):  # 极度危险的函数，小心使用！
        if not path.exists(folder):
            return True
        try:
            rmtree(folder, ignore_errors=False)
        except OSError:
            self.print(OSError)
            return False
        return True

    def 执行ffmpeg命令(self, command):
        if 常量.platfm == 'Windows':
            self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                            universal_newlines=True, encoding='utf-8',
                                            startupinfo=常量.subprocessStartUpInfo)
        else:
            self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                            universal_newlines=True, encoding='utf-8')
        for line in self.process.stdout:
            self.printForFFmpeg(line)

    def 创建临时文件夹(self):
        # 如果临时文件已经存在，就删掉
        临时文件夹路径 = path.splitext(self.输入文件)[0] + '_TEMP'
        if not self.删除文件夹(临时文件夹路径):
            self.print('检测到临时文件夹存在，但无法删除，停止自动剪辑\n')
            self.print('请手动检查删除该目录：%s\n' % 临时文件夹路径)
            return False

        # 创建临时文件夹
        self.print(self.tr('新建临时文件夹：%s \n\n') % 临时文件夹路径)
        if not self.创建文件夹(临时文件夹路径):
            self.print(self.tr('临时文件夹（%s）创建失败，自动剪辑停止，请检查权限\n\n') % 临时文件夹路径)
            return False
        
        return 临时文件夹路径
    
    def 获取音视频流信息(self):
        查询命令 = f'ffprobe -of json -select_streams v -show_streams "{self.输入文件}"'
        查询结果 = json.loads(subprocess.run(shlex.split(查询命令), capture_output=True, encoding='utf-8').stdout)
        self.视频流信息 = 查询结果

        查询命令 = f'ffprobe -of json -select_streams a -show_streams "{self.输入文件}"'
        查询结果 = json.loads(subprocess.run(shlex.split(查询命令), capture_output=True, encoding='utf-8').stdout)
        self.音频流信息 = 查询结果
    
    def 检查输入文件是否只含音频(self):
        if not self.视频流信息['streams']:  # 没有视频轨
            self.print(f'无法得到视频帧率，认为输入只包含音频\n\n')
            self.只处理音频 = True
    
    def 得到输入视频帧率(self):
        if self.只处理音频: return 30
        try:
            return  float(eval(self.视频流信息['streams'][0]['avg_frame_rate']))
        except: 
            self.print(f'无法获取视频帧率，停止任务\n\n')
            return False
    
    def 得到输入音频采样率(self):
        try:
            return  float(eval(self.音频流信息['streams'][0]['sample_rate']))
        except:
            self.print(f'无法获取音频采样率，停止任务\n\n')
            return False
    
    def 提取音频流(self, 输入文件, 输出文件, 音频采样率):
        command = f'ffmpeg -hide_banner -i "{输入文件}" -ac 2 -ar {音频采样率} -vn "{输出文件}"'
        进程 = subprocess.run(command, stderr=subprocess.PIPE)
        return
    
    def 由音频得到片段列表(self, 音频文件, 视频帧率, 声音检测相对阈值, 片段间缓冲帧数):
        # 变量 音频采样率, 总音频数据 ，得到采样总数为 wavfile.read("audio.wav").shape[0] ，（shape[1] 是声道数）
        采样率, 总音频数据 = wavfile.read(音频文件, mmap=True)
        总音频采样数 = 总音频数据.shape[0]

        最大音量 = self.得到最大音量(总音频数据)
        if 最大音量 == 0: 最大音量 = 1
        每帧采样数 = 采样率 / 视频帧率
        总音频帧数 = int(math.ceil(总音频采样数 / 每帧采样数))
        hasLoudAudio = np.zeros((总音频帧数))

        # 这里给每一帧音频标记上是否超过阈值
        for i in range(总音频帧数):
            该帧音频起始 = int(i * 每帧采样数)
            该帧音频结束 = min(int((i + 1) * 每帧采样数), 总音频采样数)
            单帧音频区间 = 总音频数据[该帧音频起始:该帧音频结束]
            单帧音频最大相对音量 = float(self.得到最大音量(单帧音频区间)) / 最大音量
            if 单帧音频最大相对音量 >= 声音检测相对阈值:
                hasLoudAudio[i] = 1

        # 按声音阈值划分片段
        片段列表 = [[0, 0, 0]]
        shouldIncludeFrame = np.zeros((总音频帧数))  # 返回一个数量为 音频总帧数 的列表，默认数值为0，用于存储是否该存储这一帧
        for i in range(总音频帧数):
            start = int(max(0, i - 片段间缓冲帧数))
            end = int(min(总音频帧数, i + 1 + 片段间缓冲帧数))
            # 如果从加上淡入淡出的起始到最后之间的几帧中，有1帧是要保留的，那就保留这一区间所有的
            shouldIncludeFrame[i] = np.max(hasLoudAudio[start:end])
            # 如果这一帧不是总数第一帧 且 是否保留这一帧 与 前一帧 不同
            if (i >= 1 and shouldIncludeFrame[i] != shouldIncludeFrame[i - 1]):  # Did we flip?
                片段列表.append([片段列表[-1][1], i, int(shouldIncludeFrame[i - 1])])
        片段列表.append([片段列表[-1][1], 总音频帧数, int(shouldIncludeFrame[i - 1])])  # 加一个最后那几帧要不要保留
        片段列表.pop(0)  # 把片段列表中开头那个开始用于占位的 [0,0,0]去掉
        self.print(f'静音、响亮片段分析完成\n')
        return 片段列表
    
    def 使用字幕进一步处理片段列表(self, srt字幕):
        self.print('\n开始根据字幕中的关键词二次处理片段\n\n')
        
        with open(srt字幕, "r", encoding='utf-8') as f:
            字幕内容 = f.read()
        字幕列表 = list(srt.parse(字幕内容))
        字幕关键句列表 = []
        for index in 字幕列表:
            if re.match(f'({self.剪去片段关键词})|({self.保留片段关键词})$', index.content):
                字幕关键句列表.append(index)
        上一句的结束帧 = 0
        # 每一个关键句的影响范围是:上一句的结束帧,到这一句的结束帧
        
        SegI = 2 # 令 SegI 表示「self.片段列表」的索引
        for index, 关键句 in enumerate(字幕关键句列表):
            SegI -= 2
            if index > 0:
                上一句的结束帧 = int(
                    (
                            字幕关键句列表[index - 1].end.seconds +
                            字幕关键句列表[index - 1].end.microseconds / 1000000
                    )
                    * self.视频帧率
                ) + 10
            这一句的起始帧 = int((关键句.start.seconds + 关键句.start.microseconds / 1000000) * self.视频帧率) - 4
            这一句的结束帧 = int((关键句.end.seconds + 关键句.end.microseconds / 1000000) * self.视频帧率) + 10

            if re.match(f'({self.剪去片段关键词})', 关键句.content):
                while SegI < len(self.片段列表):
                    if self.片段列表[SegI][0] < 上一句的结束帧:
                        if self.片段列表[SegI][1] <= 上一句的结束帧:
                            # 这个片段在 cut 区间左侧，不管
                            SegI += 1
                        else:
                            if self.片段列表[SegI][1] <= 这一句的结束帧:
                                # 把进来的部分截去
                                self.片段列表[SegI][1] = 上一句的结束帧
                                SegI += 1
                            else:
                                # 这个片段整个盖信本 save 区间了,要截断,删掉左边一段
                                temp = self.片段列表[SegI]
                                temp[0] = 这一句的结束帧
                                self.片段列表[SegI][1] = 上一句的结束帧
                                self.片段列表.insert(SegI + 1, temp)
                                SegI += 1
                    elif self.片段列表[SegI][0] < 这一句的结束帧:
                        if self.片段列表[SegI][1] <= 这一句的结束帧:
                            del self.片段列表[SegI]
                        else:
                            self.片段列表[SegI][0] = 这一句的结束帧
                    else:
                        break
            else:  # 这里就是保留关键起作用了
                while SegI < len(self.片段列表):
                    if self.片段列表[SegI][0] < 这一句的起始帧:
                        if self.片段列表[SegI][1] < 这一句的起始帧:
                            # 这个片段在 save 区间左侧，不管
                            SegI += 1
                        elif self.片段列表[SegI][1] <= 这一句的结束帧:
                            # 这个片段骑在本 save 区间左端了,把它右边截掉
                            self.片段列表[SegI][1] = 这一句的起始帧
                            SegI += 1
                        else:
                            # 这个片段整个盖信本 save 区间了,要截断,删掉中间一段
                            temp = self.片段列表[SegI]
                            temp[0] = 这一句的结束帧
                            self.片段列表[SegI][1] = 这一句的起始帧
                            self.片段列表.insert(SegI + 1, temp)
                            SegI += 1
                    elif self.片段列表[SegI][0] < 这一句的结束帧:
                        if self.片段列表[SegI][1] <= 这一句的结束帧:
                            del self.片段列表[SegI]
                        else:
                            self.片段列表[SegI][0] = 这一句的结束帧
                            SegI += 1
                    else:
                        break
        return 片段列表

    def 得到最大音量(self, 音频数据):
        maxv = float(np.max(音频数据))
        minv = float(np.min(音频数据))
        return max(maxv, -minv)


    def 音频变速(self, wav音频数据列表, 声道数, 采样率, 目标速度, 临时文件夹):
        if 目标速度 == 1.0:
            return wav音频数据列表
        if 查找可执行程序('soundstretch') != None:
            内存音频二进制缓存区 = io.BytesIO()
            fd, soundstretch临时输出文件 = tempfile.mkstemp()
            os.close(fd)
            wavfile.write(内存音频二进制缓存区, 采样率, wav音频数据列表)
            变速命令 = f'soundstretch stdin "{soundstretch临时输出文件}" -tempo={(目标速度 - 1) * 100}'
            变速线程 = subprocess.Popen(变速命令, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            变速线程.communicate(内存音频二进制缓存区.getvalue())
            try:
                采样率, 音频区间处理后的数据 = wavfile.read(soundstretch临时输出文件)
            except Exception as e:
                出错时间 = int(time.time())

                fd, 原始数据存放位置 = tempfile.mkstemp(dir=临时文件夹, prefix=f'原始-{出错时间}-', suffix='.wav')
                os.close(fd)
                wavfile.write(原始数据存放位置, 采样率, wav音频数据列表)

                fd, 出错文件 = tempfile.mkstemp(dir=临时文件夹, prefix=f'变速-{出错时间}-', suffix='.wav')
                os.close(fd)
                try:
                    copy(soundstretch临时输出文件, 出错文件)
                except:
                    ...

                fd, soundstretch临时输出文件 = tempfile.mkstemp(dir=临时文件夹, prefix=f'变速-{出错时间}-', suffix='.wav')
                os.close(fd)
                变速命令 = f'soundstretch stdin "{soundstretch临时输出文件}" -tempo={(目标速度 - 1) * 100}'
                变速线程 = subprocess.Popen(变速命令, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                变速线程.communicate(内存音频二进制缓存区.getvalue())

                self.print(f'Soundstretch 音频变速出错了，请前往查看详情\n    原始音频数据：{原始数据存放位置} \n    变速音频数据：{soundstretch临时输出文件}\n')
                self.print(f'出错的音频信息：\n    音频采样数：{len(wav音频数据列表)}\n    目标速度：{目标速度}\n    目标采样数：{len(wav音频数据列表) / 目标速度}\n')

                return wav音频数据列表

            os.remove(soundstretch临时输出文件)
        else:
            self.print(
                '检测到没有安装 SoundTouch 的 soundstretch，所以使用 phasevocoder 的音频变速方法。建议到 http://www.surina.net/soundtouch 下载系统对应的 soundstretch，放到系统环境变量下，可以获得更好的音频变速效果\n\n')
            sFile = io.BytesIO()
            wavfile.write(sFile, 采样率, wav音频数据列表)
            sFile = io.BytesIO(sFile.getvalue())
            eFile = io.BytesIO()
            with WavReader(sFile) as reader:
                with WavWriter(eFile, reader.channels, reader.samplerate) as writer:
                    tsm = phasevocoder(reader.channels, speed=目标速度)
                    tsm.run(reader, writer)
            _, 音频区间处理后的数据 = wavfile.read(io.BytesIO(eFile.getvalue()))

        return 音频区间处理后的数据

    def 处理音频(self, 音频文件, 片段列表, 视频帧率, 静音片段速度, 有声片段速度, 临时文件夹, concat记录文件路径):
        # 静音片段速度, 有声片段速度, 临时文件夹
        速度 = [静音片段速度, 有声片段速度]
        采样率, 总音频数据 = wavfile.read(音频文件, mmap=True)
        最大音量 = self.得到最大音量(总音频数据)
        if 最大音量 == 0:
            最大音量 = 1
        衔接前总音频片段末点 = 0  # 上一个帧为空
        concat记录文件 = open(concat记录文件路径, "w", encoding='utf-8')
        输出音频的数据 = np.zeros((0, 总音频数据.shape[1]))  # 返回一个数量为 0 的列表，数据类型为声音 shape[1]
        总片段数量 = len(片段列表)
        每帧采样数 = 采样率 / 视频帧率
        总输出采样数 = 0
        # for index, 片段 in enumerate(片段列表):
        #     print(片段)
        总帧数 = 0
        超出 = 0
        for index, 片段 in enumerate(片段列表):
            # print(f'总共有 {总片段数量} 个音频片段需处理, 现在在处理第 {index + 1} 个：{片段}\n')
            # 音频区间变速处理
            音频区间 = 总音频数据[int(片段[0] * 每帧采样数):int((片段[1]) * 每帧采样数)]
            音频区间处理后的数据 = self.音频变速(音频区间, 2, 采样率, 速度[int(片段[2])], 临时文件夹)
            处理后音频的采样数 = 音频区间处理后的数据.shape[0]
            理论采样数 = int(len(音频区间) / 速度[int(片段[2])])

            if 处理后音频的采样数 < 理论采样数:
                音频区间处理后的数据 = np.concatenate((音频区间处理后的数据, np.zeros((理论采样数 - 处理后音频的采样数, 2), dtype=np.int16)))
            elif 处理后音频的采样数 > 理论采样数:
                音频区间处理后的数据 = 音频区间处理后的数据[0:理论采样数]
            处理后又补齐的音频的采样数 = 音频区间处理后的数据.shape[0]
            总输出采样数 += 处理后又补齐的音频的采样数

            输出音频的数据 = np.concatenate((输出音频的数据, 音频区间处理后的数据 / 最大音量))  # 将刚才处理过后的小片段，添加到输出音频数据尾部
            衔接后总音频片段末点 = 衔接前总音频片段末点 + 处理后音频的采样数

            # 音频区间平滑处理
            音频过渡区块大小 = 400
            if 处理后音频的采样数 < 音频过渡区块大小:
                # 把 0 到 400 的数值都变成0 ，之后乘以音频就会让这小段音频静音。
                输出音频的数据[衔接前总音频片段末点:衔接后总音频片段末点] = 0  # audio is less than 0.01 sec, let's just remove it.
            else:
                # 音频大小渐变蒙板 = np.arange(音频过渡区块大小) / 音频过渡区块大小  # 1 - 400 的等差数列，分别除以 400，得到淡入时每个音频应乘以的系数。
                # 双声道音频大小渐变蒙板 = np.repeat(音频大小渐变蒙板[:, np.newaxis], 2, axis=1)  # 将这个数列乘以 2 ，变成2轴数列，就能用于双声道
                # 输出音频的数据[衔接前总音频片段末点 : 衔接前总音频片段末点 + 音频过渡区块大小] *= 双声道音频大小渐变蒙板  # 淡入
                # 输出音频的数据[衔接后总音频片段末点 - 音频过渡区块大小: 衔接后总音频片段末点] *= 1 - 双声道音频大小渐变蒙板  # 淡出
                pass
            衔接前总音频片段末点 = 衔接后总音频片段末点  # 将这次衔接后的末点作为下次衔接前的末点

            # 根据已衔接长度决定是否将已有总片段写入文件，再新建一个用于衔接的片段
            if len(输出音频的数据) >= 采样率 * 60 * 10 or (index + 1) == 总片段数量:
                tempWavClip = tempfile.mkstemp(dir=临时文件夹, prefix='AudioClipForNewVideo_', suffix='.wav')
                os.close(tempWavClip[0])
                wavfile.write(tempWavClip[1], 采样率, 输出音频的数据)
                concat记录文件.write("file " + Path(tempWavClip[1]).name + "\n")
                输出音频的数据 = np.zeros((0, 总音频数据.shape[1]))
        concat记录文件.close()
        self.print('子线程中的音频文件处理完毕，只待视频流输出完成了\n\n')
        return

    def 进行音频变速处理(self, 临时文件夹, 变速用的音频文件, 片段列表, 视频帧率, 静音速度, 有声速度):
        concat记录文件 = (Path(临时文件夹) / 'concat.txt').as_posix()
        音频处理线程 = threading.Thread(target=self.处理音频, args=[变速用的音频文件, 片段列表.copy(), 视频帧率, 静音速度, 有声速度, 临时文件夹, concat记录文件])
        音频处理线程.start()
        return 音频处理线程, concat记录文件

    def 计算总共帧数(self, 片段列表, 片段速度):
        总共帧数 = 0.0
        for 片段 in 片段列表:
            总共帧数 += (片段[1] - 片段[0]) / 片段速度[片段[2]]
        return int(总共帧数)

    def 秒数转时分秒(self, 秒数):
        秒数 = int(秒数)
        输出 = ''
        if 秒数 // 3600 > 0:
            输出 = f'{输出}{秒数 // 3600} 小时 '
            秒数 = 秒数 % 3600
        if 秒数 // 60 > 0:
            输出 = f'{输出}{秒数 // 60} 分 '
            秒数 = 秒数 % 60
        输出 = f'{输出}{秒数} 秒'
        return 输出

    def 生成临时srt字幕(self, 临时文件夹):
        临时srt路径 = (Path(临时文件夹) / 'Subtitle.srt').as_posix()
        subprocess.run(
            shlex.split(
                f'ffmpeg -i "{self.字幕文件}" "{临时srt路径}"'
            )
        )
        return 临时srt路径

    def ffmpeg和pyav综合处理视频流(self, 文件, 临时视频文件, 片段列表, 静音片段速度, 有声片段速度, 输出选项):
        开始时间 = time.time()
        片段速度 = [静音片段速度, 有声片段速度]

        input_ = av.open(文件)
        inputVideoStream = input_.streams.video[0]
        inputVideoStream.thread_type = 'AUTO'
        平均帧率 = float(inputVideoStream.average_rate)

        输入视频流查询命令 = f'ffprobe -of json -select_streams v -show_streams "{文件}"'
        输入视频流查询结果 = subprocess.run(shlex.split(输入视频流查询命令), capture_output=True, encoding='utf-8')
        输入视频流信息 = json.loads(输入视频流查询结果.stdout)

        height = 输入视频流信息['streams'][0]['height']
        width = 输入视频流信息['streams'][0]['width']
        pix_fmt = 输入视频流信息['streams'][0]['pix_fmt']
        if 'display_aspect_ratio' in 输入视频流信息['streams'][0]:
            输出视频比例选项 = ['-aspect', f'{输入视频流信息["streams"][0]["display_aspect_ratio"]}']
        else:
            输出视频比例选项 = []

        # 用 ffprobe 获得信息：
        # ffprobe -of json -select_streams v -show_entries stream=r_frame_rate "D:\Users\Haujet\Videos\2020-11-04 18-16-56.mkv"
        process2Command = ['ffmpeg', '-y',
                           '-f', 'rawvideo',
                           '-vcodec', 'rawvideo',
                           '-pix_fmt', pix_fmt,
                           '-s', f'{width}*{height}',
                           '-frame_size', f'{width}*{height}',
                           '-framerate', f'{平均帧率}',
                           '-i', '-',
                           '-s', f'{width}*{height}'] + 输出视频比例选项 + shlex.split(输出选项) + [临时视频文件]
        self.print(process2Command)
        self.print('\n\n')
        process2 = subprocess.Popen(process2Command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)

        帧率 = float(inputVideoStream.framerate)
        原始总帧数 = inputVideoStream.frames
        if 原始总帧数 == 0:
            原始总帧数 = int(得到输入视频时长(文件) * 平均帧率)
        总帧数 = self.计算总共帧数(片段列表, 片段速度)

        self.print(f'输出视频总帧数：{int(总帧数)}，输出后时长：{self.秒数转时分秒(int(总帧数 / 平均帧率))}')

        输入等效, 输出等效 = 0.0, 0.0
        片段 = 片段列表.pop(0)
        开始时间 = time.time()
        视频帧序号 = 0
        index = 0
        # input_.demux(VideoStream) 反回 [packet, packet, ......]
        # packet.decode() 反回 [frame, frame, ...]
        # frame.planes() 或 frame.planes 是一个列表，[plane, plane, ...]
        # plane.line_size 是它每一行多少字节
        # plane.width 是画面宽度，它小于等于 line_size
        for packet in input_.demux(inputVideoStream):
            for frame in packet.decode():
                # frame = frame.reformat() # 也不确定以前为什么要加这句，它是用于为帧重新设置分辩率、格式等的
                index += 1
                if len(片段列表) > 0 and index >= 片段[1]: 片段 = 片段列表.pop(0)
                输入等效 += (1 / 片段速度[片段[2]])
                while 输入等效 > 输出等效:
                    # 经过测试得知，在一些分辨率的视频中，例如一行虽然只有 2160 个像素，但是这一行的数据不止 2160 个，有可能是2176个，然后所有行的数据是连在一起的
                    # 在 python 里很难分离，只能使用 pyav 的 to_ndarray 再 tobytes
                    if frame.planes[0].width != frame.planes[0].line_size:
                        # in_bytes = frame.to_ndarray().tobytes()
                        # process2.stdin.write(in_bytes)
                        if frame.format.name in ('yuv420p', 'yuvj420p'):
                            # av.video.frame.useful_array(plane, bytes_per_pixel).to_bytes() 可以得到有效 plane
                            process2.stdin.write(av.video.frame.useful_array(frame.planes[0]).to_bytes())
                            process2.stdin.write(av.video.frame.useful_array(frame.planes[1]).to_bytes())
                            process2.stdin.write(av.video.frame.useful_array(frame.planes[2]).to_bytes())
                        elif frame.format.name == 'yuyv422':
                            process2.stdin.write(av.video.frame.useful_array(frame.planes[0], 2).to_bytes())
                        elif frame.format.name in ('rgb24', 'bgr24'):
                            process2.stdin.write(av.video.frame.useful_array(frame.planes[0], 3).to_bytes())
                        elif frame.format.name in ('argb', 'rgba', 'abgr', 'bgra'):
                            process2.stdin.write(av.video.frame.useful_array(frame.planes[0], 4).to_bytes())
                        elif frame.format.name in ('gray', 'gray8', 'rgb8', 'bgr8'):
                            process2.stdin.write(av.video.frame.useful_array(frame.planes[0]).to_bytes())
                        elif frame.format.name == 'pal8':
                            process2.stdin.write(av.video.frame.useful_array(frame.planes[0]).to_bytes())
                        else:
                            self.print(f'{frame.format.name} 像素格式不支持\n')
                    else:
                        if frame.format.name in ('yuv420p', 'yuvj420p'):
                            process2.stdin.write(frame.planes[0].to_bytes())
                            process2.stdin.write(frame.planes[1].to_bytes())
                            process2.stdin.write(frame.planes[2].to_bytes())
                        elif frame.format.name in (
                        'yuyv422', 'rgb24', 'bgr24', 'argb', 'rgba', 'abgr',
                        'bgra', 'gray', 'gray8', 'rgb8', 'bgr8','pal8'):
                            process2.stdin.write(frame.planes[0].to_bytes())
                        else:
                            self.print(f'{frame.format.name} 像素格式不支持\n')
                            return False

                    输出等效 += 1
                    if 输出等效 % 200 == 0:
                        self.printForFFmpeg(
                            f'帧速：{int(int(输出等效) / max(time.time() - 开始时间, 1))}, 剩余：{总帧数 - int(输出等效)} 帧，剩余时间：{self.秒数转时分秒(int((总帧数 - int(输出等效)) / max(1, int(输出等效) / max(time.time() - 开始时间, 1))))}    \n')
        process2.stdin.close()
        process2.wait()
        del process2
        input_.close()
        self.print(f'输出视频总帧数：{int(总帧数)}，输出后时长：{self.秒数转时分秒(int(总帧数 / 平均帧率))}\n')
        self.print(f'原来视频长度：{self.秒数转时分秒(原始总帧数 / 平均帧率)}，输出视频长度：{self.秒数转时分秒(int(输出等效) / 平均帧率)}\n')
        self.print(f'视频合成耗时：{self.秒数转时分秒(time.time() - 开始时间)}\n\n')
        return

    def 退出清理(self):
        ...

    def run(self):
        开始时间 = time.time()

        # 创建临时文件夹
        临时文件夹 = self.创建临时文件夹()
        if not 临时文件夹: return False
        
        self.获取音视频流信息()
        self.检查输入文件是否只含音频()
        
        视频帧率 = self.得到输入视频帧率()
        if not 视频帧率: return False
        
        音频采样率 = self.得到输入音频采样率()
        if not 音频采样率: return False

        分析用的音频文件 = (Path(临时文件夹) / 'OriginalAudio.wav').as_posix()
        变速用的音频文件 = (Path(临时文件夹) / 'OriginalAudio.wav').as_posix()
        
        self.提取音频流(self.输入文件, 变速用的音频文件, 音频采样率)

        片段列表 = self.由音频得到片段列表(音频文件=分析用的音频文件, 
                              视频帧率=视频帧率, 
                              声音检测相对阈值=self.静音阈值, 
                              片段间缓冲帧数=self.片段间缓冲帧数)

        if self.使用辅助字幕:
            srt字幕 = self.生成临时srt字幕(临时文件夹)
            self.使用字幕进一步处理片段列表(srt字幕)

        音频处理线程, concat记录文件 = self.进行音频变速处理(
            临时文件夹,
            变速用的音频文件,
            片段列表,
            视频帧率,
            self.静音片段倍速,
            self.响亮片段倍速
        )

        if not self.只处理音频:
            临时视频文件 = (Path(临时文件夹) / 'Video.mp4').as_posix()
            try:
                self.ffmpeg和pyav综合处理视频流(self.输入文件, 临时视频文件, 片段列表, self.静音片段倍速, self.响亮片段倍速, self.输出选项)
            except Exception as e:
                print(e)
                self.print('\n视频部分处理出错，任务停止\n')
                return False
        音频处理线程.join()

        # 合并音视频
        self.print(f'现在开始合并\n\n')
        if self.只处理音频:
            command = f'ffmpeg -y -hide_banner -safe 0  -f concat -i "{concat记录文件}" -i "{self.输入文件}" -c:v copy -map_metadata 1 -map_metadata:s:a 1:s:a -map 0:a "{self.输出文件}"'
        else:
            command = f'ffmpeg -y -hide_banner -i "{临时视频文件}" -safe 0 -f concat -i "{concat记录文件}" -i "{self.输入文件}" -c:v copy -map_metadata 2 -map_metadata:s:a 2:s:a:0 -map_metadata:s:v:0 2:s:v -map 0:v -map 1:a  "{self.输出文件}"'
        subprocess.run(shlex.split(command), encoding='utf-8', stderr=subprocess.PIPE)

        # 删除临时文件
        try:
            self.print('删除临时文件\n\n')
            rmtree(临时文件夹)
        except Exception as e:
            self.print(f'删除临时文件夹失败，可能是被占用导致，请手动删除：\n    {临时文件夹}\n\n')

        # 打开文件路径
        os.startfile(Path(self.输出文件).parent)
        # os.system(f'explorer /select, "{Path(self.输出文件)}')

        self.print(f'任务完成，总共耗时：{self.秒数转时分秒(time.time() - 开始时间)}\n\n')
        return

