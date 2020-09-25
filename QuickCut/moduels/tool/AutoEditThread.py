# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from moduels.component.NormalValue import 常量

import subprocess, os, re, math, cv2, time
import numpy as np
from shutil import rmtree, move
from scipy.io import wavfile
from audiotsm.io.wav import WavReader, WavWriter
from audiotsm import phasevocoder

# 自动剪辑
class AutoEditThread(QThread):
    signal = Signal(str)
    signalForFFmpeg = Signal(str)

    output = None  # 用于显示输出的控件，如一个 QEditBox，它需要有自定义的 print 方法。

    inputFile = ''
    outputFile = ''
    silentSpeed = 1
    soundedSpeed = 2
    frameMargin = 3
    silentThreshold = 0.025
    extractFrameOption = '-c:v mjpeg -qscale:v 3'
    ffmpegOutputOption = ''
    whetherToUseOnlineSubtitleKeywordAutoCut = False
    apiEngine = ''
    cutKeyword = ''
    saveKeyword = ''

    TEMP_FOLDER = 'TEMP'

    def __init__(self, parent=None):
        super(AutoEditThread, self).__init__(parent)

    def print(self, text):
        self.signal.emit(text)

    def printForFFmpeg(self, text):
        self.signalForFFmpeg.emit(text)

    def createPath(self, s):
        assert (not os.path.exists(s)), "临时文件输出路径：" + s + " 已存在，任务取消"
        try:
            os.mkdir(s)
        except OSError:
            assert False, "创建临时文件夹失败，可能是已存在临时文件夹或者权限不足"

    def deletePath(self, s):  # 极度危险的函数，小心使用！
        try:
            rmtree(s, ignore_errors=False)
        except OSError:
            self.print(self.tr('删除临时文件夹 %s 失败') % s)
            print(OSError)
            return False

    def removeTempFolder(self):
        if (os.path.exists(self.TEMP_FOLDER)):
            self.print(self.tr('正在清除产生的临时文件夹：%s\n') % self.TEMP_FOLDER)
            self.deletePath(self.TEMP_FOLDER)

    def getMaxVolume(self, s):
        maxv = float(np.max(s))
        minv = float(np.min(s))
        return max(maxv, -minv)

    # 复制文件，返回一个保存成功的信息(每50帧提示一次)
    def moveFrame(self, 输入帧, outputFrame):
        src = self.TEMP_FOLDER + "/frame{:06d}".format(输入帧 + 1) + ".jpg"
        dst = self.TEMP_FOLDER + "/newFrame{:06d}".format(outputFrame + 1) + ".jpg"
        if not os.path.isfile(str(src)):
            return False
        if outputFrame % 20 == 19:
            self.print(str(outputFrame + 1) + "  ")
        move(src, dst)
        return True

    def run(self):
        # 定义剪切、保留片段的关键词
        # try:
        key_word = [self.cutKeyword, self.saveKeyword]

        NEW_SPEED = [self.silentSpeed, self.soundedSpeed]

        # 音频淡入淡出大小，使声音在不同片段之间平滑
        AUDIO_FADE_ENVELOPE_SIZE = 400  # smooth out transitiion's audio by quickly fading in/out (arbitrary magic number whatever)

        self.TEMP_FOLDER = os.path.splitext(self.inputFile)[0] + '_TEMP'
        self.print(self.tr('临时文件目录：%s \n') % self.TEMP_FOLDER)

        # 如果临时文件已经存在，就删掉
        删除缓存文件结果 = self.removeTempFolder()
        if 删除缓存文件结果 == False:
            self.print('检测到临时文件夹存在，但无法删除，停止自动剪辑\n')
            self.print('请手动检查删除该目录：%s\n' % self.TEMP_FOLDER)
            return

        # 创建临时文件夹
        self.print(self.tr('新建临时文件夹：%s \n') % self.TEMP_FOLDER)
        try:
            self.createPath(self.TEMP_FOLDER)
        except:
            self.print(self.tr('临时文件夹（%s）创建失败，自动剪辑停止，请检查权限\n') % self.TEMP_FOLDER)
            return


        # 如果要用在线转字幕
        if self.whetherToUseOnlineSubtitleKeywordAutoCut:

            ########改用主数据库
            try:
                newConn = sqlite3.connect(常量.dbname)

                ossData = newConn.cursor().execute(
                    '''select provider, bucketName, endPoint, accessKeyId,  accessKeySecret from %s ;''' % (
                        ossTableName)).fetchone()

                ossProvider, ossBucketName, ossEndPoint, ossAccessKeyId, ossAccessKeySecret = ossData[0], ossData[1], \
                                                                                              ossData[2], ossData[3], \
                                                                                              ossData[4]
                if ossProvider == 'Alibaba':
                    oss = AliOss()
                    oss.auth(ossBucketName, ossEndPoint, ossAccessKeyId, ossAccessKeySecret)
                elif ossProvider == 'Tencent':
                    oss = TencentOss()
                    oss.auth(ossBucketName, ossEndPoint, ossAccessKeyId, ossAccessKeySecret)

                apiData = newConn.cursor().execute(
                    '''select provider, appKey, language, accessKeyId, accessKeySecret from %s where name = '%s';''' % (
                        apiTableName, self.apiEngine)).fetchone()

                apiProvider, apiappKey, apiLanguage, apiAccessKeyId, apiAccessKeySecret = apiData[0].replace('\n', ''), apiData[1].replace('\n', ''), apiData[
                    2].replace('\n', ''), apiData[3].replace('\n', ''), apiData[4].replace('\n', '')

                if apiProvider == 'Alibaba':
                    transEngine = AliTrans()
                elif apiProvider == 'Tencent':
                    transEngine = TencentTrans()

                transEngine.setupApi(apiappKey, apiLanguage, apiAccessKeyId, apiAccessKeySecret)

                srtSubtitleFile = transEngine.mediaToSrt(self.output, oss, self.inputFile)
            except:
                self.print(self.tr('\n转字幕出问题了，有可能是 oss 填写错误，或者语音引擎出错误，总之，请检查你的 api 和 KeyAccess 的权限\n'))
                return
            newConn.close()

        # 运行一下 ffmpeg，将输入文件的音视频信息写入文件
        with open(self.TEMP_FOLDER + "/params.txt", "w") as f:
            command = 'ffmpeg -hide_banner -i "%s"' % (self.inputFile)
            subprocess.call(command, shell=True, stderr=f)

        # 读取一下 params.txt ，找一下 fps 数值到 视频帧率
        with open(self.TEMP_FOLDER + "/params.txt", 'r+', encoding='utf-8') as f:
            pre_params = f.read()
        params = pre_params.split('\n')
        for line in params:
            m = re.search(r'Stream #.*Video.* ([0-9\.]*) fps', line)
            if m is not None:
                视频帧率 = float(m.group(1))
        for line in params:
            m = re.search('Stream #.*Audio.* ([0-9]*) Hz', line)
            if m is not None:
                采样率 = int(m.group(1))
        self.print(self.tr('视频帧率是: ') + str(视频帧率) + '\n')
        self.print(self.tr('音频采样率是: ') + str(采样率) + '\n')

        command = 'ffmpeg -hide_banner -i "%s" -ab 160k -ac 2 -ar %s -vn "%s/audio.wav"' % (
            self.inputFile, 采样率, self.TEMP_FOLDER)
        self.print(self.tr('\n开始提取音频流：%s\n') % command)
        if 常量.platfm == 'Windows':
            self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                            universal_newlines=True, encoding='utf-8',
                                            startupinfo=常量.subprocessStartUpInfo)
        else:
            self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                            universal_newlines=True, encoding='utf-8')
        for line in self.process.stdout:
            self.printForFFmpeg(line)

        # 变量 音频采样率, 总音频数据 ，得到采样总数为 wavfile.read("audio.wav").shape[0] ，（shape[1] 是声道数）
        音频采样率, 总音频数据 = wavfile.read(self.TEMP_FOLDER + "/audio.wav")
        总音频采样数 = 总音频数据.shape[0]
        最大音量 = self.getMaxVolume(总音频数据)
        每帧采样数 = 音频采样率 / 视频帧率
        总音频帧数 = int(math.ceil(总音频采样数 / 每帧采样数))
        hasLoudAudio = np.zeros((总音频帧数))

        # 这里给每一帧音频标记上是否超过阈值
        self.print(self.tr('\n正在分析每一帧音频是否超过阈值\n'))
        for i in range(总音频帧数):
            该帧音频起始 = int(i * 每帧采样数)
            该帧音频结束 = min(int((i + 1) * 每帧采样数), 总音频采样数)
            单帧音频区间 = 总音频数据[该帧音频起始:该帧音频结束]
            单帧音频最大相对音量 = float(self.getMaxVolume(单帧音频区间)) / 最大音量
            if 单帧音频最大相对音量 >= self.silentThreshold:
                hasLoudAudio[i] = 1

        # 这里得到一个个判断为静音或有音的片段
        self.print(self.tr('\n正在按声音阈值划分片段\n'))
        片段列表 = [[0, 0, 0]]
        shouldIncludeFrame = np.zeros((总音频帧数)) # 返回一个数量为 音频总帧数 的列表，默认数值为0，用于存储是否该存储这一帧
        for i in range(总音频帧数):
            start = int(max(0, i - self.frameMargin))
            end = int(min(总音频帧数, i + 1 + self.frameMargin))
            # 如果从加上淡入淡出的起始到最后之间的几帧中，有1帧是要保留的，那就保留这一区间所有的
            shouldIncludeFrame[i] = np.max(hasLoudAudio[start:end])
            # 如果这一帧不是总数第一帧 且 是否保留这一帧 与 前一帧 不同
            if (i >= 1 and shouldIncludeFrame[i] != shouldIncludeFrame[i - 1]):  # Did we flip?
                片段列表.append([片段列表[-1][1], i, int(shouldIncludeFrame[i - 1])])
        片段列表.append([片段列表[-1][1], 总音频帧数, int(shouldIncludeFrame[i - 1])])# 加一个最后那几帧要不要保留
        片段列表 = 片段列表[1:] # 把片段列表中开头那个开始用于占位的 [0,0,0]去掉
        self.print(self.tr('\n静音、响亮片段分析完成\n'))

        # 根据字幕进一步处理片段
        if self.whetherToUseOnlineSubtitleKeywordAutoCut:
            self.print(self.tr('\n开始根据字幕中的关键词二次处理片段\n'))
            try:
                subtitleFile = open(srtSubtitleFile, "r", encoding='utf-8')
                subtitleContent = subtitleFile.read()
                subtitleLists = list(srt.parse(subtitleContent))
                subtitleKeywordLists = []
                for i in subtitleLists:
                    if re.match('(%s)|(%s)$' % (key_word[0], key_word[1]), i.content):
                        subtitleKeywordLists.append(i)
                lastEnd = 0
                # this q means the index of the 片段列表
                q = 2
                for i in range(len(subtitleKeywordLists)):
                    q -= 2
                    self.print(str(subtitleKeywordLists[i]))
                    if i > 0:
                        lastEnd = int((subtitleKeywordLists[i - 1].end.seconds + subtitleKeywordLists[
                            i - 1].end.microseconds / 1000000) * 视频帧率) + 10
                    thisStart = int((subtitleKeywordLists[i].start.seconds + subtitleKeywordLists[
                        i].start.microseconds / 1000000) * 视频帧率) - 4
                    thisEnd = int((subtitleKeywordLists[i].end.seconds + subtitleKeywordLists[
                        i].end.microseconds / 1000000) * 视频帧率) + 10
                    self.print(self.tr('上一区间的结尾是: %s \n') % str(lastEnd))
                    self.print(self.tr('这是区间是: %s 到 %s \n') % (str(thisStart), str(thisEnd)))

                    # note that the key_word[0] is cut keyword
                    if re.match('(%s)' % (key_word[0]), subtitleKeywordLists[i].content):

                        while q < len(片段列表):
                            self.print(str(片段列表[q]))
                            if 片段列表[q][1] <= lastEnd:
                                self.print(self.tr('这个 chunk (%s 到 %s) 在 cut 区间  %s 到 %s  左侧，下一个 chunk') % (
                                    片段列表[q][0], 片段列表[q][1], thisStart, thisEnd))
                                q += 1
                                continue
                            elif 片段列表[q][0] >= thisEnd:
                                self.print(self.tr('这个 chunk (%s 到 %s) 在 cut 区间  %s 到 %s  右侧，下一个区间') % (
                                    片段列表[q][0], 片段列表[q][1], thisStart, thisEnd))
                                q += 1
                                break
                            elif 片段列表[q][1] <= thisEnd:
                                self.print(str(片段列表[q][1]) + " < " + str(thisEnd))
                                self.print(self.tr('这个chunk 的右侧 %s 小于区间的终点  %s ，删掉') % (片段列表[q][1], thisEnd))
                                del 片段列表[q]
                            elif 片段列表[q][1] > thisEnd:
                                self.print(self.tr('这个chunk 的右侧 %s 大于区间的终点 %s ，把它的左侧 %s 改成本区间的终点 %s ') % (
                                    片段列表[q][1], thisEnd, 片段列表[q][0], thisEnd))
                                片段列表[q][0] = thisEnd
                                q += 1
                    # key_word[1] is save keyword
                    elif re.match('(%s)' % (key_word[1]), subtitleKeywordLists[i].content):
                        while q < len(片段列表):
                            self.print(str(片段列表[q]))
                            if 片段列表[q][1] <= thisStart:
                                self.print(
                                    "这个区间 (%s 到 %s) 在起点 %s 左侧，放过，下一个 chunk" % (片段列表[q][0], 片段列表[q][1], thisStart))
                                q += 1
                                continue
                            elif 片段列表[q][0] >= thisEnd:
                                self.print(self.tr('这个 chunk (%s 到 %s) 在 cut 区间  %s 到 %s  右侧，下一个区间') % (
                                    片段列表[q][0], 片段列表[q][1], thisStart, thisEnd))
                                q += 1
                                break
                            elif 片段列表[q][1] > thisStart and 片段列表[q][0] <= thisStart:
                                self.print(self.tr('这个区间 (%s 到 %s) 的右侧，在起点 %s 和终点 %s 之间，修改区间右侧为 %s ') % (
                                    片段列表[q][0], 片段列表[q][1], thisStart, thisEnd, thisStart))
                                片段列表[q][1] = thisStart
                                q += 1
                            elif 片段列表[q][0] >= thisStart and 片段列表[q][1] > thisEnd:
                                self.print(self.tr('这个区间 (%s 到 %s) 的左侧，在起点 %s 和终点 %s 之间，修改区间左侧为 %s ') % (
                                    片段列表[q][0], 片段列表[q][1], thisStart, thisEnd, thisEnd))
                                片段列表[q][0] = thisEnd
                                q += 1
                            elif 片段列表[q][0] >= thisStart and 片段列表[q][1] <= thisEnd:
                                self.print(self.tr('这个区间 (%s 到 %s) 整个在起点 %s 和终点 %s 之间，删除 ') % (
                                    片段列表[q][0], 片段列表[q][1], thisStart, thisEnd))
                                del 片段列表[q]
                            elif 片段列表[q][0] < thisStart and 片段列表[q][1] > thisEnd:
                                self.print(self.tr('这个区间 (%s 到 %s) 横跨了 %s 到 %s ，分成两个：从 %s 到 %s ，从 %s 到 %s  ') % (
                                    片段列表[q][0], 片段列表[q][1], thisStart, thisEnd, 片段列表[q][0], thisStart, thisEnd,
                                    片段列表[q][1]))
                                temp = 片段列表[q]
                                temp[0] = thisEnd
                                片段列表[q][1] = thisStart
                                片段列表.insert(q + 1, temp)
                                q += 1
            except:
                self.print(self.tr('自动剪辑过程出错了，可能是因为启用了在线语音识别引擎，但是填写的 oss 和 api 有误，如果是其它原因，你可以将问题出现过程记录下，在帮助页面加入 QQ 群向作者反馈。'))

        # 打印片段列表
        self.print(self.tr('\n得到最终分段信息如下：\n'))
        最终分段信息 = ""
        for i in range(len(片段列表)):
            最终分段信息 += str(片段列表[i]) + '  '
        self.print(最终分段信息)


        self.print(self.tr('\n\n开始根据分段信息处理音频\n'))
        lastExistingFrame = 0 # 上一个帧为空
        i = 0
        concat = open(self.TEMP_FOLDER + "/concat.txt", "a")
        输出音频的数据 = np.zeros((0, 总音频数据.shape[1])) # 返回一个数量为 0 的列表，数据类型为声音 shape[1]
        总片段数量 = len(片段列表)
        衔接前总音频片段末点 = 0
        for 片段 in 片段列表:
            i += 1
            # 音频区间变速处理
            音频区间 = 总音频数据[int(片段[0] * 每帧采样数):int(片段[1] * 每帧采样数)] # 得到一块音频区间
            音频区间处理前保存位置 = self.TEMP_FOLDER + "/音频区间处理前临时保存文件.wav"
            音频区间处理后保存位置 = self.TEMP_FOLDER + "/音频区间处理后临时保存文件.wav"
            wavfile.write(音频区间处理前保存位置, 采样率, 音频区间) # 将得到的音频区间写入到 音频区间处理前保存位置(startFile)
            with WavReader(音频区间处理前保存位置) as reader:
                with WavWriter(音频区间处理后保存位置, reader.channels, reader.samplerate) as writer:
                    tsm = phasevocoder(reader.channels, speed=NEW_SPEED[int(片段[2])]) # 给音频区间设定变速 time-scale modification
                    tsm.run(reader, writer) # 按照指定参数，生成新速度的音频，写入音频区间处理后保存位置
            _, 音频区间处理后的数据 = wavfile.read(音频区间处理后保存位置) # 读取 endFile ，赋予 改变后的数据
            处理后音频的采样数 = 音频区间处理后的数据.shape[0]
            
            # 输出音频数据接上 改变后的数据/最大音量
            输出音频的数据 = np.concatenate((输出音频的数据, 音频区间处理后的数据 / 最大音量)) # 将刚才处理过后的小片段，添加到输出音频数据尾部
            衔接后总音频片段末点 = 衔接前总音频片段末点 + 处理后音频的采样数

            # 音频区间平滑处理
            if 处理后音频的采样数 < AUDIO_FADE_ENVELOPE_SIZE:
                # 把 0 到 400 的数值都变成0 ，之后乘以音频就会让这小段音频静音。
                输出音频的数据[衔接前总音频片段末点:衔接后总音频片段末点] = 0  # audio is less than 0.01 sec, let's just remove it.
            else:
                # 音频大小渐变蒙板 = np.arange(AUDIO_FADE_ENVELOPE_SIZE) / AUDIO_FADE_ENVELOPE_SIZE  # 1 - 400 的等差数列，分别除以 400，得到淡入时每个音频应乘以的系数。
                # 双声道音频大小渐变蒙板 = np.repeat(音频大小渐变蒙板[:, np.newaxis], 2, axis=1)  # 将这个数列乘以 2 ，变成2轴数列，就能用于双声道
                # 输出音频的数据[衔接前总音频片段末点 : 衔接前总音频片段末点 + AUDIO_FADE_ENVELOPE_SIZE] *= 双声道音频大小渐变蒙板  # 淡入
                # 输出音频的数据[衔接后总音频片段末点 - AUDIO_FADE_ENVELOPE_SIZE: 衔接后总音频片段末点] *= 1 - 双声道音频大小渐变蒙板  # 淡出
                pass

            衔接前总音频片段末点 = 衔接后总音频片段末点 # 将这次衔接后的末点作为下次衔接前的末点

            # 根据已衔接长度决定是否将已有总片段写入文件，再新建一个用于衔接的片段
            # print('本音频片段已累计时长：%ss' % str(len(输出音频的数据) / 采样率) )
            if len(输出音频的数据) >= 采样率 * 60 * 10 or i == 总片段数量:
                wavfile.write(self.TEMP_FOLDER + '/AudioClipForNewVideo_' + '%06d' % i + '.wav', 采样率, 输出音频的数据)
                concat.write("file " + "AudioClipForNewVideo_" + "%06d" % i + ".wav\n")
                输出音频的数据 = np.zeros((0, 总音频数据.shape[1]))
        concat.close()

        self.print(self.tr('\n\n开始根据分段信息处理视频\n'))
        原始图像捕获器 = cv2.VideoCapture(self.inputFile)
        原始视频宽度 = int(原始图像捕获器.get(cv2.CAP_PROP_FRAME_WIDTH))
        原始视频高度 = int(原始图像捕获器.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        输出 = cv2.VideoWriter(f'{self.TEMP_FOLDER}/FinalVideo.mp4', fourcc, 视频帧率, (原始视频宽度, 原始视频高度))
        总帧数 = 片段列表[len(片段列表) - 1][1]
        开始时间 = time.time()
        remander = 0
        视频帧已写入 = 0
        while 原始图像捕获器.isOpened():
            ret, 原始图像帧 = 原始图像捕获器.read()
            if (not ret):
                break
            当前图像帧数 = int(原始图像捕获器.get(cv2.CAP_PROP_POS_FRAMES))  # current frame
            state = None
            for 片段 in 片段列表:
                if (当前图像帧数 >= 片段[0] and 当前图像帧数 <= 片段[1]):
                    state = 片段[2]
                    break
            if (state is not None):
                mySpeed = NEW_SPEED[state]

                if (mySpeed != 99999):
                    doIt = (1 / mySpeed) + remander
                    for __ in range(int(doIt)):
                        输出.write(原始图像帧)
                        视频帧已写入 += 1
                    remander = doIt % 1
            self.printForFFmpeg('当前图像帧数：%s, 总帧数：%s, 速度：%sfps \n' % (当前图像帧数, 总帧数, int(当前图像帧数 / (time.time() - 开始时间))) )
        原始图像捕获器.release()
        输出.release()
        cv2.destroyAllWindows()
        # 可以参考 https://github.com/yati-sagade/aveta 进行优化



        self.print(self.tr('\n\n现在开始合并音频片段\n'))
        command = 'ffmpeg -y -hide_banner -safe 0 -f concat -i "%s/concat.txt" -framerate %s "%s/FinalAudio.wav"' % (self.TEMP_FOLDER, 视频帧率, self.TEMP_FOLDER)
        if 常量.platfm == 'Windows':
            self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True, encoding='utf-8',startupinfo=常量.subprocessStartUpInfo)
        else:
            self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True, encoding='utf-8')
        for line in self.process.stdout:
            self.printForFFmpeg(line)

        self.print(self.tr('\n音频片段合成完毕，开始合并音视频\n'))
        command = 'ffmpeg -y -hide_banner  -i "%s/FinalVideo.mp4" -i "%s/FinalAudio.wav"  %s "%s"' % (self.TEMP_FOLDER, self.TEMP_FOLDER, self.ffmpegOutputOption, self.outputFile)
        if 常量.platfm == 'Windows':
            self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                        universal_newlines=True, encoding='utf-8', startupinfo=常量.subprocessStartUpInfo)
        else:
            self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                            universal_newlines=True, encoding='utf-8')
        for line in self.process.stdout:
            self.printForFFmpeg(line)
        self.print(self.tr('\n音视频合并完成！\n'))

        # if args.online_subtitle:
        #     # 生成新视频文件后，生成新文件的字幕
        #
        #     # 可以考虑先删除在线生成的原始字幕
        #     # os.remove(input_subtitle)
        #     if re.match('Alibaba', args.cloud_engine):
        #         print('使用引擎是 Alibaba')
        #         aliTrans.auth()
        #         aliTrans.mediaToSrt(OUTPUT_FILE, args.subtitle_language, args.delete_cloud_file)
        #     elif re.match('Tencent', args.cloud_engine):
        #         print('使用引擎是 Tencent')
        #         tenTrans.mediaToSrt(OUTPUT_FILE, args.subtitle_language, args.delete_cloud_file)

        # 删除临时文件夹
        self.print(self.tr('\n现在删除临时文件夹\n'))
        self.deletePath(self.TEMP_FOLDER)


        self.print(self.tr('\n自动剪辑所有步骤完成！\n'))
        # except:
        #     self.print(self.tr('自动剪辑过程出错了，可能是因为启用了在线语音识别引擎，但是填写的 oss 和 api 有误，如果是其它原因，你可以将问题出现过程记录下，在帮助页面加入 QQ 群向作者反馈。'))
