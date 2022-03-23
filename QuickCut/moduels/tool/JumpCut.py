# -*- coding: UTF-8 -*-

#coding=utf-8

# JumpCutter2
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021 Haujet Zhao

import av
import io
import math
import os
import platform
import re
import json
import subprocess
import sys
import tempfile
import threading
import time
import shlex
from shutil import rmtree, copy
from pathlib import Path
from pprint import pprint
from moduels.component.NormalValue import 常量

import numpy as np
from audiotsm import phasevocoder
from audiotsm.io.wav import WavReader, WavWriter
from scipy.io import wavfile


os.environ['PATH'] += os.pathsep + os.path.abspath('./bin/Windows')  # 将可执行文件的目录加入环境变量
os.environ['PATH'] += os.pathsep + os.path.abspath('./bin/MacOS')  # 将可执行文件的目录加入环境变量

def 提取音频流(输入文件, 输出文件, 音频采样率):
    command = f'ffmpeg -hide_banner -i "{输入文件}" -ac 2 -ar {音频采样率} -vn "{输出文件}"'
    进程 = subprocess.run(command,
                    shell=True,
                    stderr=subprocess.PIPE,
                    startupinfo=常量.subprocessStartUpInfo)
    del 进程
    return

def 得到最大音量(音频数据):
    maxv = float(np.max(音频数据))
    minv = float(np.min(音频数据))
    return max(maxv, -minv)

def 由音频得到片段列表(音频文件, 视频帧率, 声音检测相对阈值, 片段间缓冲帧数):
    # 变量 音频采样率, 总音频数据 ，得到采样总数为 wavfile.read("audio.wav").shape[0] ，（shape[1] 是声道数）
    采样率, 总音频数据 = wavfile.read(音频文件, mmap=True)
    总音频采样数 = 总音频数据.shape[0]

    最大音量 = 得到最大音量(总音频数据)
    if 最大音量 == 0: 最大音量 = 1
    每帧采样数 = 采样率 / 视频帧率
    总音频帧数 = int(math.ceil(总音频采样数 / 每帧采样数))
    hasLoudAudio = np.zeros((总音频帧数))

    # 这里给每一帧音频标记上是否超过阈值
    for i in range(总音频帧数):
        该帧音频起始 = int(i * 每帧采样数)
        该帧音频结束 = min(int((i + 1) * 每帧采样数), 总音频采样数)
        单帧音频区间 = 总音频数据[该帧音频起始:该帧音频结束]
        单帧音频最大相对音量 = float(得到最大音量(单帧音频区间)) / 最大音量
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
    print(f'静音、响亮片段分析完成')
    return 片段列表

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

# @profile()
def 由spleeter得到辅助音频数据(音频文件, 分轨器, 临时文件夹):
    print('正在使用 spleeter 分离音轨')

    分轨器.separate_to_file(音频文件, Path(临时文件夹))
    采样率, 音频数据 = wavfile.read(Path(临时文件夹)/Path(音频文件).stem/'vocals.wav')

    rmtree((Path(临时文件夹)/Path(音频文件).stem))
    return 采样率, 音频数据

def 音频片段合并(片段列表:list, 输出文件:str):
    # 建立一个临时TXT文件，用于CONCAT记录
    concat文件夹 = (Path(片段列表[0]).parent).as_posix()
    fd, concat文件 = tempfile.mkstemp(dir=concat文件夹, prefix='音频文件concat记录-', suffix='.txt')
    os.close(fd)

    # 将音频片段的名字写入CONCAT文件
    with open(concat文件, 'w', encoding='utf-8') as f:
        for 片段路径 in 片段列表:
            f.write(f'file {Path(片段路径).name}\n')

    # FFMPEG连接音频片段
    command = f'ffmpeg -y -hide_banner -safe 0  -f concat -i "{concat文件}" -c:a copy "{输出文件}"'
    # print(command)
    进程 = subprocess.run(shlex.split(command),
                        shell=True,
                        encoding='utf-8',
                        cwd=concat文件夹,
                        stderr=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL,
                        startupinfo=常量.subprocessStartUpInfo)
    del 进程
    return


def 音频变速(wav音频数据列表, 声道数, 采样率, 目标速度, 临时文件夹):
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

            print(f'Soundstretch 音频变速出错了，请前往查看详情\n    原始音频数据：{原始数据存放位置} \n    变速音频数据：{soundstretch临时输出文件}\n')
            print(f'出错的音频信息：\n    音频采样数：{len(wav音频数据列表)}\n    目标速度：{目标速度}\n    目标采样数：{len(wav音频数据列表) / 目标速度}')

            return wav音频数据列表

        os.remove(soundstretch临时输出文件)
    else:
        print(
            '检测到没有安装 SoundTouch 的 soundstretch，所以使用 phasevocoder 的音频变速方法。建议到 http://www.surina.net/soundtouch 下载系统对应的 soundstretch，放到系统环境变量下，可以获得更好的音频变速效果\n')
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

def 处理音频(音频文件, 片段列表, 视频帧率, 静音片段速度, 有声片段速度, 临时文件夹, concat记录文件路径):
    # 静音片段速度, 有声片段速度, 临时文件夹
    print(f'在子线程开始根据分段信息处理音频')
    速度 = [静音片段速度, 有声片段速度]
    采样率, 总音频数据 = wavfile.read(音频文件, mmap=True)
    最大音量 = 得到最大音量(总音频数据)
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
        音频区间处理后的数据 = 音频变速(音频区间, 2, 采样率, 速度[int(片段[2])], 临时文件夹)
        处理后音频的采样数 = 音频区间处理后的数据.shape[0]
        理论采样数 = int(len(音频区间) / 速度[int(片段[2])])

        # 理想长度 = len(音频区间) / 速度[int(片段[2])]
        # 现实长度 = len(音频区间处理后的数据)
        # 原始帧数 = len(音频区间) / 每帧采样数
        # 理想帧数 = 理想长度 / 每帧采样数
        # 现实帧数 = 现实长度 / 每帧采样数
        # 总帧数 += 现实帧数
        # print(f'这个区间速度为：{速度[int(片段[2])]}\n它的长度为：   {len(音频区间)}\n理想化转换后，长度应为：{理想长度}\n实际长度为：{现实长度}')
        # print(f'这个音频区间速度为：{速度[int(片段[2])]}\n它的长度为：   {原始帧数}\n理想化转换后，长度应为：{理想帧数}\n实际长度为：{现实帧数}\n已写入：{总帧数}')

        if 处理后音频的采样数 < 理论采样数:
            音频区间处理后的数据 = np.concatenate((音频区间处理后的数据, np.zeros((理论采样数 - 处理后音频的采样数, 2), dtype=np.int16)))
        elif 处理后音频的采样数 > 理论采样数:
            音频区间处理后的数据 = 音频区间处理后的数据[0:理论采样数]
            # print(f'片段音频采样数超出：{处理后音频的采样数 - 理论采样数}  此片段速度是：{速度[int(片段[2])]}  它的原长度是：{len(音频区间)}  它的现长度是：{处理后音频的采样数}')
            # 超出 += (处理后音频的采样数 - 理论采样数)
        处理后又补齐的音频的采样数 = 音频区间处理后的数据.shape[0]
        总输出采样数 += 处理后又补齐的音频的采样数

        # self.print('每帧采样数: %s   理论后采样数: %s  处理后采样数: %s  实际转换又补齐后后采样数: %s， 现在总采样数:%s  , 现在总音频时间: %s \n' % (int(self.每帧采样数), 理论采样数, 处理后音频的采样数, 处理后又补齐的音频的采样数, 总输出采样数, 总输出采样数 / (self.视频帧率 * 每帧采样数)  ))
        # 输出音频数据接上 改变后的数据/self.最大音量
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
        # print('本音频片段已累计时长：%ss' % str(len(输出音频的数据) / 采样率) )
        # print('输出音频加的帧数: %s' % str(处理后又补齐的音频的采样数 / 每帧采样数) )
        # print(f'\n\nindex: {index}; 总：{总片段数量}\n\n')
        if len(输出音频的数据) >= 采样率 * 60 * 10 or (index + 1) == 总片段数量:
            tempWavClip = tempfile.mkstemp(dir=临时文件夹, prefix='AudioClipForNewVideo_', suffix='.wav')
            os.close(tempWavClip[0])
            wavfile.write(tempWavClip[1], 采样率, 输出音频的数据)
            concat记录文件.write("file " + Path(tempWavClip[1]).name + "\n")
            输出音频的数据 = np.zeros((0, 总音频数据.shape[1]))
    # print(f'音频总帧数：{len(输出音频的数据) / 采样率 * 视频帧率}')
    # print(f'总共超出帧数：{超出 / 采样率 * 视频帧率}')
    concat记录文件.close()
    print('子线程中的音频文件处理完毕，只待视频流输出完成了')
    return

def 计算总共帧数(片段列表, 片段速度):
    总共帧数 = 0.0
    for 片段 in 片段列表:
        总共帧数 += (片段[1] - 片段[0]) / 片段速度[片段[2]]
    return int(总共帧数)

# @profile()
def ffmpeg和pyav综合处理视频流(文件, 临时视频文件, 片段列表, 静音片段速度, 有声片段速度, 视频编码器, 视频质量crf参数):
    开始时间 = time.time()
    片段速度 = [静音片段速度, 有声片段速度]

    input_ = av.open(文件)
    inputVideoStream = input_.streams.video[0]
    inputVideoStream.thread_type = 'AUTO'
    平均帧率 = float(inputVideoStream.average_rate)

    输入视频流查询命令 = f'ffprobe -of json -select_streams v -show_streams "{文件}"'
    输入视频流查询结果 = subprocess.run(shlex.split(输入视频流查询命令),
                                shell=True,
                               capture_output=True,
                               encoding='utf-8',
                                startupinfo=常量.subprocessStartUpInfo)
    输入视频流信息 = json.loads(输入视频流查询结果.stdout)

    height = 输入视频流信息['streams'][0]['height']
    width = 输入视频流信息['streams'][0]['width']
    pix_fmt = 输入视频流信息['streams'][0]['pix_fmt']


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
                                 '-s', f'{width}*{height}',
                                 '-vcodec', 视频编码器,
                                 '-crf', f'{视频质量crf参数}',
                                 临时视频文件]
    # print(process2Command)
    process2 = subprocess.Popen(process2Command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    帧率 = float(inputVideoStream.framerate)
    原始总帧数 = inputVideoStream.frames
    if 原始总帧数 == 0:
        原始总帧数 = int(得到输入视频时长(文件) * 平均帧率)
    总帧数 = 计算总共帧数(片段列表, 片段速度)

    print(f'输出视频总帧数：{int(总帧数)}，输出后时长：{秒数转时分秒(int(总帧数 / 平均帧率))}')

    输入等效, 输出等效 = 0.0, 0.0
    片段 = 片段列表.pop(0)
    开始时间 = time.time()
    视频帧序号 = 0
    index = 0
    for packet in input_.demux(inputVideoStream):
        for frame in packet.decode():
            frame = frame.reformat()
            index += 1
            if len(片段列表) > 0 and index >= 片段[1]:片段 = 片段列表.pop(0)
            输入等效 += (1 / 片段速度[片段[2]])
            while 输入等效 > 输出等效:
                # 经过测试得知，在一些分辨率的视频中，例如一行虽然只有 2160 个像素，但是这一行的数据不止 2160 个，有可能是2176个，然后所有行的数据是连在一起的
                # 在 python 里很难分离，只能使用 pyav 的 to_ndarray 再 tobytes
                if frame.planes[1].width != frame.planes[0].line_size:
                    # in_bytes = frame.to_ndarray().astype(np.uint8).tobytes()
                    in_bytes = frame.to_ndarray().tobytes()
                    process2.stdin.write(in_bytes)
                else:
                    if frame.format.name in ('yuv420p', 'yuvj420p'):
                        process2.stdin.write(frame.planes[0].to_bytes())
                        process2.stdin.write(frame.planes[1].to_bytes())
                        process2.stdin.write(frame.planes[2].to_bytes())
                    elif frame.format.name in ('yuyv422', 'rgb24', 'bgr24', 'argb', 'rgba', 'abgr', 'bgra', 'gray', 'gray8', 'rgb8', 'bgr8', 'pal8'):
                        process2.stdin.write(frame.planes[0].to_bytes())
                    else:
                        print(f'{frame.format.name} 像素格式不支持')
                        return False

                输出等效 += 1
                if 输出等效 % 200 == 0:
                    print(
                        f'帧速：{int(int(输出等效) / max(time.time() - 开始时间, 1))}, 剩余：{总帧数 - int(输出等效)} 帧，剩余时间：{秒数转时分秒(int((总帧数 - int(输出等效)) / max(1, int(输出等效) / max(time.time() - 开始时间, 1))))}    ')
    process2.stdin.close()
    process2.wait()
    del process2
    print(f'输出视频总帧数：{int(总帧数)}，输出后时长：{秒数转时分秒(int(总帧数 / 平均帧率))}')
    print(f'原来视频长度：{"{:.2f}".format(原始总帧数 / 平均帧率 / 60)} 分钟，输出视频长度：{"{:.2f}".format(int(输出等效) / 平均帧率 / 60)} 分钟')
    print(f'视频合成耗时：{秒数转时分秒(time.time() - 开始时间)}')
    return

def 秒数转时分秒(秒数):
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

# @profile()
def 跳剪(文件,
         输出文件,
         静音速度: float = 8.0,
         有声速度: float = 1.0,
         缓冲帧数: int = 2,
         有声阈值: float = 0.04,
         视频编码器: str = 'libx264',
         crf画质参数: float = 23.5,
         只处理音频: bool = False,
         辅助音频文件: str = '',
         使用spleeter=True,
         临时文件夹=None
         ):

    开始时间 = time.time()

    if not 临时文件夹: 临时文件夹 = tempfile.mkdtemp()

    # 得到 spleeter 分轨器
    if 使用spleeter:
        from spleeter.separator import Separator
        if type(使用spleeter) == Separator:
            分轨器 = 使用spleeter
        else:
            spleeter辅助音频文件名 = 'vocal.wav'
            # 模型要放到 pretrained_models 文件夹中
            spleeter使用模型名称 = '5stems'
            模型父文件夹 = Path(Path(__file__).parent)
            os.chdir(模型父文件夹)
            分轨器 = Separator(f'spleeter:{spleeter使用模型名称}', multiprocess=False)

    # 得到视频帧率
    if 只处理音频:
        视频帧率 = 30
    else:
        查询命令 = f'ffprobe -of json -select_streams v -show_streams "{文件}"'
        查询结果 = json.loads(subprocess.run(shlex.split(查询命令),
                    shell=True,
                            capture_output=True,
                            encoding='utf-8').stdout,
                            startupinfo=常量.subprocessStartUpInfo)

        if not 查询结果['streams']: # 没有视频轨
            print(f'无法得到视频帧率，认为输入只包含音频')
            只处理音频 = True
            视频帧率 = 30
        else:
            视频帧率 = float(eval(查询结果['streams'][0]['avg_frame_rate']))
            视频时长 = float(eval(查询结果['streams'][0]['duration']))

    # 得到文件音频采样率
    查询命令 = f'ffprobe -of json -select_streams a -show_streams "{文件}"'
    查询结果 = json.loads(subprocess.run(shlex.split(查询命令),
                    shell=True,
                                        capture_output=True,
                                        encoding='utf-8').stdout,
                                        startupinfo=常量.subprocessStartUpInfo)
    音频采样率 = float(eval(查询结果['streams'][0]['sample_rate']))

    # 设定音频路径
    if 使用spleeter or 辅助音频文件 != '':
        分析用的音频文件 = (Path(临时文件夹) / 'AnalyticAudio.wav').as_posix()
        变速用的音频文件 = (Path(临时文件夹) / 'OriginalAudio.wav').as_posix()
    else:
        分析用的音频文件 = (Path(临时文件夹) / 'OriginalAudio.wav').as_posix()
        变速用的音频文件 = (Path(临时文件夹) / 'OriginalAudio.wav').as_posix()

    # 提取原始音频
    提取音频流(文件, 变速用的音频文件, 音频采样率)

    # 提取辅助音频
    if 使用spleeter:
        由spleeter得到分析音频(输入文件=变速用的音频文件, 输出文件=分析用的音频文件, 分轨器=分轨器)
    elif 辅助音频文件 != '':
        提取音频流(辅助音频文件, 分析用的音频文件, 音频采样率)


    # 从音频得到片段列表
    片段列表 = 由音频得到片段列表(音频文件=分析用的音频文件, 视频帧率=视频帧率, 声音检测相对阈值=有声阈值, 片段间缓冲帧数=缓冲帧数)

    # pprint(片段列表)

    concat记录文件 = (Path(临时文件夹) / 'concat.txt').as_posix()
    音频处理线程 = threading.Thread(target=处理音频, args=[变速用的音频文件, 片段列表.copy(), 视频帧率, 静音速度, 有声速度, 临时文件夹, concat记录文件])
    音频处理线程.start()
    if not 只处理音频:
        临时视频文件 = (Path(临时文件夹) / 'Video.mp4').as_posix()
        ffmpeg和pyav综合处理视频流(文件, 临时视频文件, 片段列表, 静音速度, 有声速度, 视频编码器, crf画质参数)

    音频处理线程.join()

    print(f'现在开始合并')  # 合并音视频
    if 只处理音频:
        command = f'ffmpeg -y -hide_banner -safe 0  -f concat -i "{concat记录文件}" -i "{文件}" -c:v copy -map_metadata 1 -map_metadata:s:a 1:s:a -map 0:a "{输出文件}"'
    else:
        command = f'ffmpeg -y -hide_banner -i "{临时视频文件}" -safe 0 -f concat -i "{concat记录文件}" -i "{文件}" -c:v copy -map_metadata 2 -map_metadata:s:a 2:s:a -map_metadata:s:v 2:s:v -map 0:v -map 1:a  "{输出文件}"'
    subprocess.run(shlex.split(command),
                    shell=True,
                    encoding='utf-8',
                    stderr=subprocess.PIPE,
                    startupinfo=常量.subprocessStartUpInfo)
    try:
        rmtree(临时文件夹)
        ...
    except Exception as e:
        print(f'删除临时文件夹失败，可能是被占用导致，请手动删除：\n    {临时文件夹}')
    if platform.system() == 'Windows':
        os.system(f'explorer /select, "{Path(输出文件)}')
    else:
        os.startfile(Path(输出文件).parent)
    print(f'总共耗时：{秒数转时分秒(time.time() - 开始时间)}')
    return

def 跳剪2():
    print('worked')



