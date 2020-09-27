# -*- coding: UTF-8 -*-

import os
import sys

os.chdir(os.path.dirname(__file__)) # 更改工作目录，指向正确的当前文件夹，才能读取 database.db
sys.path.append(os.path.dirname(__file__)) # 将当前目录导入 python 寻找 package 和 moduel 的变量

import sqlite3
import platform
import subprocess

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

# try:
from moduels.function.createDB import * # 引入检查和创建创建数据库的函数
from moduels.function.checkDBLanguage import * # 引入检查和初始化语言设置的函数
from moduels.function.excepthook import *
from moduels.component.NormalValue import 常量
from moduels.gui.MainWindow import MainWindow
from moduels.gui.SystemTray import SystemTray
# except:
#     from QuickCut.moduels.function.createDB import * # 引入检查和创建创建数据库的函数


#
# import datetime
# from functools import wraps
# import json
# import math
# import os
# import re
# import srt
# import time
# from traceback import format_exception
# import urllib.parse
# import webbrowser
# import pyaudio
# import keyboard
# import threading
# import signal
# import auditok
# import pymediainfo
# import io
# import cv2
# from shutil import rmtree, move

#
# import numpy as np
# import oss2
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtSql import *
# from PyQt5.QtWidgets import *
# import requests
# from aliyunsdkcore.acs_exception.exceptions import ClientException
# from aliyunsdkcore.acs_exception.exceptions import ServerException
# from aliyunsdkcore.client import AcsClient
# from aliyunsdkcore.request import CommonRequest
#
# import ali_speech
# from ali_speech.callbacks import SpeechRecognizerCallback
# from ali_speech.constant import ASRFormat
# from ali_speech.constant import ASRSampleRate
#
# from audiotsm import phasevocoder
# from audiotsm.io.wav import WavReader, WavWriter
# from qcloud_cos import CosConfig
# from qcloud_cos import CosS3Client
# from scipy.io import wavfile
# from tencentcloud.asr.v20190614 import asr_client, models
# from tencentcloud.common import credential
# from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# from tencentcloud.common.profile.client_profile import ClientProfile
# from tencentcloud.common.profile.http_profile import HttpProfile



############# 程序入口 ################

def main():
    sys.excepthook = excepthook
    os.environ['PATH'] += os.pathsep + os.getcwd()
    app = QApplication(sys.argv)
    createDB()
    language = checkDBLanguage()  # 得到已设置的语言
    if language != '中文':
        print('language changed')
        translator = QTranslator()
        translator.load('./languages/%s.qm' % language)
        app.installTranslator(translator)
    mainWindow = MainWindow()
    # 常量.mainWindow = mainWindow
    mainWindow.capsWriterTab.initCapsWriterStatus()  # 只有在 mainWindow 初始化完成后，才能启动 capsWriter
    if 常量.platfm == 'Darwin':
        tray = SystemTray(QIcon('misc/icon.icns'), mainWindow)
    else:
        tray = SystemTray(QIcon('misc/icon.ico'), mainWindow)
    常量.tray = tray
    sys.exit(app.exec_())
    conn.close()

if __name__ == '__main__':
    main()
