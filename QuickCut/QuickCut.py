# -*- coding: UTF-8 -*-

import datetime
from functools import wraps
import json
import math
import os
import re
import sqlite3
import srt
import subprocess
import sys
import time
from traceback import format_exception
import urllib.parse
import webbrowser
import pyaudio
import keyboard
import threading
import platform
import signal
import auditok
import pymediainfo
import io
import cv2
from shutil import rmtree, move
try:
    os.chdir(os.path.dirname(__file__))
except:
    print('更改工作目录失败，关系不大，不用管它')

import numpy as np
import oss2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
import requests
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

import ali_speech
from ali_speech.callbacks import SpeechRecognizerCallback
from ali_speech.constant import ASRFormat
from ali_speech.constant import ASRSampleRate

from audiotsm import phasevocoder
from audiotsm.io.wav import WavReader, WavWriter
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from scipy.io import wavfile
from tencentcloud.asr.v20190614 import asr_client, models
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile


try:
    from moduels.SystemTray import SystemTray # 引入托盘栏
except:
    from QuickCut.moduels.SystemTray import SystemTray # 引入托盘栏

dbname = './database.db'  # 存储预设的数据库名字
presetTableName = 'commandPreset'  # 存储预设的表单名字
ossTableName = 'oss'
apiTableName = 'api'
preferenceTableName = 'preference'
styleFile = './style.css'  # 样式表的路径
finalCommand = ''
version = 'V1.6.10'




############# 程序入口 ################

def main():
    global app, conn, language, translator, apiUpdateBroadCaster, platfm, subprocessStartUpInfo, mainWindow, tray
    sys.excepthook = excepthook
    os.environ['PATH'] += os.pathsep + os.getcwd()
    app = QApplication(sys.argv)
    conn = sqlite3.connect(dbname)
    createDB()
    language = checkDBLanguage()  # 得到已设置的语言
    if language != '中文':
        print('language changed')
        translator = QTranslator()
        translator.load('./languages/%s.qm' % language)
        app.installTranslator(translator)
    apiUpdateBroadCaster = ApiUpdated()
    platfm = platform.system()
    if platfm == 'Windows':
        global subprocessStartUpInfo
        subprocessStartUpInfo = subprocess.STARTUPINFO()
        subprocessStartUpInfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
        subprocessStartUpInfo.wShowWindow = subprocess.SW_HIDE
    else:
        pass
    mainWindow = MainWindow()
    mainWindow.capsWriterTab.initCapsWriterStatus()  # 只有在 mainWindow 初始化完成后，才能启动 capsWriter
    if platfm == 'Darwin':
        tray = SystemTray(QIcon('misc/icon.icns'), mainWindow)
    else:
        tray = SystemTray(QIcon('misc/icon.ico'), mainWindow)
    sys.exit(app.exec_())
    conn.close()

if __name__ == '__main__':
    main()
