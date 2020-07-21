# -*- coding: UTF-8 -*-
import os, sys, re, time, datetime, sqlite3, subprocess, threading, platform
import requests, json, base64, urllib.parse, srt


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *

from contextlib import closing
from PIL import Image
from audiotsm import phasevocoder
from audiotsm.io.wav import WavReader, WavWriter
from scipy.io import wavfile
import numpy as np
import math
from shutil import copyfile, rmtree, move



import oss2
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import logging

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.asr.v20190614 import asr_client, models

# from PyQt5.QtWidgets import QListWidget, QWidget, QApplication, QFileDialog, QMainWindow, QDialog, QLabel, QLineEdit, QTextEdit, QPlainTextEdit, QTabWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout, QPushButton, QCheckBox, QSplitter
# from PyQt5.QtGui import QCloseEvent
# from PyQt5.QtCore import Qt

print('开始运行')
dbname = './database.db'  # 存储预设的数据库名字
presetTableName = 'commandPreset'  # 存储预设的表单名字
ossTableName = 'oss'
apiTableName = 'api'
finalCommand = ''


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initGui()
        # sys.stdout = Stream(newText=self.onUpdateText)
        self.status = self.statusBar()


    def initGui(self):
        # 定义中心控件为多 tab 页面
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # 定义多个不同功能的 tab
        self.ffmpegMainTab = FFmpegMainTab()  # 主要功能的 tab
        self.ffmpegCutVideoTab = FFmpegCutVideoTab()  # 剪切视频的 tab
        self.ffmpegConcatTab = FFmpegConcatTab()  # 合并视频的 tab
        self.ffmpegBurnCaptionTab = FFmpegBurnCaptionTab()  # 烧字幕的 tab
        self.apiConfigTab = ApiConfigTab()  # 配置 Api 的 tab
        self.ffmpegAutoEditTab = FFmpegAutoEditTab()  # 自动剪辑的 tab
        self.ffmpegAutoSrtTab = FFmpegAutoSrtTab()  # 自动转字幕的 tab
        # self.consoleTab = ConsoleTab() # 新的控制台输出 tab
        self.helpTab = HelpTab()  # 帮助
        # self.aboutTab = AboutTab()  # 关于

        # 将不同功能的 tab 添加到主 tabWidget
        self.tabs.addTab(self.ffmpegMainTab, 'FFmpeg 主功能')
        # self.tabs.addTab(self.ffmpegCutVideoTab, '截取片段')
        self.tabs.addTab(self.ffmpegConcatTab, '合并片段')
        self.tabs.addTab(self.ffmpegBurnCaptionTab, '嵌入字幕')
        self.tabs.addTab(self.ffmpegAutoEditTab, '自动跳跃剪辑')
        self.tabs.addTab(self.ffmpegAutoSrtTab, '自动字幕')
        self.tabs.addTab(self.apiConfigTab, '设置')
        # self.tabs.addTab(self.consoleTab, '控制台')
        self.tabs.addTab(self.helpTab, '帮助')
        # self.tabs.addTab(self.aboutTab, '关于')

        self.adjustSize()
        self.setWindowTitle('FFmpeg GUI（轻量好用的视频剪辑工具）')

        # self.setWindowFlag(Qt.WindowStaysOnTopHint) # 始终在前台
        self.show()

        # test.show()

    def onUpdateText(self, text):
        """Write console output to text widget."""

        cursor = self.consoleTab.consoleEditBox.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.consoleTab.consoleEditBox.setTextCursor(cursor)
        self.consoleTab.consoleEditBox.ensureCursorVisible()



    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        sys.stdout = sys.__stdout__
        super().closeEvent(event)

# noinspection PyBroadException,PyGlobalUndefined
class FFmpegMainTab(QWidget):
    def __init__(self):
        super().__init__()

        self.输入输出vbox = QVBoxLayout()
        # 构造输入一、输入二和输出选项
        if True:
            # 输入1
            if True:
                self.输入1标签 = QLabel('输入1路径：')
                self.输入1路径框 = QLineEdit()
                self.输入1路径框.textChanged.connect(self.generateFinalCommand)
                self.输入1选择文件按钮 = QPushButton('选择文件')
                self.输入1选择文件按钮.clicked.connect(self.chooseFile1ButtonClicked)
                self.输入1路径hbox = QHBoxLayout()
                self.输入1路径hbox.addWidget(self.输入1标签, 0)
                self.输入1路径hbox.addWidget(self.输入1路径框, 1)
                self.输入1路径hbox.addWidget(self.输入1选择文件按钮, 0)

                self.输入1截取时间hbox = QHBoxLayout()
                self.输入1截取时间勾选框 = QCheckBox('截取片段')
                self.输入1截取时间勾选框.clicked.connect(self.inputOneCutCheckboxClicked)
                self.输入1截取时间勾选框.clicked.connect(self.generateFinalCommand)
                self.输入1截取时间start标签 = QLabel('起始时间：')
                self.输入1截取时间start输入框 = self.CutTimeEdit()
                self.输入1截取时间start输入框.textChanged.connect(self.generateFinalCommand)
                self.输入1截取时间start输入框.setAlignment(Qt.AlignCenter)
                self.输入1截取时间end标签 = self.ClickableEndTimeLable()
                # self.输入1截取时间end标签.mousePressEvent.connect(self.generateFinalCommand)
                self.输入1截取时间end输入框 = self.CutTimeEdit()
                self.输入1截取时间end输入框.textChanged.connect(self.generateFinalCommand)
                self.输入1截取时间end输入框.setAlignment(Qt.AlignCenter)
                self.输入1截取时间hbox.addWidget(self.输入1截取时间勾选框)
                self.输入1截取时间hbox.addWidget(self.输入1截取时间start标签)
                self.输入1截取时间hbox.addWidget(self.输入1截取时间start输入框)
                self.输入1截取时间hbox.addWidget(self.输入1截取时间end标签)
                self.输入1截取时间hbox.addWidget(self.输入1截取时间end输入框)
                self.输入1截取时间start标签.setVisible(False)
                self.输入1截取时间start输入框.setVisible(False)
                self.输入1截取时间end标签.setVisible(False)
                self.输入1截取时间end输入框.setVisible(False)

                self.输入1选项hbox = QHBoxLayout()
                self.输入1选项标签 = QLabel('输入1选项：')
                self.输入1选项输入框 = QLineEdit()
                self.输入1选项输入框.textChanged.connect(self.generateFinalCommand)
                self.输入1选项hbox.addWidget(self.输入1选项标签)
                self.输入1选项hbox.addWidget(self.输入1选项输入框)

                self.输入1vbox = QVBoxLayout()
                self.输入1vbox.addLayout(self.输入1路径hbox)
                self.输入1vbox.addLayout(self.输入1选项hbox)
                self.输入1vbox.addLayout(self.输入1截取时间hbox)

            # 输入2
            if True:
                self.输入2标签 = QLabel('输入2路径：')
                self.输入2路径框 = QLineEdit()
                self.输入2路径框.textChanged.connect(self.generateFinalCommand)
                self.输入2选择文件按钮 = QPushButton('选择文件')
                self.输入2选择文件按钮.clicked.connect(self.chooseFile2ButtonClicked)
                self.输入2路径hbox = QHBoxLayout()
                self.输入2路径hbox.addWidget(self.输入2标签, 0)
                self.输入2路径hbox.addWidget(self.输入2路径框, 1)
                self.输入2路径hbox.addWidget(self.输入2选择文件按钮, 0)

                self.输入2截取时间hbox = QHBoxLayout()
                self.输入2截取时间勾选框 = QCheckBox('截取片段')
                self.输入2截取时间勾选框.clicked.connect(self.inputTwoCutCheckboxClicked)
                self.输入2截取时间勾选框.clicked.connect(self.generateFinalCommand)
                self.输入2截取时间start标签 = QLabel('起始时间：')
                self.输入2截取时间start输入框 = self.CutTimeEdit()
                self.输入2截取时间start输入框.setAlignment(Qt.AlignCenter)
                self.输入2截取时间start输入框.textChanged.connect(self.generateFinalCommand)
                self.输入2截取时间end标签 = self.ClickableEndTimeLable()
                self.输入2截取时间end输入框 = self.CutTimeEdit()
                self.输入2截取时间end输入框.setAlignment(Qt.AlignCenter)
                self.输入2截取时间end输入框.textChanged.connect(self.generateFinalCommand)
                self.输入2截取时间hbox.addWidget(self.输入2截取时间勾选框)
                self.输入2截取时间hbox.addWidget(self.输入2截取时间start标签)
                self.输入2截取时间hbox.addWidget(self.输入2截取时间start输入框)
                self.输入2截取时间hbox.addWidget(self.输入2截取时间end标签)
                self.输入2截取时间hbox.addWidget(self.输入2截取时间end输入框)
                self.输入2截取时间start标签.setVisible(False)
                self.输入2截取时间start输入框.setVisible(False)
                self.输入2截取时间end标签.setVisible(False)
                self.输入2截取时间end输入框.setVisible(False)

                self.输入2选项hbox = QHBoxLayout()
                self.输入2选项标签 = QLabel('输入2选项：')
                self.输入2选项输入框 = QLineEdit()
                self.输入2选项输入框.textChanged.connect(self.generateFinalCommand)
                self.输入2选项hbox.addWidget(self.输入2选项标签)
                self.输入2选项hbox.addWidget(self.输入2选项输入框)

                self.输入2vbox = QVBoxLayout()
                self.输入2vbox.addLayout(self.输入2路径hbox)
                self.输入2vbox.addLayout(self.输入2选项hbox)
                self.输入2vbox.addLayout(self.输入2截取时间hbox)

            # 输出
            if True:
                self.输出标签 = QLabel('输出：')
                self.输出路径框 = QLineEdit()
                self.输出路径框.textChanged.connect(self.generateFinalCommand)
                self.输出选择文件按钮 = QPushButton('选择保存位置')
                self.输出选择文件按钮.clicked.connect(self.chooseOutputFileButtonClicked)
                self.输出路径hbox = QHBoxLayout()
                self.输出路径hbox.addWidget(self.输出标签, 0)
                self.输出路径hbox.addWidget(self.输出路径框, 1)
                self.输出路径hbox.addWidget(self.输出选择文件按钮, 0)

                self.输出分辨率hbox = QHBoxLayout()
                self.输出分辨率勾选框 = QCheckBox('新分辨率')
                self.输出分辨率勾选框.clicked.connect(self.outputResolutionCheckboxClicked)
                self.输出分辨率勾选框.clicked.connect(self.generateFinalCommand)

                self.X轴分辨率输入框 = self.ResolutionEdit()
                self.X轴分辨率输入框.setAlignment(Qt.AlignCenter)
                self.X轴分辨率输入框.textChanged.connect(self.generateFinalCommand)
                self.分辨率乘号标签 = self.ClickableResolutionTimesLable()
                self.Y轴分辨率输入框 = self.ResolutionEdit()
                self.Y轴分辨率输入框.setAlignment(Qt.AlignCenter)
                self.Y轴分辨率输入框.textChanged.connect(self.generateFinalCommand)
                self.分辨率预设按钮 = QPushButton('分辨率预设')
                self.分辨率预设按钮.clicked.connect(self.resolutionPresetButtonClicked)
                self.X轴分辨率输入框.setVisible(False)
                self.分辨率乘号标签.setVisible(False)
                self.Y轴分辨率输入框.setVisible(False)
                self.分辨率预设按钮.setVisible(False)

                self.输出分辨率hbox.addWidget(self.输出分辨率勾选框, 0)
                self.输出分辨率hbox.addWidget(self.X轴分辨率输入框, 1)
                self.输出分辨率hbox.addWidget(self.分辨率乘号标签, 0)
                self.输出分辨率hbox.addWidget(self.Y轴分辨率输入框, 1)
                self.输出分辨率hbox.addWidget(self.分辨率预设按钮, 0)

                self.输出选项标签 = QLabel('输出选项：')
                self.输出选项输入框 = QPlainTextEdit()
                self.输出选项输入框.textChanged.connect(self.generateFinalCommand)
                self.输出选项输入框.setMaximumHeight(100)
                self.输出选项hbox = QHBoxLayout()
                self.输出选项hbox.addWidget(self.输出选项标签)
                self.输出选项hbox.addWidget(self.输出选项输入框)

                self.输出vbox = QVBoxLayout()
                self.输出vbox.addLayout(self.输出路径hbox)
                self.输出vbox.addLayout(self.输出分辨率hbox)
                self.输出vbox.addLayout(self.输出选项hbox)

            # 输入输出放到一个布局
            if True:
                self.主布局 = QVBoxLayout()
                self.主布局.addLayout(self.输入1vbox)
                self.主布局.addSpacing(15)
                self.主布局.addLayout(self.输入2vbox)
                self.主布局.addSpacing(15)
                self.主布局.addLayout(self.输出vbox)

            # 输入输出布局放到一个控件
            self.主布局控件 = QWidget()
            self.主布局控件.setLayout(self.主布局)

        # 预设列表
        if True:
            self.预设列表提示标签 = QLabel('选择预设：')
            self.预设列表 = QListWidget()
            self.预设列表.itemClicked.connect(self.presetItemSelected)
            self.预设列表.itemDoubleClicked.connect(self.addPresetButtonClicked)

            self.添加预设按钮 = QPushButton('+')
            self.删除预设按钮 = QPushButton('-')
            # self.修改预设按钮 = QPushButton('修改选中预设')
            self.上移预设按钮 = QPushButton('↑')
            self.下移预设按钮 = QPushButton('↓')
            self.查看预设帮助按钮 = QPushButton('查看该预设帮助')
            self.预设vbox = QGridLayout()
            self.预设vbox.addWidget(self.预设列表提示标签, 0, 0, 1, 1)
            self.预设vbox.addWidget(self.预设列表, 1, 0, 1, 2)
            self.预设vbox.addWidget(self.上移预设按钮, 2, 0, 1, 1)
            self.预设vbox.addWidget(self.下移预设按钮, 2, 1, 1, 1)
            self.预设vbox.addWidget(self.添加预设按钮, 3, 0, 1, 1)
            self.预设vbox.addWidget(self.删除预设按钮, 3, 1, 1, 1)
            # self.预设vbox.addWidget(self.修改预设按钮, 3, 0, 1, 1)
            self.预设vbox.addWidget(self.查看预设帮助按钮, 4, 0, 1, 2)
            self.预设vbox控件 = QWidget()
            self.预设vbox控件.setLayout(self.预设vbox)

            self.上移预设按钮.clicked.connect(self.upwardButtonClicked)
            self.下移预设按钮.clicked.connect(self.downwardButtonClicked)
            self.添加预设按钮.clicked.connect(self.addPresetButtonClicked)
            self.删除预设按钮.clicked.connect(self.delPresetButtonClicked)
            # self.修改预设按钮.clicked.connect(self.modifyPresetButtonClicked)
            self.查看预设帮助按钮.clicked.connect(self.checkPresetHelpButtonClicked)

        # 总命令编辑框
        if True:
            self.总命令编辑框 = QPlainTextEdit()
            self.总命令编辑框.setPlaceholderText('这里是自动生成的总命令')

            self.总命令编辑框.setMaximumHeight(100)
            self.总命令执行按钮 = QPushButton('运行')
            self.总命令执行按钮.clicked.connect(self.runFinalCommandButtonClicked)
            self.总命令部分vbox = QVBoxLayout()
            self.总命令部分vbox.addWidget(self.总命令编辑框)
            self.总命令部分vbox.addWidget(self.总命令执行按钮)
            self.总命令部分vbox控件 = QWidget()
            self.总命令部分vbox控件.setLayout(self.总命令部分vbox)

        # 放置三个主要部件
        if True:
            # 分割线左边放输入输出布局，右边放列表
            self.竖分割线 = QSplitter(Qt.Horizontal)
            self.竖分割线.addWidget(self.主布局控件)
            self.竖分割线.addWidget(self.预设vbox控件)

            self.横分割线 = QSplitter(Qt.Vertical)
            self.横分割线.addWidget(self.竖分割线)
            self.横分割线.addWidget(self.总命令部分vbox控件)

            # 用一个横向布局，将分割线放入
            self.最顶层布局hbox = QHBoxLayout()
            self.最顶层布局hbox.addWidget(self.横分割线)

            # 将本页面的布局设为上面的横向布局
            self.setLayout(self.最顶层布局hbox)

        # 检查杂项文件夹是否存在
        self.createMiscFolder()

        # 检查数据库是否存在
        self.createDB()

        # 刷新预设列表
        self.refreshList()

        # 连接数据库，供以后查询和更改使用
        self.conn = sqlite3.connect(dbname)

    # 选择输入文件1
    def chooseFile1ButtonClicked(self):
        filename = QFileDialog().getOpenFileName(self, '打开文件', None, '所有文件(*)')
        if filename[0] != '':
            self.输入1路径框.setText(filename[0])
            outputName = re.sub(r'(\.[^\.]+)$', r'_out\1', filename[0])
            self.输出路径框.setText(outputName)
        return True

    # 选择输入文件2
    def chooseFile2ButtonClicked(self):
        filename = QFileDialog().getOpenFileName(self, '打开文件', None, '所有文件(*)')
        if filename[0] != '':
            self.输入2路径框.setText(filename[0])
        return True

    # 选择输出文件
    def chooseOutputFileButtonClicked(self):
        filename = QFileDialog().getSaveFileName(self, '设置输出保存的文件名', '输出视频.mp4', '所有文件(*)')
        self.输出路径框.setText(filename[0])
        return True

    # 输出一截取勾选框
    def inputOneCutCheckboxClicked(self):
        if self.输入1截取时间勾选框.isChecked():
            self.输入1截取时间start标签.setVisible(True)
            self.输入1截取时间start输入框.setVisible(True)
            self.输入1截取时间end标签.setVisible(True)
            self.输入1截取时间end输入框.setVisible(True)
        else:
            self.输入1截取时间start标签.setVisible(False)
            self.输入1截取时间start输入框.setVisible(False)
            self.输入1截取时间end标签.setVisible(False)
            self.输入1截取时间end输入框.setVisible(False)
        return True

    # 输出2截取勾选框
    def inputTwoCutCheckboxClicked(self):
        if self.输入2截取时间勾选框.isChecked():
            self.输入2截取时间start标签.setVisible(True)
            self.输入2截取时间start输入框.setVisible(True)
            self.输入2截取时间end标签.setVisible(True)
            self.输入2截取时间end输入框.setVisible(True)
        else:
            self.输入2截取时间start标签.setVisible(False)
            self.输入2截取时间start输入框.setVisible(False)
            self.输入2截取时间end标签.setVisible(False)
            self.输入2截取时间end输入框.setVisible(False)
        return True

        # 输出分辨率勾选框

    # 输出分辨率勾选框
    def outputResolutionCheckboxClicked(self):
        if self.输出分辨率勾选框.isChecked():
            self.X轴分辨率输入框.setVisible(True)
            self.分辨率乘号标签.setVisible(True)
            self.Y轴分辨率输入框.setVisible(True)
            self.分辨率预设按钮.setVisible(True)
        else:
            self.X轴分辨率输入框.setVisible(False)
            self.分辨率乘号标签.setVisible(False)
            self.Y轴分辨率输入框.setVisible(False)
            self.分辨率预设按钮.setVisible(False)
        return True

    def resolutionPresetButtonClicked(self):
        self.ResolutionDialog()
        return True

    # 自动生成总命令
    def generateFinalCommand(self):
        self.finalCommand = 'ffmpeg -y -hide_banner'
        inputOnePath = self.输入1路径框.text()
        if inputOnePath != '':  # 只有有输入文件1时才会继续生成命令

            inputOneCutSwitch = self.输入1截取时间勾选框.isChecked()
            if inputOneCutSwitch != 0:
                inputOneStartTime = self.输入1截取时间start输入框.text()
                if inputOneStartTime != '':
                    self.finalCommand = self.finalCommand + ' ' + '-ss %s' % (inputOneStartTime)
                inputOneEndTime = self.输入1截取时间end输入框.text()
                if inputOneEndTime != '':
                    if self.输入1截取时间end标签.text() == '截取时长：':
                        self.finalCommand = self.finalCommand + ' ' + '-t %s' % (inputOneEndTime)
                    elif self.输入1截取时间end标签.text() == '截止时刻：':
                        self.finalCommand = self.finalCommand + ' ' + '-to %s' % (inputOneEndTime)
            inputOneOption = self.输入1选项输入框.text()
            if inputOneOption != '':
                self.finalCommand = self.finalCommand + ' ' + inputOneOption

            self.finalCommand = self.finalCommand + ' ' + '-i "%s"' % (inputOnePath)

            inputTwoPath = self.输入2路径框.text()
            if inputTwoPath != '':  # 只有有输入文件2时才会继续生成命令
                inputTwoCutSwitch = self.输入2截取时间勾选框.isChecked()
                if inputTwoCutSwitch != 0:
                    inputTwoStartTime = self.输入2截取时间start输入框.text()
                    if inputTwoStartTime != '':
                        self.finalCommand = self.finalCommand + ' ' + '-ss %s' % (inputTwoStartTime)
                    inputTwoEndTime = self.输入2截取时间end输入框.text()
                    if inputTwoEndTime != '':
                        if self.输入2截取时间end标签.text() == '截取时长：':
                            self.finalCommand = self.finalCommand + ' ' + '-t %s' % (inputTwoEndTime)
                        elif self.输入2截取时间end标签.text() == '截止时刻：':
                            self.finalCommand = self.finalCommand + ' ' + '-to %s' % (inputTwoEndTime)
                inputTwoOption = self.输入2选项输入框.text()
                if inputTwoOption != '':
                    self.finalCommand = self.finalCommand + ' ' + inputTwoOption
                self.finalCommand = self.finalCommand + ' ' + '-i "%s"' % (inputTwoPath)

            outputOption = self.输出选项输入框.toPlainText()
            if self.输出分辨率勾选框.isChecked() != 0:
                outputResizeX = self.X轴分辨率输入框.text()
                if outputResizeX == '':
                    outputResizeX = '-2'
                outputResizeY = self.Y轴分辨率输入框.text()
                if outputResizeY == '':
                    outputResizeY = '-2'
                if '-vf' not in self.finalCommand and 'scale' not in outputOption and 'filter' not in outputOption:
                    print(False)
                    self.finalCommand = self.finalCommand + ' ' + '-vf "scale=%s:%s"' % (outputResizeX, outputResizeY)
                elif 'scale' in outputOption:
                    print(True)
                    outputOption = re.sub('[-0-9]+:[-0-9]+', '%s:%s' % (outputResizeX, outputResizeY), outputOption)
            if outputOption != '':
                self.finalCommand = self.finalCommand + ' ' + outputOption
            outputPath = self.输出路径框.text()
            if outputPath != '':
                self.finalCommand = self.finalCommand + ' ' + '"%s"' % (outputPath)

            if self.预设列表.currentRow() > -1:
                if self.extraCode != '' and self.extraCode != None:
                    try:
                        exec(self.extraCode)
                    except:
                        pass

            self.总命令编辑框.setPlainText(self.finalCommand)
        return True

    # 点击运行按钮
    def runFinalCommandButtonClicked(self):
        finalCommand = self.总命令编辑框.toPlainText()
        if finalCommand != '':
            execute(finalCommand)

    # 检查杂项文件夹是否存在
    def createMiscFolder(self):
        if not os.path.exists('./misc'):
            os.mkdir('./misc')

    # 检查数据库是否存在
    def createDB(self):
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
        result = cursor.execute('select * from sqlite_master where name = "%s";' % (presetTableName))
        # 将初始预设写入数据库
        if result.fetchone() == None:
            cursor.execute('''create table %s (
                            id integer primary key autoincrement, 
                            name text, 
                            inputOneOption TEXT, 
                            inputTwoOption TEXT, 
                            outputExt TEXT, 
                            outputOption TEXT, 
                            extraCode TEXT, 
                            description TEXT
                            )''' % (presetTableName))
            print('新建了表单')

            # 新建一个空预设
            cursor.execute('''
                            insert into %s 
                            (name) 
                            values (
                            "不使用预设"
                            );'''
                           % (presetTableName))

            description = '''h264压制'''
            cursor.execute('''
                            insert into %s 
                            (name, outputOption, description) 
                            values (
                            'H264压制', 
                            '-c:v libx264 -crf 23 -preset slow -qcomp 0.5 -psy-rd 0.3:0 -aq-mode 2 -aq-strength 0.8 -c:a copy',
                            '%s'
                            );'''
                           % (presetTableName, description.replace("'", "''")))
            description = '''h265压制'''
            cursor.execute('''
                            insert into %s 
                            (name, outputOption, description) 
                            values (
                            "H265压制", 
                            "-c:v libx265 -crf 28 -c:a copy",
                            '%s'
                            );'''
                           % (presetTableName, description.replace("'", "''")))
            description = '''h264恒定比特率压制'''
            cursor.execute('''
                            insert into %s 
                            (name, outputOption, description)
                            values (
                            "H264压制目标比特率6000k", 
                            "-c:a copy -b:v 6000k",
                            '%s'
                            );'''
                           % (presetTableName, description.replace("'", "''")))
            description = '''h264恒定比特率二压'''
            extraCode = """nullPath = '/dev/null'
connector = '&&'
platfm = platform.system()
if platfm == 'Windows':
    nullPath = 'NUL'
inputOne = self.输入1路径框.text()
inputOneWithoutExt = os.path.splitext(inputOne)[0]
outFile = self.输出路径框.text()
outFileWithoutExt = os.path.splitext(outFile)[0]
logFileName = outFileWithoutExt + r'-0.log'
logTreeFileName = outFileWithoutExt + r'-0.log.mbtree'
tempCommand = self.finalCommand.replace('"' + outFile + '"', r'-passlogfile "%s"' % (
    outFileWithoutExt) + ' "' + outFile + '"')
self.finalCommand = r'''ffmpeg -y -hide_banner -i "%s" -passlogfile "%s"  -c:v libx264 -pass 1 -an -f rawvideo "%s" %s %s %s rm "%s" %s rm "%s"''' % (
inputOne, outFileWithoutExt, nullPath, connector, tempCommand, connector, logFileName, connector,
logTreeFileName)
"""
            extraCode = extraCode.replace("'", "''")
            cursor.execute('''
                            insert into %s 
                            (name, outputOption, extraCode, description)
                            values (
                            "H264 二压 目标比特率2000k", 
                            "-c:v libx264 -pass 2 -b:v 2000k -preset slow -c:a copy", 
                            '%s',
                            '%s'
                            );'''
                           % (presetTableName, extraCode, description.replace("'", "''")))

            cursor.execute('''
                            insert into %s
                            (name, outputExt, outputOption)
                            values (
                            '复制视频流到mp4容器', 
                            'mp4', 
                            '-c:v copy'
                            );''' % presetTableName)
            cursor.execute('''
                            insert into %s
                            (name, outputExt, outputOption)
                            values (
                            '将输入文件打包到mkv格式容器', 
                            'mkv', 
                            '-c copy'
                            );''' % presetTableName)
            cursor.execute('''
                            insert into %s
                            (name, outputExt, outputOption)
                            values (
                            '转码到mp3格式', 
                            'mp3', 
                            '-vn'
                            );''' % presetTableName)
            description = '''GIF (15fps 480p)'''
            cursor.execute('''
                            insert into %s 
                            (name, outputExt, outputOption, description)
                            values (
                            'GIF (15fps 480p)', 
                            'gif', 
                            '-filter_complex "[0:v] scale=480:-1, fps=15, split [a][b];[a] palettegen [p];[b][p] paletteuse"',
                            '%s'
                            );'''
                           % (presetTableName, description.replace("'", "''")))
            outputOption = '''-vf "split [main][tmp]; [tmp] crop=宽:高:X轴位置:Y轴位置, boxblur=luma_radius=25:luma_power=2:enable='between(t,第几秒开始,第几秒结束)'[tmp]; [main][tmp] overlay=X轴位置:Y轴位置"'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '区域模糊', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            outputOption = '''-filter_complex "[0:v]setpts=1/2*PTS[v];[0:a]atempo=2 [a]" -map "[v]" -map "[a]" '''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '视频两倍速', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            outputOption = '''-filter_complex "[0:a]atempo=2.0[a]" -map "[a]"'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '音频两倍速', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            outputOption = '''-filter_complex "[0:v]setpts=2*PTS[v];[0:a]atempo=1/2 [a];[v]minterpolate='mi_mode=mci:mc_mode=aobmc:me_mode=bidir:mb_size=16:vsbmc=1:fps=60'[v]" -map "[v]" -map "[a]" -max_muxing_queue_size 1024'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '视频0.5倍速 + 光流法补帧到60帧', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            outputOption = '''-filter_complex "[0:v]scale=-2:-2[v];[v]minterpolate='mi_mode=mci:mc_mode=aobmc:me_mode=bidir:mb_size=16:vsbmc=1:fps=60'" -max_muxing_queue_size 1024'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '光流法补帧到60帧', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            outputOption = '''-vf reverse -af areverse'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '视频倒放', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            outputOption = '''-af areverse'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '音频倒放', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            outputOption = '''-aspect:0 16:9'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '设置画面比例', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            inputOneOption = '''-itsoffset 1'''
            inputOneOption = inputOneOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, inputOneOption)
                            values (
                            '视频流时间戳偏移，用于同步音画', 
                            '%s'
                            );''' % (presetTableName, inputOneOption))
            outputOption = ''' -r 1 -q:v 2 -f image2 -tatget pal-dvcd-r'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputExt, outputOption)
                            values (
                            '从视频区间每秒提取n张照片', 
                            '%s', 
                            '%s'
                            );''' % (presetTableName, r'%03d.jpg', outputOption))
            outputOption = '''-vframes 5'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputExt, outputOption)
                            values (
                            '截取指定数量的帧保存为图片', 
                            '%s', 
                            '%s'
                            );''' % (presetTableName, r'%03d.jpg', outputOption))
            outputOption = '''-c:v libx264 -tune stillimage -c:a aac -shortest'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, inputOneOption, outputOption)
                            values (
                            '一图流', 
                            '-loop 1', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            outputOption = '''-c:v libx264 -tune stillimage -c:a aac -shortest'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, inputOneOption, outputOption)
                            values (
                            '一图流', 
                            '-loop 1', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            outputOption = '''-strict -2 -vf crop=w:h:x:y'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '裁切视频画面', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            outputOption = '''-c copy -metadata:s:v:0 rotate=90'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '视频旋转度数', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            outputOption = '''-vf "hflip" '''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '水平翻转画面', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            outputOption = '''-vf "vflip" '''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '垂直翻转画面', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            outputOption = '''-vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" '''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '设定至指定分辨率，并且自动填充黑边', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            outputOption = '''-map 0 -map 1 -c copy -c:v:1 jpg -disposition:v:1 attached_pic'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '视频或音乐添加封面图片', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            outputOption = '''-af "loudnorm=i=-24.0:lra=7.0:tp=-2.0:" -c:v copy'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '声音响度标准化', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            outputOption = '''-af "volume=1.0"'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '音量大小调节', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            outputOption = '''-map_channel -1 -map_channel 0.0.1 '''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '静音第一个声道', 
                            '%s'
                            );''' % (presetTableName, outputOption))
            outputOption = '''-map_channel [-1]"'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '静音所有声道', 
                            '%s'
                            );''' % (presetTableName, outputOption))

            outputOption = '''-map_channel 0.0.1 -map_channel 0.0.0 '''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '交换左右声道', 
                            '%s'
                            );''' % (presetTableName, outputOption))

            outputOption = '''-filter_complex "[0:1] [1:1] amerge" -c:v copy'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '两个音频流混合到一个文件', 
                            '%s'
                            );''' % (presetTableName, outputOption))

        else:
            print('存储"预设"的表单已存在')
        conn.commit()
        conn.close()
        return True

    # 将数据库的预设填入列表（更新列表）
    def refreshList(self):
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
        presetData = cursor.execute(
            'select id, name, inputOneOption, inputTwoOption, outputExt, outputOption, extraCode from %s order by id' % (
                presetTableName))
        self.预设列表.clear()
        for i in presetData:
            self.预设列表.addItem(i[1])
        conn.close()
        pass

    # 选择一个预设时，将预设中的命令填入相应的框
    def presetItemSelected(self, Index):
        global 当前已选择的条目
        当前已选择的条目 = self.预设列表.item(self.预设列表.row(Index)).text()
        print(当前已选择的条目)
        presetData = self.conn.cursor().execute(
            'select id, name, inputOneOption, inputTwoOption, outputExt, outputOption, extraCode, description from %s where name = "%s"' % (
                presetTableName, 当前已选择的条目)).fetchone()
        self.inputOneOption = presetData[2]
        self.inputTwoOption = presetData[3]
        self.outputExt = presetData[4]
        # print(presetData[4])
        self.outputOption = presetData[5]
        self.extraCode = presetData[6]
        self.description = presetData[7]
        if self.inputOneOption != None:
            self.输入1选项输入框.setText(self.inputOneOption)
        else:
            self.输入1选项输入框.clear()

        if self.inputTwoOption != None:
            self.输入2选项输入框.setText(self.inputTwoOption)
        else:
            self.输入2选项输入框.clear()

        if self.outputExt != None and self.outputExt != '':
            原来的输出路径 = self.输出路径框.text()
            if '.' in self.outputExt:
                修改后缀名后的输出路径 = re.sub('\..+?$', self.outputExt, 原来的输出路径)
            else:
                修改后缀名后的输出路径 = re.sub('(?<=\.).+?$', self.outputExt, 原来的输出路径)
            if 修改后缀名后的输出路径 != '':
                self.输出路径框.setText(修改后缀名后的输出路径)
            pass

        if self.outputOption != None:
            self.输出选项输入框.setPlainText(self.outputOption)
        else:
            self.输出选项输入框.clear()

    # 点击添加一个预设
    def addPresetButtonClicked(self):
        dialog = self.SetupPresetItemDialog()

    # 点击删除按钮后删除预设
    def delPresetButtonClicked(self):
        global 当前已选择的条目
        try:
            当前已选择的条目
            answer = QMessageBox.question(self, '删除预设', '将要删除“%s”预设，是否确认？' % (当前已选择的条目))
            if answer == QMessageBox.Yes:
                id = self.conn.cursor().execute(
                    '''select id from %s where name = '%s'; ''' % (presetTableName, 当前已选择的条目)).fetchone()[0]
                self.conn.cursor().execute("delete from %s where id = '%s'; " % (presetTableName, id))
                self.conn.cursor().execute("update %s set id=id-1 where id > %s" % (presetTableName, id))
                self.conn.commit()
                self.refreshList()
        except:
            QMessageBox.information(self, '删除失败', '还没有选择要删除的预设')

    # 向上移动预设
    def upwardButtonClicked(self):
        currentRow = self.预设列表.currentRow()
        if currentRow > 0:
            currentText = self.预设列表.currentItem().text()
            currentText = currentText.replace("'", "''")
            id = self.conn.cursor().execute(
                "select id from %s where name = '%s'" % (presetTableName, currentText)).fetchone()[0]
            self.conn.cursor().execute("update %s set id=10000 where id=%s-1 " % (presetTableName, id))
            self.conn.cursor().execute("update %s set id = id - 1 where name = '%s'" % (presetTableName, currentText))
            self.conn.cursor().execute("update %s set id=%s where id=10000 " % (presetTableName, id))
            self.conn.commit()
            self.refreshList()
            self.预设列表.setCurrentRow(currentRow - 1)

    # 向下移动预设
    def downwardButtonClicked(self):
        currentRow = self.预设列表.currentRow()
        totalRow = self.预设列表.count()
        if currentRow > -1 and currentRow < totalRow - 1:
            currentText = self.预设列表.currentItem().text()
            currentText = currentText.replace("'", "''")
            id = self.conn.cursor().execute(
                "select id from %s where name = '%s'" % (presetTableName, currentText)).fetchone()[0]
            self.conn.cursor().execute("update %s set id=10000 where id=%s+1 " % (presetTableName, id))
            self.conn.cursor().execute("update %s set id = id + 1 where name = '%s'" % (presetTableName, currentText))
            self.conn.cursor().execute("update %s set id=%s where id=10000 " % (presetTableName, id))
            self.conn.commit()
            self.refreshList()
            if currentRow < totalRow:
                self.预设列表.setCurrentRow(currentRow + 1)
            else:
                self.预设列表.setCurrentRow(currentRow)
        return

    # 看预设描述
    def checkPresetHelpButtonClicked(self):
        if self.预设列表.currentRow() > -1:
            dialog = QDialog()
            dialog.setWindowTitle('预设描述')
            dialog.resize(700, 600)
            textEdit = QTextEdit()
            layout = QHBoxLayout()
            layout.addWidget(textEdit)
            dialog.setLayout(layout)
            content = self.conn.cursor().execute("select description from %s where name = '%s'" % (
                presetTableName, self.预设列表.currentItem().text())).fetchone()[0]
            textEdit.setHtml(content)
            dialog.exec()

    # 添加预设对话框
    class SetupPresetItemDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.initUI()

        def initUI(self):
            self.setWindowTitle('添加或更新预设')
            self.conn = sqlite3.connect(dbname)

            # 预设名称
            if True:
                self.预设名称标签 = QLabel('预设名称：')
                self.预设名称输入框 = QLineEdit()
                self.预设名称输入框.textChanged.connect(self.presetNameEditChanged)

            # 输入1选项
            if True:
                self.输入1选项标签 = QLabel('输入1选项：')
                self.输入1选项输入框 = QLineEdit()

            # 输入2选项
            if True:
                self.输入2选项标签 = QLabel('输入2选项：')
                self.输入2选项输入框 = QLineEdit()

            # 输出选项
            if True:
                # 输出后缀名
                if True:
                    self.输出后缀标签 = QLabel('输出后缀名：')
                    self.输出后缀输入框 = QLineEdit()
                # 输出选项
                if True:
                    self.输出选项标签 = QLabel('输出选项：')
                    self.输出选项输入框 = QPlainTextEdit()
                    self.输出选项输入框.setMaximumHeight(70)

            # 额外代码
            if True:
                self.额外代码标签 = QLabel('额外代码：')
                self.额外代码输入框 = QPlainTextEdit()
                self.额外代码输入框.setMaximumHeight(70)
                self.额外代码输入框.setPlaceholderText('这里是用于实现一些比较复杂的预设的，普通用户不用管这个框')

            # 描述
            if True:
                self.描述标签 = QLabel('描述：')
                self.描述输入框 = QTextEdit()

            # 底部按钮
            if True:
                self.submitButton = QPushButton('确定')
                self.submitButton.clicked.connect(self.submitButtonClicked)
                self.cancelButton = QPushButton('取消')
                self.cancelButton.clicked.connect(lambda: self.close())

            # 各个区域组装起来
            if True:
                self.表格布局控件 = QWidget()
                self.表格布局 = QFormLayout()
                self.表格布局.addRow(self.预设名称标签, self.预设名称输入框)
                self.表格布局.addRow(self.输入1选项标签, self.输入1选项输入框)
                self.表格布局.addRow(self.输入2选项标签, self.输入2选项输入框)
                self.表格布局.addRow(self.输出后缀标签, self.输出后缀输入框)
                self.表格布局.addRow(self.输出选项标签, self.输出选项输入框)
                self.表格布局.addRow(self.额外代码标签, self.额外代码输入框)
                self.表格布局.addRow(self.描述标签, self.描述输入框)
                self.表格布局控件.setLayout(self.表格布局)

                self.按钮布局控件 = QWidget()
                self.按钮布局 = QHBoxLayout()

                self.按钮布局.addWidget(self.submitButton)

                self.按钮布局.addWidget(self.cancelButton)

                self.按钮布局控件.setLayout(self.按钮布局)

                self.主布局vbox = QVBoxLayout()
                self.主布局vbox.addWidget(self.表格布局控件)
                self.主布局vbox.addWidget(self.按钮布局控件)
            self.setLayout(self.主布局vbox)
            # self.submitButton.setFocus()

            # 查询数据库，填入输入框
            if True:
                global 当前已选择的条目
                try:
                    当前已选择的条目
                except:
                    当前已选择的条目 = None
                if 当前已选择的条目 != None:
                    presetData = self.conn.cursor().execute(
                        'select id, name, inputOneOption, inputTwoOption, outputExt, outputOption, extraCode, description from %s where name = "%s"' % (
                            presetTableName, 当前已选择的条目)).fetchone()
                    if presetData != None:
                        self.inputOneOption = presetData[2]
                        self.inputTwoOption = presetData[3]
                        self.outputExt = presetData[4]
                        self.outputOption = presetData[5]
                        self.extraCode = presetData[6]
                        self.description = presetData[7]

                        self.预设名称输入框.setText(当前已选择的条目)
                        if self.inputOneOption != None:
                            self.输入1选项输入框.setText(self.inputOneOption)
                        if self.inputTwoOption != None:
                            self.输入2选项输入框.setText(self.inputTwoOption)
                        if self.outputExt != None:
                            self.输出后缀输入框.setText(self.outputExt)
                        if self.outputOption != None:
                            self.输出选项输入框.setPlainText(self.outputOption)
                        if self.extraCode != None:
                            self.额外代码输入框.setPlainText(self.extraCode)
                        if self.description != None:
                            self.描述输入框.setHtml(self.description)

            # 根据刚开始预设名字是否为空，设置确定键可否使用
            if True:
                self.新预设名称 = self.预设名称输入框.text()
                if self.新预设名称 == '':
                    self.submitButton.setEnabled(False)

            self.exec()

        # 根据刚开始预设名字是否为空，设置确定键可否使用
        def presetNameEditChanged(self):
            self.新预设名称 = self.预设名称输入框.text()
            if self.新预设名称 == '':
                if self.submitButton.isEnabled():
                    self.submitButton.setEnabled(False)
            else:
                if not self.submitButton.isEnabled():
                    self.submitButton.setEnabled(True)

        # 点击提交按钮后, 添加预设
        def submitButtonClicked(self):
            self.新预设名称 = self.预设名称输入框.text()
            self.新预设名称 = self.新预设名称.replace("'", "''")

            self.新预设输入1选项 = self.输入1选项输入框.text()
            self.新预设输入1选项 = self.新预设输入1选项.replace("'", "''")

            self.新预设输入2选项 = self.输入2选项输入框.text()
            self.新预设输入2选项 = self.新预设输入2选项.replace("'", "''")

            self.新预设输出后缀 = self.输出后缀输入框.text()
            self.新预设输出后缀 = self.新预设输出后缀.replace("'", "''")

            self.新预设输出选项 = self.输出选项输入框.toPlainText()
            self.新预设输出选项 = self.新预设输出选项.replace("'", "''")

            self.新预设额外代码 = self.额外代码输入框.toPlainText()
            self.新预设额外代码 = self.新预设额外代码.replace("'", "''")

            self.新预设描述 = self.描述输入框.toHtml()
            self.新预设描述 = self.新预设描述.replace("'", "''")

            result = self.conn.cursor().execute(
                'select name from %s where name = "%s";' % (presetTableName, self.新预设名称)).fetchone()
            if result == None:
                try:
                    maxIdItem = self.conn.cursor().execute('select id from %s order by id desc' % presetTableName).fetchone()
                    if maxIdItem != None:
                        maxId = maxIdItem[0]
                    else:
                        maxId = 0
                    self.conn.cursor().execute(
                        '''insert into %s (id, name, inputOneOption, inputTwoOption, outputExt, outputOption, extraCode, description) values (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s');''' % (
                            presetTableName, maxId + 1,  self.新预设名称, self.新预设输入1选项, self.新预设输入2选项, self.新预设输出后缀, self.新预设输出选项,
                            self.新预设额外代码, self.新预设描述))
                    self.conn.commit()
                    QMessageBox.information(self, '添加预设', '新预设添加成功')
                    self.close()
                except:
                    QMessageBox.warning(self, '添加预设', '新预设添加失败，你可以把失败过程重新操作记录一遍，然后发给作者')
            else:
                answer = QMessageBox.question(self, '覆盖预设', '''已经存在名字相同的预设，你可以选择换一个预设名字或者覆盖旧的预设。是否要覆盖？''')
                if answer == QMessageBox.Yes:  # 如果同意覆盖
                    try:
                        self.conn.cursor().execute(
                            '''update %s set name = '%s', inputOneOption = '%s', inputTwoOption = '%s', outputExt = '%s', outputOption = '%s', extraCode = '%s', description = '%s' where name = '%s';''' % (
                                presetTableName, self.新预设名称, self.新预设输入1选项, self.新预设输入2选项, self.新预设输出后缀, self.新预设输出选项,
                                self.新预设额外代码, self.新预设描述, self.新预设名称))
                        print(
                            '''update %s set name = '%s', inputOneOption = '%s', inputTwoOption = '%s', outputExt = '%s', outputOption = '%s', extraCode = '%s', description = '%s' where name = '%s';''' % (
                                presetTableName, self.新预设名称, self.新预设输入1选项, self.新预设输入2选项, self.新预设输出后缀, self.新预设输出选项,
                                self.新预设额外代码, self.新预设描述, self.新预设名称))
                        self.conn.commit()
                        QMessageBox.information(self, '更新预设', '预设更新成功')
                        self.close()
                    except:
                        QMessageBox.warning(self, '更新预设', '预设更新失败，你可以把失败过程重新操作记录一遍，然后发给作者')

        def closeEvent(self, a0: QCloseEvent) -> None:
            try:
                self.conn.close()
                main.ffmpegMainTab.refreshList()
            except:
                pass

    # 点击会变化“截取时长”、 “截止时刻”的label
    class ClickableEndTimeLable(QLabel):
        def __init__(self):
            super().__init__()
            self.setText('截取时长：')

        def enterEvent(self, *args, **kwargs):
            main.status.showMessage('点击交换“截取时长”和“截止时刻”')

        def leaveEvent(self, *args, **kwargs):
            main.status.showMessage('')

        def mousePressEvent(self, QMouseEvent):
            # print(self.text())
            if self.text() == '截取时长：':
                self.setText('截止时刻：')
            else:
                self.setText('截取时长：')
            main.ffmpegMainTab.generateFinalCommand()

    # 点击会交换横竖分辨率的 label
    class ClickableResolutionTimesLable(QLabel):
        def __init__(self):
            # global main
            super().__init__()
            self.setText('×')
            self.setToolTip('点击交换横纵分辨率')
            # main.status.showMessage('1')

        def enterEvent(self, *args, **kwargs):
            main.status.showMessage('点击交换横竖分辨率')

        def leaveEvent(self, *args, **kwargs):
            main.status.showMessage('')

        def mousePressEvent(self, QMouseEvent):
            x = main.ffmpegMainTab.X轴分辨率输入框.text()
            main.ffmpegMainTab.X轴分辨率输入框.setText(main.ffmpegMainTab.Y轴分辨率输入框.text())
            main.ffmpegMainTab.Y轴分辨率输入框.setText(x)

    # 分辨率预设 dialog
    class ResolutionDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.resolutions = ['4096 x 2160 (Ultra HD 4k)', '2560 x 1440 (Quad HD 2k)', '1920 x 1080 (Full HD 1080p)',
                                '1280 x 720 (HD 720p)', '720 x 480 (480p)', '480 x 360 (360p)']
            self.setWindowTitle('选择分辨率预设')
            self.listWidget = QListWidget()
            self.listWidget.addItems(self.resolutions)
            self.listWidget.itemDoubleClicked.connect(self.setResolution)
            self.layout = QVBoxLayout()
            self.layout.addWidget(self.listWidget)
            self.setLayout(self.layout)
            self.exec()

        def setResolution(self):
            resolution = re.findall('\d+', self.listWidget.currentItem().text())
            main.ffmpegMainTab.X轴分辨率输入框.setText(resolution[0])
            main.ffmpegMainTab.Y轴分辨率输入框.setText(resolution[1])
            self.close()

    # 剪切时间的提示 QLineEdit
    class CutTimeEdit(QLineEdit):
        def __init__(self):
            super().__init__()
            self.setAlignment(Qt.AlignCenter)

        def enterEvent(self, *args, **kwargs):
            main.status.showMessage('例如 “00:05.00”、“23.189”、“12:03:45”的形式都是有效的，注意冒号是英文冒号')

        def leaveEvent(self, *args, **kwargs):
            main.status.showMessage('')

    # 分辨率的提示 QLineEdit
    class ResolutionEdit(QLineEdit):
        def __init__(self):
            super().__init__()
            self.setAlignment(Qt.AlignCenter)

        def enterEvent(self, *args, **kwargs):
            main.status.showMessage('负数表示自适应。例如，“ 720 × -2 ” 表示横轴分辨率为 720，纵轴分辨率为自适应且能够整除 -2')

        def leaveEvent(self, *args, **kwargs):
            main.status.showMessage('')


class FFmpegCutVideoTab(QWidget):
    def __init__(self):
        super().__init__()
        label = QLabel('还没想好怎么做，期待大神来支招')
        label.setAlignment(Qt.AlignCenter)
        hlayout = QHBoxLayout()
        hlayout.addWidget(label)
        self.setLayout(hlayout)


class FFmpegConcatTab(QWidget):
    def __init__(self):
        super().__init__()
        self.fileList = []
        self.initUI()

    def initUI(self):
        self.inputHintLabel = QLabel('点击列表右下边的加号添加要合并的视频片段：')
        self.fileListWidget = self.FileListWidget()  # 文件表控件
        self.fileListWidget.doubleClicked.connect(self.fileListWidgetDoubleClicked)
        # self.fileListWidget.setLineWidth(1)

        self.masterVLayout = QVBoxLayout()
        self.masterVLayout.addWidget(self.inputHintLabel)
        self.masterVLayout.addWidget(self.fileListWidget)

        self.buttonHLayout = QHBoxLayout()
        self.upButton = QPushButton('↑')
        self.upButton.clicked.connect(self.upButtonClicked)
        self.downButton = QPushButton('↓')
        self.downButton.clicked.connect(self.downButtonClicked)
        self.reverseButton = QPushButton('倒序')
        self.reverseButton.clicked.connect(self.reverseButtonClicked)
        self.addButton = QPushButton('+')
        self.addButton.clicked.connect(self.addButtonClicked)
        self.delButton = QPushButton('-')
        self.delButton.clicked.connect(self.delButtonClicked)
        self.buttonHLayout.addWidget(self.upButton)
        self.buttonHLayout.addWidget(self.downButton)
        self.buttonHLayout.addWidget(self.reverseButton)
        self.buttonHLayout.addWidget(self.addButton)
        self.buttonHLayout.addWidget(self.delButton)
        self.masterVLayout.addLayout(self.buttonHLayout)

        self.outputFileWidgetLayout = QHBoxLayout()
        self.outputHintLabel = QLabel('输出：')
        self.outputFileLineEdit = QLineEdit()
        self.outputFileSelectButton = QPushButton('选择保存位置')
        self.outputFileSelectButton.clicked.connect(self.outputFileSelectButtonClicked)
        self.outputFileWidgetLayout.addWidget(self.outputHintLabel)
        self.outputFileWidgetLayout.addWidget(self.outputFileLineEdit)
        self.outputFileWidgetLayout.addWidget(self.outputFileSelectButton)
        self.masterVLayout.addLayout(self.outputFileWidgetLayout)

        self.methodVLayout = QVBoxLayout()

        self.concatRadioButton = QRadioButton('concat格式衔接，不重新解码、编码（快、无损、要求格式一致）')
        self.tsRadioButton = QRadioButton('先转成 ts 格式，再衔接，要解码、编码（用于合并不同格式）')
        self.concatFilterVStream0RadioButton = QRadioButton('concat滤镜衔接（视频为Stream0），要解码、编码')
        self.concatFilterAStream0RadioButton = QRadioButton('concat滤镜衔接（音频为Stream0），要解码、编码')
        self.methodVLayout.addWidget(self.concatRadioButton)
        self.methodVLayout.addWidget(self.tsRadioButton)
        self.methodVLayout.addWidget(self.concatFilterVStream0RadioButton)
        self.methodVLayout.addWidget(self.concatFilterAStream0RadioButton)

        self.finalCommandBoxLayout = QVBoxLayout()
        self.finalCommandEditBox = QPlainTextEdit()
        self.finalCommandEditBox.setPlaceholderText('这里是自动生成的总命令')
        self.runCommandButton = QPushButton('运行')
        self.runCommandButton.clicked.connect(self.runCommandButtonClicked)
        self.finalCommandBoxLayout.addWidget(self.finalCommandEditBox)
        self.finalCommandBoxLayout.addWidget(self.runCommandButton)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.addLayout(self.methodVLayout)
        self.bottomLayout.addLayout(self.finalCommandBoxLayout)

        self.masterVLayout.addLayout(self.bottomLayout)
        self.setLayout(self.masterVLayout)

        self.refreshFileList()

        self.concatRadioButton.clicked.connect(lambda: self.concatMethodButtonClicked('concatFormat'))
        self.concatFilterVStream0RadioButton.clicked.connect(
            lambda: self.concatMethodButtonClicked('concatFilterVStreamFirst'))
        self.tsRadioButton.clicked.connect(lambda: self.concatMethodButtonClicked('tsConcat'))
        self.concatFilterAStream0RadioButton.clicked.connect(
            lambda: self.concatMethodButtonClicked('concatFilterAStreamFirst'))
        self.outputFileLineEdit.textChanged.connect(self.generateFinalCommand)
        self.concatRadioButton.setChecked(True)
        self.concatMethod = 'concatFormat'

    def refreshFileList(self):
        self.fileListWidget.clear()
        self.fileListWidget.addItems(self.fileList)
        self.generateFinalCommand()

    def concatMethodButtonClicked(self, method):
        self.concatMethod = method
        self.generateFinalCommand()

    def fileListWidgetDoubleClicked(self):
        print(True)
        result = QMessageBox.warning(self, '清空列表', '是否确认清空列表？', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if result == QMessageBox.Yes:
            self.fileList.clear()
            self.refreshFileList()

    def upButtonClicked(self):
        itemCurrentPosition = self.fileListWidget.currentRow()
        if itemCurrentPosition > 0:
            temp = self.fileList[itemCurrentPosition]
            self.fileList.insert(itemCurrentPosition - 1, temp)
            self.fileList.pop(itemCurrentPosition + 1)
            self.refreshFileList()
            self.fileListWidget.setCurrentRow(itemCurrentPosition - 1)

    def downButtonClicked(self):
        itemCurrentPosition = self.fileListWidget.currentRow()
        if itemCurrentPosition > -1 and itemCurrentPosition < len(self.fileList) - 1:
            temp = self.fileList[itemCurrentPosition]
            self.fileList.insert(itemCurrentPosition + 2, temp)
            self.fileList.pop(itemCurrentPosition)
            self.refreshFileList()
            self.fileListWidget.setCurrentRow(itemCurrentPosition + 1)

    def reverseButtonClicked(self):
        self.fileList.reverse()
        self.refreshFileList()

    def addButtonClicked(self):
        fileNames, _ = QFileDialog().getOpenFileNames(self, '添加音视频文件', None)
        if self.fileList == [] and fileNames != []:
            tempName = fileNames[0]
            tempNameParts = os.path.splitext(tempName)
            self.outputFileLineEdit.setText(tempNameParts[0] + 'out' + tempNameParts[1])
        self.fileList += fileNames
        self.refreshFileList()

    def delButtonClicked(self):
        currentPosition = self.fileListWidget.currentRow()
        if currentPosition > -1:
            self.fileList.pop(currentPosition)
            self.refreshFileList()
            if len(self.fileList) > 0:
                self.fileListWidget.setCurrentRow(currentPosition)

    def outputFileSelectButtonClicked(self):
        file, _ = QFileDialog.getSaveFileName(self, '选择保存位置', 'out.mp4')
        if file != '':
            self.outputFileLineEdit.setText(file)

    def generateFinalCommand(self):
        if self.fileList != []:
            finalCommand = ''
            if self.concatMethod == 'concatFormat':
                finalCommand = '''ffmpeg -y -hide_banner -vsync 0 -safe 0 -f concat -i "fileList.txt" -c copy "%s"''' % self.outputFileLineEdit.text()
                f = open('fileList.txt', 'w', encoding='utf-8')
                with f:
                    for i in self.fileList:
                        f.write(r'''file '%s'
''' % i)
            elif self.concatMethod == 'tsConcat':
                inputTsFiles = ''
                for i in self.fileList:
                    tsOutPath = os.path.splitext(i)[0] + '.ts'
                    finalCommand = finalCommand + '''ffmpeg -y -hide_banner -i "%s" -c copy -bsf:v h264_mp4toannexb -f mpegts "%s" && ''' % (
                        i, tsOutPath)
                    inputTsFiles = inputTsFiles + tsOutPath + '|'
                if inputTsFiles[-1] == '|':
                    inputTsFiles = inputTsFiles[0:-1]
                print(inputTsFiles)
                finalCommand += '''ffmpeg -hide_banner -y -i "concat:%s" -c copy -bsf:a aac_adtstoasc "%s"''' % (
                    inputTsFiles, self.outputFileLineEdit.text())
                pass
            elif self.concatMethod == 'concatFilterVStreamFirst':
                inputFiles = ''
                inputStreamIdentifiers = ''
                for i in range(len(self.fileList)):
                    inputFiles += '''-i "%s" ''' % self.fileList[i]
                    inputStreamIdentifiers += '''[%s:0][%s:1]''' % (i, i)
                finalCommand = '''ffmpeg -hide_banner -y %s -filter_complex "%sconcat=n=%s:v=1:a=1" "%s"''' % (
                    inputFiles, inputStreamIdentifiers, len(self.fileList), self.outputFileLineEdit.text())

            elif self.concatMethod == 'concatFilterAStreamFirst':
                inputFiles = ''
                inputStreamIdentifiers = ''
                for i in range(len(self.fileList)):
                    inputFiles += '''-i "%s" ''' % self.fileList[i]
                    inputStreamIdentifiers += '''[%s:1][%s:0]''' % (i, i)
                finalCommand = '''ffmpeg -hide_banner -y %s -filter_complex "%sconcat=n=%s:v=1:a=1" "%s"''' % (
                    inputFiles, inputStreamIdentifiers, len(self.fileList), self.outputFileLineEdit.text())
            self.finalCommandEditBox.setPlainText(finalCommand)
        else:
            self.finalCommandEditBox.clear()
            pass

    def runCommandButtonClicked(self):
        execute(self.finalCommandEditBox.toPlainText())

    class FileListWidget(QListWidget):
        def enterEvent(self, a0: QEvent) -> None:
            main.status.showMessage('双击列表项可以清空文件列表')

        def leaveEvent(self, a0: QEvent) -> None:
            main.status.showMessage('')


class FFmpegBurnCaptionTab(QWidget):
    def __init__(self):
        super().__init__()


class FFmpegAutoEditTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initGui()

    def initGui(self):
        self.masterLayout = QVBoxLayout()



        # 输入输出文件部分
        if True:
            self.inputOutputLayout = QGridLayout()
            self.inputHintLabel = QLabel('输入文件')
            self.outputHintLabel = QLabel('输出路径')
            self.inputLineEdit = QLineEdit()
            self.outputLineEdit = QLineEdit()
            self.chooseInputFileButton = QPushButton('选择文件')
            self.chooseInputFileButton.clicked.connect(self.chooseInputFileButtonClicked)
            self.chooseOutputFileButton = QPushButton('选择保存位置')
            self.chooseOutputFileButton.clicked.connect(self.chooseOutputFileButtonClicked)
            self.inputOutputLayout.addWidget(self.inputHintLabel, 0, 0, 1, 1)
            self.inputOutputLayout.addWidget(self.inputLineEdit, 0, 1, 1, 1)
            self.inputOutputLayout.addWidget(self.chooseInputFileButton, 0, 2, 1, 1)
            self.inputOutputLayout.addWidget(self.outputHintLabel, 1, 0, 1, 1)
            self.inputOutputLayout.addWidget(self.outputLineEdit, 1, 1, 1, 1)
            self.inputOutputLayout.addWidget(self.chooseOutputFileButton, 1, 2, 1, 1)

            self.masterLayout.addLayout(self.inputOutputLayout)

        # 一般选项
        if True:
            self.normalOptionLayout = QGridLayout()

            self.quietSpeedFactorLabel = QLabel('安静片段倍速：')
            self.silentSpeedFactorEdit = QDoubleSpinBox()
            self.silentSpeedFactorEdit.setAlignment(Qt.AlignCenter)
            self.silentSpeedFactorEdit.setValue(8)
            self.soundedSpeedFactorLabel = QLabel('响亮片段倍速：')
            self.soundedSpeedFactorEdit = QDoubleSpinBox()
            self.soundedSpeedFactorEdit.setAlignment(Qt.AlignCenter)
            self.soundedSpeedFactorEdit.setValue(1)
            self.frameMarginLabel = QLabel('片段间缓冲帧数：')
            self.frameMarginEdit = QSpinBox()
            self.frameMarginEdit.setAlignment(Qt.AlignCenter)
            self.frameMarginEdit.setValue(3)
            self.soundThresholdLabel = QLabel('声音检测相对阈值：')
            self.soundThresholdEdit = QDoubleSpinBox()
            self.soundThresholdEdit.setAlignment(Qt.AlignCenter)
            self.soundThresholdEdit.setDecimals(3)
            self.soundThresholdEdit.setSingleStep(0.005)
            self.soundThresholdEdit.setValue(0.025)

            # print(self.soundedSpeedFactorEdit.DefaultStepType)
            self.frameQualityLabel = QLabel('提取帧质量：')
            self.frameQualityEdit = QSpinBox()
            self.frameQualityEdit.setAlignment(Qt.AlignCenter)
            self.frameQualityEdit.setMinimum(1)
            self.frameQualityEdit.setValue(3)
            self.subtitleKeywordAutocutSwitch = QCheckBox('生成自动字幕并依据字幕中的关键句自动剪辑')
            self.subtitleKeywordAutocutSwitch.clicked.connect(self.subtitleKeywordAutocutSwitchClicked)

            self.subtitleEngineLabel = QLabel('字幕语音 API：')
            self.subtitleEngineComboBox = QComboBox()
            conn = sqlite3.connect(dbname)
            apis = conn.cursor().execute('select name from %s' % apiTableName).fetchall()
            if apis != None:
                for api in apis:
                    self.subtitleEngineComboBox.addItem(api[0])
                self.subtitleEngineComboBox.setCurrentIndex(0)
                pass
            self.cutKeywordLabel = QLabel('剪去片段关键句：')
            self.cutKeywordLineEdit = QLineEdit()
            self.cutKeywordLineEdit.setAlignment(Qt.AlignCenter)
            self.cutKeywordLineEdit.setText('切掉')
            self.saveKeywordLabel = QLabel('保留片段关键句：')
            self.saveKeywordLineEdit = QLineEdit()
            self.saveKeywordLineEdit.setAlignment(Qt.AlignCenter)
            self.saveKeywordLineEdit.setText('保留')


            self.subtitleEngineLabel.setEnabled(False)
            self.subtitleEngineComboBox.setEnabled(False)
            self.cutKeywordLabel.setEnabled(False)
            self.cutKeywordLineEdit.setEnabled(False)
            self.saveKeywordLabel.setEnabled(False)
            self.saveKeywordLineEdit.setEnabled(False)

            self.normalOptionLayout.addWidget(self.quietSpeedFactorLabel, 0, 0, 1, 1, Qt.AlignLeft)
            self.normalOptionLayout.addWidget(self.silentSpeedFactorEdit, 0, 1, 1, 1)
            self.normalOptionLayout.addWidget(QLabel('         '), 0, 2, 1, 1)
            self.normalOptionLayout.addWidget(self.soundedSpeedFactorLabel, 0, 3, 1, 1, Qt.AlignLeft)
            self.normalOptionLayout.addWidget(self.soundedSpeedFactorEdit, 0, 4, 1, 1)

            self.normalOptionLayout.addWidget(self.frameMarginLabel, 1, 0, 1, 1, Qt.AlignLeft)
            self.normalOptionLayout.addWidget(self.frameMarginEdit, 1, 1, 1, 1)
            self.normalOptionLayout.addWidget(self.soundThresholdLabel, 1, 3, 1, 1, Qt.AlignLeft)
            self.normalOptionLayout.addWidget(self.soundThresholdEdit, 1, 4, 1, 1)

            self.normalOptionLayout.addWidget(self.frameQualityLabel, 2, 0, 1, 1, Qt.AlignLeft)
            self.normalOptionLayout.addWidget(self.frameQualityEdit, 2, 1, 1, 1)
            self.normalOptionLayout.addWidget(self.subtitleKeywordAutocutSwitch, 2, 3, 1, 2, Qt.AlignLeft)

            self.normalOptionLayout.addWidget(self.subtitleEngineLabel, 3, 0, 1, 1, Qt.AlignLeft)
            self.normalOptionLayout.addWidget(self.subtitleEngineComboBox, 3, 1, 1, 4)

            self.normalOptionLayout.addWidget(self.cutKeywordLabel, 4, 0, 1, 1)
            self.normalOptionLayout.addWidget(self.cutKeywordLineEdit, 4, 1, 1, 1)
            self.normalOptionLayout.addWidget(self.saveKeywordLabel, 4, 3, 1, 1)
            self.normalOptionLayout.addWidget(self.saveKeywordLineEdit, 4, 4, 1, 1)

            # self.normalOptionLayout.addWidget(self.soundThresholdLabel, 1, 3, 1, 1, Qt.AlignLeft)
            # self.normalOptionLayout.addWidget(self.soundThresholdEdit, 1, 4, 1, 1)

            self.masterLayout.addLayout(self.normalOptionLayout)


        # 运行按钮
        if True:
            self.bottomButtonLayout = QHBoxLayout()
            self.runButton = QPushButton('运行')
            self.runButton.clicked.connect(self.runButtonClicked)
            self.bottomButtonLayout.addWidget(self.runButton)
            self.masterLayout.addLayout(self.bottomButtonLayout)

        # 提示
        # if True:
        #     self.helpButton = QPushButton('查看本工具帮助')
        #     self.masterLayout.addWidget(self.helpButton)

        self.setLayout(self.masterLayout)

    def chooseInputFileButtonClicked(self):
        filename = QFileDialog().getOpenFileName(self, '打开文件', None, '所有文件(*)')
        if filename[0] != '':
            self.inputLineEdit.setText(filename[0])
            outputName = re.sub(r'(\.[^\.]+)$', r'_out\1', filename[0])
            self.outputLineEdit.setText(outputName)
        return True

    def chooseOutputFileButtonClicked(self):
        filename = QFileDialog().getSaveFileName(self, '设置输出保存的文件名', '输出视频.mp4', '所有文件(*)')
        self.outputLineEdit.setText(filename[0])
        return True

    def subtitleKeywordAutocutSwitchClicked(self):
        if self.subtitleKeywordAutocutSwitch.isChecked() == 0:
            self.subtitleEngineLabel.setEnabled(False)
            self.subtitleEngineComboBox.setEnabled(False)
            self.cutKeywordLabel.setEnabled(False)
            self.cutKeywordLineEdit.setEnabled(False)
            self.saveKeywordLabel.setEnabled(False)
            self.saveKeywordLineEdit.setEnabled(False)
        else:
            self.subtitleEngineLabel.setEnabled(True)
            self.subtitleEngineComboBox.setEnabled(True)
            self.cutKeywordLabel.setEnabled(True)
            self.cutKeywordLineEdit.setEnabled(True)
            self.saveKeywordLabel.setEnabled(True)
            self.saveKeywordLineEdit.setEnabled(True)

    def runButtonClicked(self):
        if self.inputLineEdit.text() != '' and self.outputLineEdit.text() != '':
            window = Console(main)

            output = window.consoleBox

            thread = AutoEditThread(main)
            thread.output = output
            thread.inputFile = self.inputLineEdit.text()
            thread.outputFile = self.outputLineEdit.text()
            thread.silentSpeed = self.silentSpeedFactorEdit.value()
            thread.soundedSpeed = self.soundedSpeedFactorEdit.value()
            thread.frameMargin = self.frameMarginEdit.value()
            thread.silentThreshold = self.soundThresholdEdit.value()
            thread.frameQuality = self.frameQualityEdit.value()
            thread.whetherToUseOnlineSubtitleKeywordAutoCut = self.subtitleKeywordAutocutSwitch.isChecked()
            thread.apiEngine = self.subtitleEngineComboBox.currentText()
            thread.cutKeyword = self.cutKeywordLineEdit.text()
            thread.saveKeyword = self.saveKeywordLineEdit.text()

            thread.signal.connect(output.print)

            window.thread = thread # 把这里的剪辑子进程赋值给新窗口，这样新窗口就可以在关闭的时候也把进程退出

            thread.start()


class FFmpegAutoSrtTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initGui()
    def initGui(self):
        self.masterLayout = QVBoxLayout()

        self.widgetLayout = QGridLayout()


        self.inputHint = QLabel('输入文件：')
        self.inputEdit = QLineEdit()
        self.inputButton = QPushButton('选择文件')
        self.inputButton.clicked.connect(self.inputButtonClicked)

        self.outputHint = QLabel('字幕输出文件：')
        self.outputEdit = QLineEdit()
        self.outputEdit.setReadOnly(True)

        self.subtitleEngineLabel = QLabel('字幕语音 API：')
        self.subtitleEngineComboBox = QComboBox()
        conn = sqlite3.connect(dbname)
        apis = conn.cursor().execute('select name from %s' % apiTableName).fetchall()
        if apis != None:
            for api in apis:
                self.subtitleEngineComboBox.addItem(api[0])
            self.subtitleEngineComboBox.setCurrentIndex(0)
            pass

        self.runButton = QPushButton('开始运行')
        self.runButton.clicked.connect(self.runButtonClicked)

        self.widgetLayout.addWidget(self.inputHint, 0, 0, 1, 1)
        self.widgetLayout.addWidget(self.inputEdit, 0, 1, 1, 1)
        self.widgetLayout.addWidget(self.inputButton, 0, 2, 1, 1)


        self.widgetLayout.addWidget(self.outputHint, 1, 0, 1, 1)
        self.widgetLayout.addWidget(self.outputEdit, 1, 1, 1, 2)

        self.widgetLayout.addWidget(self.subtitleEngineLabel, 2, 0, 1, 1)
        self.widgetLayout.addWidget(self.subtitleEngineComboBox, 2, 1, 1, 2)

        self.widgetLayout.addWidget(QLabel('   '), 3, 0, 1, 3)
        self.widgetLayout.addWidget(self.runButton, 4, 0, 1, 3)


        self.masterLayout.addLayout(self.widgetLayout)
        self.masterLayout.addStretch(0)

        self.setLayout(self.masterLayout)

    def inputButtonClicked(self):
        filename = QFileDialog().getOpenFileName(self, '打开文件', None, '所有文件(*)')
        if filename[0] != '':
            self.inputEdit.setText(filename[0])
            self.outputName = os.path.splitext(filename[0])[0] + '.srt'
            self.outputEdit.setText(self.outputName)
        return True

    def runButtonClicked(self):

        conn = sqlite3.connect(dbname)

        ossData = conn.cursor().execute(
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

        apiData = conn.cursor().execute(
            '''select provider, appKey, language, accessKeyId, accessKeySecret from %s where name = '%s';''' % (
                apiTableName, self.apiEngine)).fetchone()

        apiProvider, apiappKey, apiLanguage, apiAccessKeyId, apiAccessKeySecret = apiData[0], apiData[1], apiData[
            2], apiData[3], apiData[4]

        if apiProvider == 'Alibaba':
            transEngine = AliTrans()
        elif apiProvider == 'Tencent':
            transEngine = TencentTrans()
        transEngine.setupApi(apiappKey, apiLanguage, apiAccessKeyId, apiAccessKeySecret)

        srtSubtitleFile = transEngine.mediaToSrt(self.output, oss, self.inputFile)






class ApiConfigTab(QWidget):
    def __init__(self):
        super().__init__()
        self.createDB()
        self.initGui()

    def initGui(self):

        self.masterLayout = QVBoxLayout()
        self.masterLayout.addSpacing(30)

        # 对象存储部分
        if True:
            self.ossConfigBoxLayout = QVBoxLayout()
            self.masterLayout.addLayout(self.ossConfigBoxLayout)
            self.ossHintLabel = QLabel('OSS对象存储设置：')
            self.ossConfigBoxLayout.addWidget(self.ossHintLabel)
            self.ossProviderBoxLayout = QHBoxLayout()
            self.ossConfigBoxLayout.addLayout(self.ossProviderBoxLayout)
            self.ossAliProviderRadioButton = QRadioButton('阿里OSS')
            self.ossTencentProviderRadioButton = QRadioButton('腾讯OSS')
            self.ossProviderBoxLayout.addWidget(self.ossAliProviderRadioButton)
            self.ossProviderBoxLayout.addWidget(self.ossTencentProviderRadioButton)

            self.ossConfigFormLayout = QFormLayout()
            self.endPointLineEdit = QLineEdit()
            self.bucketNameLineEdit = QLineEdit()
            self.accessKeyIdLineEdit = QLineEdit()
            self.accessKeyIdLineEdit.setEchoMode(QLineEdit.Password)
            self.accessKeySecretLineEdit = QLineEdit()
            self.accessKeySecretLineEdit.setEchoMode(QLineEdit.Password)
            self.ossConfigFormLayout.addRow('EndPoint：', self.endPointLineEdit)
            self.ossConfigFormLayout.addRow('BucketName：', self.bucketNameLineEdit)
            self.ossConfigFormLayout.addRow('AccessKeyID：', self.accessKeyIdLineEdit)
            self.ossConfigFormLayout.addRow('AccessKeySecret：', self.accessKeySecretLineEdit)
            self.ossConfigBoxLayout.addLayout(self.ossConfigFormLayout)

            self.getOssData()

            self.saveOssConfigButton = QPushButton('保存OSS配置')
            self.saveOssConfigButton.clicked.connect(self.saveOssData)
            self.cancelOssConfigButton = QPushButton('取消')
            self.cancelOssConfigButton.clicked.connect(self.getOssData)
            self.ossConfigButtonLayout = QHBoxLayout()
            self.ossConfigButtonLayout.addWidget(self.saveOssConfigButton)
            self.ossConfigButtonLayout.addWidget(self.cancelOssConfigButton)
            self.ossConfigBoxLayout.addLayout(self.ossConfigButtonLayout)

        self.masterLayout.addSpacing(15)

        # 语音api部分
        if True:
            self.apiBoxLayout = QVBoxLayout()
            self.masterLayout.addLayout(self.apiBoxLayout)

            self.appKeyHintLabel = QLabel('语音 Api：')
            self.apiBoxLayout.addWidget(self.appKeyHintLabel)
            # self.apiBoxLayout.addStretch(0)

            self.db = QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(dbname)
            self.model = QSqlTableModel()  # api 表的模型
            self.delrow = -1
            self.model.setTable(apiTableName)
            self.model.setEditStrategy(QSqlTableModel.OnRowChange)
            self.model.select()
            self.model.setHeaderData(0, Qt.Horizontal, 'id')
            self.model.setHeaderData(1, Qt.Horizontal, '引擎名称')
            self.model.setHeaderData(2, Qt.Horizontal, '服务商')
            self.model.setHeaderData(3, Qt.Horizontal, 'AppKey')
            self.model.setHeaderData(4, Qt.Horizontal, '语言')
            self.model.setHeaderData(5, Qt.Horizontal, 'AccessKeyId')
            self.model.setHeaderData(6, Qt.Horizontal, 'AccessKeySecret')
            self.apiTableView = QTableView()
            self.apiTableView.setModel(self.model)
            self.apiTableView.hideColumn(0)
            self.apiTableView.hideColumn(5)
            self.apiTableView.hideColumn(6)
            self.apiTableView.setColumnWidth(1, 150)
            self.apiTableView.setColumnWidth(2, 100)
            self.apiTableView.setColumnWidth(3, 150)
            self.apiTableView.setColumnWidth(4, 200)
            self.apiTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.apiTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
            # self.apiTableView.setsize(600)
            self.apiBoxLayout.addWidget(self.apiTableView)
            # self.apiBoxLayout.addStretch(0)

            self.appKeyControlButtonLayout = QHBoxLayout()
            self.upApiButton = QPushButton('↑')
            self.upApiButton.clicked.connect(self.upApiButtonClicked)
            self.downApiButton = QPushButton('↓')
            self.downApiButton.clicked.connect(self.downApiButtonClicked)
            self.addApiButton = QPushButton('+')
            self.addApiButton.clicked.connect(self.addApiButtonClicked)
            self.delApiButton = QPushButton('-')
            self.delApiButton.clicked.connect(self.delApiButtonClicked)
            self.appKeyControlButtonLayout.addWidget(self.upApiButton)
            self.appKeyControlButtonLayout.addWidget(self.downApiButton)
            self.appKeyControlButtonLayout.addWidget(self.addApiButton)
            self.appKeyControlButtonLayout.addWidget(self.delApiButton)
            self.apiBoxLayout.addLayout(self.appKeyControlButtonLayout)
            # self.apiBoxLayout.addStretch(0)

        self.setLayout(self.masterLayout)


    def findRow(self, i):
        self.delrow = i.row()

    def createDB(self):
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
        result = cursor.execute('select * from sqlite_master where name = "%s";' % (ossTableName))
        # 将oss初始预设写入数据库
        if result.fetchone() == None:
            cursor.execute('''create table %s (
                                        id integer primary key autoincrement,
                                        provider text, 
                                        endPoint text, 
                                        bucketName text, 
                                        bucketDomain text,
                                        accessKeyId text, 
                                        accessKeySecret text)''' % ossTableName)
        else:
            print('oss 表单已存在')
        result = cursor.execute('select * from sqlite_master where name = "%s";' % (apiTableName))
        # 将api初始预设写入数据库
        if result.fetchone() == None:
            cursor.execute('''create table %s (
                                        id integer primary key autoincrement,
                                        name text, 
                                        provider text, 
                                        appKey text, 
                                        language text, 
                                        accessKeyId text, 
                                        accessKeySecret text
                                        )''' % apiTableName)
        else:
            print('api 表单已存在')
        conn.commit()
        conn.close()

    def getOssData(self):
        conn = sqlite3.connect(dbname)
        ossData = conn.cursor().execute(
            '''select provider, endPoint, bucketName, accessKeyId, accessKeySecret from %s''' % ossTableName).fetchone()
        if ossData != None:
            if ossData[0] == 'Alibaba':
                self.ossAliProviderRadioButton.setChecked(True)
            elif ossData[0] == 'Tencent':
                self.ossTencentProviderRadioButton.setChecked(True)
            self.endPointLineEdit.setText(ossData[1])
            self.bucketNameLineEdit.setText(ossData[2])
            self.accessKeyIdLineEdit.setText(ossData[3])
            self.accessKeySecretLineEdit.setText(ossData[4])
        conn.close()

    def saveOssData(self):
        conn = sqlite3.connect(dbname)
        ossData = conn.cursor().execute(
            '''select provider, endPoint, bucketName, bucketDomain, accessKeyId, accessKeySecret from %s''' % ossTableName).fetchone()
        provider = ''
        if self.ossAliProviderRadioButton.isChecked():
            provider = 'Alibaba'
        elif self.ossTencentProviderRadioButton.isChecked():
            provider = 'Tencent'
        if ossData == None:
            print('新建oss item')
            conn.cursor().execute(
                '''insert into %s (provider, endPoint, bucketName, accessKeyId, accessKeySecret) values ( '%s', '%s', '%s', '%s', '%s')''' % (
                    ossTableName, provider, self.endPointLineEdit.text(), self.bucketNameLineEdit.text(),
                    self.accessKeyIdLineEdit.text(),
                    self.accessKeySecretLineEdit.text()))
        else:
            print('更新oss item')
            conn.cursor().execute(
                '''update %s set provider='%s', endPoint='%s', bucketName='%s', accessKeyId='%s', accessKeySecret='%s' where id=1 ''' % (
                    ossTableName, provider, self.endPointLineEdit.text(), self.bucketNameLineEdit.text(),
                    self.accessKeyIdLineEdit.text(),
                    self.accessKeySecretLineEdit.text()))
        conn.commit()
        conn.close()

    def addApiButtonClicked(self):
        dialog = self.AddApiDialog()

    def delApiButtonClicked(self):
        self.conn = sqlite3.connect(dbname)
        currentRow = main.apiConfigTab.apiTableView.currentIndex().row()
        print(currentRow)
        if currentRow > -1:
            try:
                answer = QMessageBox.question(self, '删除 Api', '将要删除选中的 Api，是否确认？')
                if answer == QMessageBox.Yes:
                    self.conn.cursor().execute("delete from %s where id = %s; " % (apiTableName, currentRow + 1))
                    self.conn.cursor().execute("update %s set id=id-1 where id > %s" % (apiTableName, currentRow + 1))
                    self.conn.commit()
            except:
                QMessageBox.information(self, '删除失败', '删除失败')
            self.model.select()

    def upApiButtonClicked(self):
        self.conn = sqlite3.connect(dbname)
        currentRow = self.apiTableView.currentIndex().row()
        if currentRow > 0:
            self.conn.cursor().execute("update %s set id=10000 where id=%s-1 " % (apiTableName, currentRow + 1))
            self.conn.cursor().execute("update %s set id = id - 1 where id = %s" % (apiTableName, currentRow + 1))
            self.conn.cursor().execute("update %s set id=%s where id=10000 " % (apiTableName, currentRow + 1))
            self.conn.commit()
            self.model.select()
            self.apiTableView.selectRow(currentRow - 1)
        self.conn.close()

    def downApiButtonClicked(self):
        self.conn = sqlite3.connect(dbname)
        currentRow = self.apiTableView.currentIndex().row()
        rowCount = self.model.rowCount()
        print(currentRow)
        if currentRow > -1 and currentRow < rowCount - 1:
            print(True)
            self.conn.cursor().execute("update %s set id=10000 where id=%s+1 " % (apiTableName, currentRow + 1))
            self.conn.cursor().execute("update %s set id = id + 1 where id = %s" % (apiTableName, currentRow + 1))
            self.conn.cursor().execute("update %s set id=%s where id=10000 " % (apiTableName, currentRow + 1))
            self.conn.commit()
            self.model.select()
            self.apiTableView.selectRow(currentRow + 1)
        self.conn.close()

    class AddApiDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.initUI()

        def initUI(self):
            self.setWindowTitle('添加或更新 Api')
            self.conn = sqlite3.connect(dbname)

            # 各个输入框
            if True:
                if True:
                    self.引擎名称标签 = QLabel('引擎名字：')
                    self.引擎名称编辑框 = QLineEdit()
                    self.引擎名称编辑框.setPlaceholderText('例如：阿里-中文')

                if True:
                    self.服务商标签 = QLabel('服务商：')
                    self.服务商选择框 = QComboBox()
                    self.服务商选择框.addItems(['Alibaba', 'Tencent'])
                    self.服务商选择框.setCurrentText('Alibaba')

                if True:
                    self.appKey标签 = QLabel('AppKey：')
                    self.appKey输入框 = QLineEdit()

                if True:
                    self.语言标签 = QLabel('语言：')
                    self.语言Combobox = QComboBox()
                    self.configLanguageCombobox()
                    self.服务商选择框.currentTextChanged.connect(self.configLanguageCombobox)


                if True:
                    self.accessKeyId标签 = QLabel('AccessKeyId：')
                    self.accessKeyId输入框 = QLineEdit()

                if True:
                    self.AccessKeySecret标签 = QLabel('AccessKeySecret：')
                    self.AccessKeySecret输入框 = QLineEdit()

                currentRow = main.apiConfigTab.apiTableView.currentIndex().row()
                if currentRow > -1:
                    currentApiItem = self.conn.cursor().execute('''select name, provider, appKey, language, accessKeyId, accessKeySecret from %s where id = %s''' % (apiTableName, currentRow + 1)).fetchone()
                    if currentApiItem != None:
                        self.引擎名称编辑框.setText(currentApiItem[0])
                        self.服务商选择框.setCurrentText(currentApiItem[1])
                        self.appKey输入框.setText(currentApiItem[2])
                        self.语言Combobox.setCurrentText(currentApiItem[3])
                        self.accessKeyId输入框.setText(currentApiItem[4])
                        self.AccessKeySecret输入框.setText(currentApiItem[5])
                        pass

            # 底部按钮
            if True:
                self.submitButton = QPushButton('确定')
                self.submitButton.clicked.connect(self.submitButtonClicked)
                self.cancelButton = QPushButton('取消')
                self.cancelButton.clicked.connect(lambda: self.close())

            # 各个区域组装起来
            if True:
                self.表格布局控件 = QWidget()
                self.表格布局 = QFormLayout()
                self.表格布局控件.setLayout(self.表格布局)
                self.表格布局.addRow(self.引擎名称标签, self.引擎名称编辑框)
                self.表格布局.addRow(self.服务商标签, self.服务商选择框)
                self.表格布局.addRow(self.appKey标签, self.appKey输入框)
                self.表格布局.addRow(self.语言标签, self.语言Combobox)
                self.表格布局.addRow(self.accessKeyId标签, self.accessKeyId输入框)
                self.表格布局.addRow(self.AccessKeySecret标签, self.AccessKeySecret输入框)

                self.按钮布局控件 = QWidget()
                self.按钮布局 = QHBoxLayout()

                self.按钮布局.addWidget(self.submitButton)
                self.按钮布局.addWidget(self.cancelButton)
                self.按钮布局控件.setLayout(self.按钮布局)

                self.主布局vbox = QVBoxLayout()
                self.主布局vbox.addWidget(self.表格布局控件)
                self.主布局vbox.addWidget(self.按钮布局控件)

            self.setLayout(self.主布局vbox)

            # 根据是否有名字决定是否将确定按钮取消可用
            self.engineNameChanged()
            self.引擎名称编辑框.textChanged.connect(self.engineNameChanged)

            self.exec()

        def configLanguageCombobox(self):
            if self.服务商选择框.currentText() == 'Alibaba':
                self.语言Combobox.clear()
                self.语言Combobox.addItem('由 Api 的云端配置决定')
                self.语言Combobox.setCurrentText('由 Api 的云端配置决定')
                self.语言Combobox.setEnabled(False)
                self.appKey输入框.setEnabled(True)
                self.accessKeyId标签.setText('AccessKeyId：')
                self.AccessKeySecret标签.setText('AccessKeySecret：')
            elif self.服务商选择框.currentText() == 'Tencent':
                self.语言Combobox.clear()
                self.语言Combobox.addItems(['中文普通话', '英语', '粤语'])
                self.语言Combobox.setCurrentText('中文普通话')
                self.语言Combobox.setEnabled(True)
                self.appKey输入框.setEnabled(False)
                self.accessKeyId标签.setText('AccessSecretId：')
                self.AccessKeySecret标签.setText('AccessSecretKey：')
        # 根据引擎名称是否为空，设置确定键可否使用
        def engineNameChanged(self):
            self.引擎名称 = self.引擎名称编辑框.text()
            if self.引擎名称 == '':
                if self.submitButton.isEnabled():
                    self.submitButton.setEnabled(False)
            else:
                if not self.submitButton.isEnabled():
                    self.submitButton.setEnabled(True)

        # 点击提交按钮后, 添加预设
        def submitButtonClicked(self):
            self.引擎名称 = self.引擎名称编辑框.text()
            self.引擎名称 = self.引擎名称.replace("'", "''")

            self.服务商 = self.服务商选择框.currentText()
            self.服务商 = self.服务商.replace("'", "''")

            self.appKey = self.appKey输入框.text()
            self.appKey = self.appKey.replace("'", "''")

            self.language = self.语言Combobox.currentText()
            self.language = self.language.replace("'", "''")

            self.accessKeyId = self.accessKeyId输入框.text()
            self.accessKeyId = self.accessKeyId.replace("'", "''")

            self.AccessKeySecret = self.AccessKeySecret输入框.text()
            self.AccessKeySecret = self.AccessKeySecret.replace("'", "''")

            # currentApiItem = self.conn.cursor().execute(
            #     '''select name, provider, appKey, accessKeyId, accessKeySecret from %s where id = %s''' % (
            #     apiTableName, currentRow + 1)).fetchone()
            # if currentApiItem != None:

            result = self.conn.cursor().execute(
                '''select name, provider, appKey, language, accessKeyId, accessKeySecret from %s where name = '%s' ''' % (apiTableName, self.引擎名称.replace("'", "''"))).fetchone()
            if result == None:
                try:
                    maxIdRow = self.conn.cursor().execute(
                        '''select id from %s order by id desc;''' % apiTableName).fetchone()
                    if maxIdRow != None:
                        maxId = maxIdRow[0]
                        self.conn.cursor().execute(
                            '''insert into %s (id, name, provider, appKey, language, accessKeyId, accessKeySecret) values (%s, '%s', '%s', '%s', '%s', '%s', '%s');''' % (
                                apiTableName, maxId + 1, self.引擎名称.replace("'", "''"), self.服务商.replace("'", "''"), self.appKey.replace("'", "''"), self.language.replace("'", "''"), self.accessKeyId.replace("'", "''"), self.AccessKeySecret.replace("'", "''")))
                    else:
                        maxId = 0
                        print(
                            '''insert into %s (id, name, provider, appKey, language, accessKeyId, accessKeySecret) values (%s, '%s', '%s', '%s', '%s', '%s', '%s');''' % (
                                apiTableName, maxId + 1, self.引擎名称.replace("'", "''"), self.服务商.replace("'", "''"),
                                self.appKey.replace("'", "''"), self.language.replace("'", "''"), self.accessKeyId.replace("'", "''"),
                                self.AccessKeySecret.replace("'", "''")))
                        self.conn.cursor().execute(
                            '''insert into %s (id, name, provider, appKey, language, accessKeyId, accessKeySecret) values (%s, '%s', '%s', '%s', '%s', '%s', '%s');''' % (
                                apiTableName, maxId + 1, self.引擎名称.replace("'", "''"), self.服务商.replace("'", "''"),
                                self.appKey.replace("'", "''"), self.language.replace("'", "''"), self.accessKeyId.replace("'", "''"),
                                self.AccessKeySecret.replace("'", "''")))
                    self.conn.commit()
                    self.close()
                except:
                    QMessageBox.warning(self, '添加Api', '新Api添加失败，你可以把失败过程重新操作记录一遍，然后发给作者')
            else:
                answer = QMessageBox.question(self, '覆盖Api', '''已经存在名字相同的Api，你可以选择换一个Api名称或者覆盖旧的Api。是否要覆盖？''')
                if answer == QMessageBox.Yes:  # 如果同意覆盖
                    try:
                        self.conn.cursor().execute(
                            '''update %s set name = '%s', provider = '%s', appKey = '%s', language = '%s', accessKeyId = '%s', accessKeySecret = '%s' where name = '%s';''' % (
                                apiTableName, self.引擎名称.replace("'", "''"), self.服务商.replace("'", "''"), self.appKey.replace("'", "''"), self.language.replace("'", "''"), self.accessKeyId.replace("'", "''"), self.AccessKeySecret.replace("'", "''"), self.引擎名称.replace("'", "''")))
                        self.conn.commit()
                        QMessageBox.information(self, '更新Api', 'Api更新成功')
                        self.close()
                    except:
                        QMessageBox.warning(self, '更新Api', 'Api更新失败，你可以把失败过程重新操作记录一遍，然后发给作者')
            main.apiConfigTab.model.select()

        def closeEvent(self, a0: QCloseEvent) -> None:
            try:
                self.conn.close()
                # main.ffmpegMainTab.refreshList()
            except:
                pass


class ConsoleTab(QTableWidget):
    def __init__(self):
        super().__init__()
        self.initGui()
    def initGui(self):
        self.layout = QVBoxLayout()
        self.consoleEditBox = QTextEdit(self, readOnly=True)
        self.layout.addWidget(self.consoleEditBox)
        self.setLayout(self.layout)


class HelpTab(QWidget):
    def __init__(self):
        super().__init__()


class AboutTab(QWidget):
    def __init__(self):
        super().__init__()


class Stream(QObject):
    # 用于将控制台的输出定向到一个槽
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))
        QApplication.processEvents()


class Console(QMainWindow):
    # 这个 console 是个子窗口，调用的时候要指定父窗口。例如：window = Console(main)
    # 里面包含一个 OutputBox, 可以将信号导到它的 print 方法。
    thread = None
    def __init__(self, parent=None):
        super(Console, self).__init__(parent)
        self.initGui()
    def initGui(self):
        self.setWindowTitle('命令运行输出窗口')
        self.resize(1100, 700)
        self.consoleBox = OutputBox()
        self.setCentralWidget(self.consoleBox)
        self.show()
    def closeEvent(self, a0: QCloseEvent) -> None:
        try:
            self.thread.exit()
        except:
            pass


class OutputBox(QTextEdit):
    # 定义一个 QTextEdit 类，写入 print 方法。用于输出显示。
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
    def print(self, text):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text + '\n')
        self.setTextCursor(cursor)
        self.ensureCursorVisible()


class CommandThread(QThread):
    signal = pyqtSignal(str)

    output = None # 用于显示输出的控件，如一个 QEditBox，它需要有自定义的 print 方法。

    command = None

    def __init__(self, parent=None):
        super(CommandThread, self).__init__(parent)

    def print(self, text):
        self.signal.emit(text)

    def run(self):
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            self.print(line)
        self.print('\n\n\n命令执行完毕\n\n\n')


class AutoEditThread(QThread):
    signal = pyqtSignal(str)

    output = None # 用于显示输出的控件，如一个 QEditBox，它需要有自定义的 print 方法。

    inputFile = ''
    outputFile = ''
    silentSpeed = 1
    soundedSpeed = 2
    frameMargin = 3
    silentThreshold = 0.025
    frameQuality = 3
    whetherToUseOnlineSubtitleKeywordAutoCut = False
    apiEngine = ''
    cutKeyword = ''
    saveKeyword = ''
    ffmpegOutputOption = ''

    TEMP_FOLDER = 'TEMP'

    def __init__(self, parent=None):
        super(AutoEditThread, self).__init__(parent)

    def print(self, text):
        self.signal.emit(text)

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
            self.print("删除临时文件夹 %s 失败" % s)
            self.print(OSError)

    def getMaxVolume(self, s):
        maxv = float(np.max(s))
        minv = float(np.min(s))
        return max(maxv, -minv)

    # 复制文件，返回一个保存成功的信息(每50帧提示一次)
    def copyFrame(self, inputFrame, outputFrame):
        src = self.TEMP_FOLDER + "/frame{:06d}".format(inputFrame + 1) + ".jpg"
        dst = self.TEMP_FOLDER + "/newFrame{:06d}".format(outputFrame + 1) + ".jpg"
        if not os.path.isfile(str(src)):
            return False
        if outputFrame % 20 == 19:
            self.print(str(outputFrame + 1) + " 帧画面被记录")
        move(src, dst)
        return True

    def run(self):
        # 定义剪切、保留片段的关键词
        key_word = [self.cutKeyword, self.saveKeyword]

        NEW_SPEED = [self.silentSpeed, self.soundedSpeed]

        # 音频淡入淡出大小，使声音在不同片段之间平滑
        AUDIO_FADE_ENVELOPE_SIZE = 400  # smooth out transitiion's audio by quickly fading in/out (arbitrary magic number whatever)

        # 如果临时文件已经存在，就删掉
        if (os.path.exists(self.TEMP_FOLDER)):
            self.deletePath(self.TEMP_FOLDER)
        # test if the TEMP folder exists, when it does, delete it. Prevent the error when creating TEMP while the TEMP already exists

        # 创建临时文件夹
        self.createPath(self.TEMP_FOLDER)
        self.print('新建临时文件夹：%s \n' % self.TEMP_FOLDER)

        # 如果要用在线转字幕
        # oss 和 api 配置
        if self.whetherToUseOnlineSubtitleKeywordAutoCut:

            conn = sqlite3.connect(dbname)

            ossData = conn.cursor().execute(
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

            apiData = conn.cursor().execute(
                '''select provider, appKey, language, accessKeyId, accessKeySecret from %s where name = '%s';''' % (
                apiTableName, self.apiEngine)).fetchone()

            apiProvider, apiappKey, apiLanguage, apiAccessKeyId, apiAccessKeySecret = apiData[0], apiData[1], apiData[2], apiData[3], apiData[4]

            if apiProvider == 'Alibaba':
                transEngine = AliTrans()
            elif apiProvider == 'Tencent':
                transEngine = TencentTrans()
            transEngine.setupApi(apiappKey, apiLanguage, apiAccessKeyId, apiAccessKeySecret)

            srtSubtitleFile = transEngine.mediaToSrt(self.output, oss, self.inputFile)

        # 运行一下 ffmpeg，将输入文件的音视频信息写入文件
        command = 'ffmpeg -hide_banner -i "%s"' % (self.inputFile)
        f = open(self.TEMP_FOLDER + "/params.txt", "w")
        subprocess.call(command, shell=True, stderr=f)

        # 读取一下 params.txt ，找一下 fps 数值到 frameRate
        f = open(self.TEMP_FOLDER + "/params.txt", 'r+', encoding='utf-8')
        with f:
            pre_params = f.read()
        params = pre_params.split('\n')
        for line in params:
            m = re.search('Stream #.*Video.* ([0-9]*) fps', line)
            if m is not None:
                frameRate = float(m.group(1))
        for line in params:
            m = re.search('Stream #.*Audio.* ([0-9]*) Hz', line)
            if m is not None:
                SAMPLE_RATE = int(m.group(1))
        self.print('视频帧率是: ' + str(frameRate) + '\n')
        self.print('音频采样率是: ' + str(SAMPLE_RATE) + '\n')

        # 提取帧 frame%06d.jpg
        # command = ["ffmpeg","-hide_banner","-i",input_FILE,"-qscale:v",str(FRAME_QUALITY),TEMP_FOLDER+"/frame%06d.jpg","-hide_banner"]
        self.print('\n\n将所有视频帧提取到临时文件夹：\n\n')
        command = 'ffmpeg -hide_banner -i "%s" -qscale:v %s %s/frame%s' % (
            self.inputFile, self.frameQuality, self.TEMP_FOLDER, "%06d.jpg")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            self.print(line)

        # 提取音频流 audio.wav
        # command = ["ffmpeg","-hide_banner","-i",input_FILE,"-ab","160k","-ac","2","-ar",str(SAMPLE_RATE),"-vn",TEMP_FOLDER+"/audio.wav"]
        self.print('\n\n分离出音频流:\n\n')
        command = 'ffmpeg -hide_banner -i "%s" -ab 160k -ac 2 -ar %s -vn %s/audio.wav' % (
            self.inputFile, SAMPLE_RATE, self.TEMP_FOLDER)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            self.print(line)

        # 变量 sampleRate, audioData ，得到采样总数为 wavfile.read("audio.wav").shape[0] ，（shape[1] 是声道数）
        sampleRate, audioData = wavfile.read(self.TEMP_FOLDER + "/audio.wav")
        audioSampleCount = audioData.shape[0]
        # 其实 audioData 就是一个一串数字的列表，获得最大值、最小值的负数就完了
        maxAudioVolume = self.getMaxVolume(audioData)

        # 每一帧的音频采样数=采样率/帧率
        samplesPerFrame = sampleRate / frameRate
        # print('\nsamplesPerFrame: %s' % samplesPerFrame)

        # 得到音频总帧数 audioFrameCount
        audioFrameCount = int(math.ceil(audioSampleCount / samplesPerFrame))
        # print('audioFrameCount: %s' % audioFrameCount)

        # numpy.zeros(shape, dtype=float, order='C')  Return a new array of given shape and type, filled with zeros.
        # 返回一个数量为 音频总帧数 的列表，默认数值为0，用于存储这一帧的声音是否大于阈值
        hasLoudAudio = np.zeros((audioFrameCount))

        self.print("\n\n正在分析音频\n\n")
        for i in range(audioFrameCount):
            # start 指的是这一帧的音频的起始采样点是总数第几个
            start = int(i * samplesPerFrame)
            # print('start: %s' % start)
            # end 是 下一帧的音频起点 或 整个音频的终点采样点
            end = min(int((i + 1) * samplesPerFrame), audioSampleCount)
            # audiochunks 就是从 start 到 end 这一段音频
            audiochunks = audioData[start:end]
            # 得到这一小段音频中的相对最大值（相对整个音频的最大值）
            maxchunksVolume = float(self.getMaxVolume(audiochunks)) / maxAudioVolume
            # print('i:%s    start:%s     end: %s    maxChunksVolume:%s   self.silentThreshHole: %s ' % (i, start, end, maxchunksVolume, self.silentThreshold))
            # 要是这一帧的音量大于阈值，记下来。
            if maxchunksVolume >= self.silentThreshold:

                hasLoudAudio[i] = 1

        # 剪切点，这个点很重要。
        chunks = [[0, 0, 0]]
        # 返回一个数量为 音频总帧数 的列表，默认数值为0，用于存储是否该存储这一帧
        shouldIncludeFrame = np.zeros((audioFrameCount))
        for i in range(audioFrameCount):
            start = int(max(0, i - self.frameMargin))
            end = int(min(audioFrameCount, i + 1 + self.frameMargin))
            # 如果从加上淡入淡出的起始到最后之间的几帧中，有1帧是要保留的，那就保留这一区间所有的
            shouldIncludeFrame[i] = np.max(hasLoudAudio[start:end])
            # 如果这一帧不是总数第一帧 且 是否保留这一帧 与 前一帧 不同
            if (i >= 1 and shouldIncludeFrame[i] != shouldIncludeFrame[i - 1]):  # Did we flip?
                # chunks 追加一个 [最后一个的第2个数值（也就是上一个切割点的帧数），本帧的序数，这一帧是否应该保留]
                # 其实就是在整个音频线上砍了好几刀，在刀缝间加上记号：前面这几帧要保留（不保留）
                chunks.append([chunks[-1][1], i, shouldIncludeFrame[i - 1]])

        # chunks 追加一个 [最后一个的第2个数值，总帧数，这一帧是否应该保留]
        # 就是在音频线末尾砍了一刀，加上记号：最后这几帧要保留（不保留）
        chunks.append([chunks[-1][1], audioFrameCount, shouldIncludeFrame[i - 1]])
        # 把开头哪个[0,0,0]去掉
        chunks = chunks[1:]
        # print(str(chunks))
        self.print('静音、响亮片段分析完成\n')

        if self.whetherToUseOnlineSubtitleKeywordAutoCut:
            self.print('开始根据字幕中的关键词处理片段\n')
            subtitleFile = open(srtSubtitleFile, "r", encoding='utf-8')
            subtitleContent = subtitleFile.read()
            subtitleLists = list(srt.parse(subtitleContent))
            subtitleKeywordLists = []
            for i in subtitleLists:
                if re.match('(%s)|(%s)$' % (key_word[0], key_word[1]), i.content):
                    subtitleKeywordLists.append(i)
            lastEnd = 0
            # this q means the index of the chunks
            q = 2
            for i in range(len(subtitleKeywordLists)):
                q -= 2
                self.print(str(subtitleKeywordLists[i]))
                if i > 0:
                    lastEnd = int((subtitleKeywordLists[i - 1].end.seconds + subtitleKeywordLists[
                        i - 1].end.microseconds / 1000000) * frameRate) + 10
                thisStart = int((subtitleKeywordLists[i].start.seconds + subtitleKeywordLists[
                    i].start.microseconds / 1000000) * frameRate) - 4
                thisEnd = int((subtitleKeywordLists[i].end.seconds + subtitleKeywordLists[
                    i].end.microseconds / 1000000) * frameRate) + 10
                self.print("上一区间的结尾是: %s \n" % str(lastEnd))
                self.print("这是区间是: %s 到 %s \n" % (str(thisStart), str(thisEnd)))

                # note that the key_word[0] is cut keyword
                if re.match('(%s)' % (key_word[0]), subtitleKeywordLists[i].content):

                    while q < len(chunks):
                        self.print(str(chunks[q]))
                        if chunks[q][1] <= lastEnd:
                            self.print('这个 chunk (%s 到 %s) 在 cut 区间  %s 到 %s  左侧，下一个 chunk' % (
                            chunks[q][0], chunks[q][1], thisStart, thisEnd))
                            q += 1
                            continue
                        elif chunks[q][0] >= thisEnd:
                            self.print('这个 chunk (%s 到 %s) 在 cut 区间  %s 到 %s  右侧，下一个区间' % (
                            chunks[q][0], chunks[q][1], thisStart, thisEnd))
                            q += 1
                            break
                        elif chunks[q][1] <= thisEnd:
                            self.print(str(chunks[q][1]) + " < " + str(thisEnd))
                            self.print("这个chunk 的右侧 %s 小于区间的终点  %s ，删掉" % (chunks[q][1], thisEnd))
                            del chunks[q]
                        elif chunks[q][1] > thisEnd:
                            self.print("这个chunk 的右侧 %s 大于区间的终点 %s ，把它的左侧 %s 改成本区间的终点 %s " % (
                            chunks[q][1], thisEnd, chunks[q][0], thisEnd))
                            chunks[q][0] = thisEnd
                            q += 1
                # key_word[1] is save keyword
                elif re.match('(%s)' % (key_word[1]), subtitleKeywordLists[i].content):
                    while q < len(chunks):
                        self.print(str(chunks[q]))
                        if chunks[q][1] <= thisStart:
                            self.print("这个区间 (%s 到 %s) 在起点 %s 左侧，放过，下一个 chunk" % (chunks[q][0], chunks[q][1], thisStart))
                            q += 1
                            continue
                        elif chunks[q][0] >= thisEnd:
                            self.print('这个 chunk (%s 到 %s) 在 cut 区间  %s 到 %s  右侧，下一个区间' % (
                            chunks[q][0], chunks[q][1], thisStart, thisEnd))
                            q += 1
                            break
                        elif chunks[q][1] > thisStart and chunks[q][0] <= thisStart:
                            self.print("这个区间 (%s 到 %s) 的右侧，在起点 %s 和终点 %s 之间，修改区间右侧为 %s " % (
                            chunks[q][0], chunks[q][1], thisStart, thisEnd, thisStart))
                            chunks[q][1] = thisStart
                            q += 1
                        elif chunks[q][0] >= thisStart and chunks[q][1] > thisEnd:
                            self.print("这个区间 (%s 到 %s) 的左侧，在起点 %s 和终点 %s 之间，修改区间左侧为 %s " % (
                            chunks[q][0], chunks[q][1], thisStart, thisEnd, thisEnd))
                            chunks[q][0] = thisEnd
                            q += 1
                        elif chunks[q][0] >= thisStart and chunks[q][1] <= thisEnd:
                            self.print("这个区间 (%s 到 %s) 整个在起点 %s 和终点 %s 之间，删除 " % (
                            chunks[q][0], chunks[q][1], thisStart, thisEnd))
                            del chunks[q]
                        elif chunks[q][0] < thisStart and chunks[q][1] > thisEnd:
                            self.print("这个区间 (%s 到 %s) 横跨了 %s 到 %s ，分成两个：从 %s 到 %s ，从 %s 到 %s  " % (
                            chunks[q][0], chunks[q][1], thisStart, thisEnd, chunks[q][0], thisStart, thisEnd,
                            chunks[q][1]))
                            temp = chunks[q]
                            temp[0] = thisEnd
                            chunks[q][1] = thisStart
                            chunks.insert(q + 1, temp)
                            q += 1

        self.print("\n\n开始根据分段信息处理音频\n")
        for i in range(len(chunks)):
            self.print(str(chunks[i]))
        # 输出指针为0
        outputPointer = 0
        # 上一个帧为空
        lastExistingFrame = None
        i = 0
        concat = open(self.TEMP_FOLDER + "/concat.txt", "a")
        for chunk in chunks:
            i += 1
            # 返回一个数量为 0 的列表，数据类型为声音 shape[1]
            outputAudioData = np.zeros((0, audioData.shape[1]))
            # 得到一块音频区间
            audioChunk = audioData[int(chunk[0] * samplesPerFrame):int(chunk[1] * samplesPerFrame)]

            sFile = self.TEMP_FOLDER + "/tempStart.wav"
            eFile = self.TEMP_FOLDER + "/tempEnd.wav"
            # 将得到的音频区间写入到 sFile(startFile)
            wavfile.write(sFile, SAMPLE_RATE, audioChunk)
            # 临时打开 sFile(startFile) 到 reader 变量
            with WavReader(sFile) as reader:
                # 临时打开 eFile(endFile) 到 writer 变量
                with WavWriter(eFile, reader.channels, reader.samplerate) as writer:
                    # 给音频区间设定变速 time-scale modification
                    tsm = phasevocoder(reader.channels, speed=NEW_SPEED[int(chunk[2])])
                    # 按照指定参数，将输入变成输出
                    tsm.run(reader, writer)
            # 读取 endFile ，赋予 改变后的数据
            _, alteredAudioData = wavfile.read(eFile)
            # 长度就是改变后数据的总采样数
            leng = alteredAudioData.shape[0]
            # 记一下，原始音频输出帧，这回输出到哪一个采样点时该停下
            # endPointer 是上一回输出往下的采样点地方
            endPointer = outputPointer + leng
            # 输出数据接上 改变后的数据/最大音量
            outputAudioData = np.concatenate((outputAudioData, alteredAudioData / maxAudioVolume))

            # outputAudioData[outputPointer:endPointer] = alteredAudioData/maxAudioVolume
            # smooth out transitiion's audio by quickly fading in/out
            if leng < AUDIO_FADE_ENVELOPE_SIZE:
                # 把 0 到 400 的数值都变成0 ，之后乘以音频就会让这小段音频静音。
                outputAudioData[0:leng] = 0  # audio is less than 0.01 sec, let's just remove it.
            else:
                # 做一个 1 - 400 的等差数列，分别除以 400，得到淡入时，400 个数就分别是每个音频应乘以的系数。
                premask = np.arange(AUDIO_FADE_ENVELOPE_SIZE) / AUDIO_FADE_ENVELOPE_SIZE
                # 将这个数列乘以 2 ，变成2轴数列，就能用于双声道
                mask = np.repeat(premask[:, np.newaxis], 2, axis=1)  # make the fade-envelope mask stereo
                # 淡入
                outputAudioData[0:0 + AUDIO_FADE_ENVELOPE_SIZE] *= mask
                # 淡出
                outputAudioData[leng - AUDIO_FADE_ENVELOPE_SIZE:leng] *= 1 - mask

            # 开始输出帧是 outputPointer/samplesPerFrame ，根据音频所在帧数决定视频从哪帧开始输出
            startOutputFrame = int(math.ceil(outputPointer / samplesPerFrame))
            # 终止输出帧是 endPointer/samplesPerFrame ，根据音频所在帧数决定视频到哪里就不要再输出了
            endOutputFrame = int(math.ceil(endPointer / samplesPerFrame))
            # 对于所有输出帧
            for outputFrame in range(startOutputFrame, endOutputFrame):
                # 该复制第几个输入帧 ＝ （开始帧序号 + 新速度*（输出序数-输入序数））
                # 新速度*（输出序数-输入序数） 其实是：（输出帧的当前帧数 - 输出帧的起始帧数）* 时间系数，得到应该是原始视频线的第几帧
                inputFrame = int(chunk[0] + NEW_SPEED[int(chunk[2])] * (outputFrame - startOutputFrame))
                # 从原始视频线复制输入帧 到 新视频线 输出帧
                didItWork = self.copyFrame(inputFrame, outputFrame)
                # 如果成功了，最后一帧就是最后那个输入帧
                if didItWork:
                    lastExistingFrame = inputFrame
                else:
                    # 如果没成功，那就复制上回的最后一帧到输出帧。没成功的原因大概是：所谓输入帧不存在，比如视频末尾，音频、视频长度不同。
                    self.copyFrame(lastExistingFrame, outputFrame)
            # 记一下，原始音频输出帧，输出到哪一个采样点了，这就是下回输出的起始点
            outputPointer = endPointer
            wavfile.write(self.TEMP_FOLDER + "/audioNew_" + "%06d" % i + ".wav", SAMPLE_RATE, outputAudioData)
            concat.write("file " + "audioNew_" + "%06d" % i + ".wav\n")
        concat.close()

        self.print("\n\n现在开始合并音频片段\n\n\n")
        # command = ["ffmpeg","-y","-hide_banner","-safe","0","-f","concat","-i",TEMP_FOLDER+"/concat.txt","-framerate",str(frameRate),TEMP_FOLDER+"/audioNew.wav"]
        command = 'ffmpeg -y -hide_banner -safe 0 -f concat -i %s/concat.txt -framerate %s %s/audioNew.wav' % (
        self.TEMP_FOLDER, frameRate, self.TEMP_FOLDER)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            self.print(line)

        self.print("\n\n现在开始合并音视频\n\n\n")
        # command = ["ffmpeg","-y","-hide_banner","-framerate",str(frameRate),"-i",TEMP_FOLDER+"/newFrame%06d.jpg","-i",TEMP_FOLDER+"/audioNew.wav","-strict","-2",OUTPUT_FILE]
        command = 'ffmpeg -y -hide_banner -framerate %s -i %s/newFrame%s -i %s/audioNew.wav -strict -2 %s "%s"' % (
        frameRate, self.TEMP_FOLDER, "%06d.jpg", self.TEMP_FOLDER, self.ffmpegOutputOption, self.outputFile)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            self.print(line)



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
        self.deletePath(self.TEMP_FOLDER)
        self.print('\n\n\n自动剪辑处理完成！\n\n\n')


class AutoSrtThread(QThread):
    signal = pyqtSignal(str)

    output = None # 用于显示输出的控件，如一个 QEditBox，它需要有自定义的 print 方法。

    apiEngine = ''

    def __init__(self, parent=None):
        super(AutoSrtThread, self).__init__(parent)

    def print(self, text):
        self.signal.emit(text)

    def run(self):
        try:
            conn = sqlite3.connect(dbname)

            ossData = conn.cursor().execute(
                '''select provider, bucketName, endPoint, accessKeyId,  accessKeySecret from %s ;''' % (
                    ossTableName)).fetchone()

            conn.close()

            ossProvider, ossBucketName, ossEndPoint, ossAccessKeyId, ossAccessKeySecret = ossData[0], ossData[1], \
                                                                                          ossData[2], ossData[3], \
                                                                                          ossData[4]
            if ossProvider == 'Alibaba':
                oss = AliOss()
                oss.auth(ossBucketName, ossEndPoint, ossAccessKeyId, ossAccessKeySecret)
            elif ossProvider == 'Tencent':
                oss = TencentOss()
                oss.auth(ossBucketName, ossEndPoint, ossAccessKeyId, ossAccessKeySecret)

            apiData = conn.cursor().execute(
                '''select provider, appKey, language, accessKeyId, accessKeySecret from %s where name = '%s';''' % (
                    apiTableName, self.apiEngine)).fetchone()

            apiProvider, apiappKey, apiLanguage, apiAccessKeyId, apiAccessKeySecret = apiData[0], apiData[1], apiData[
                2], apiData[3], apiData[4]

            if apiProvider == 'Alibaba':
                transEngine = AliTrans()
            elif apiProvider == 'Tencent':
                transEngine = TencentTrans()
            transEngine.setupApi(apiappKey, apiLanguage, apiAccessKeyId, apiAccessKeySecret)

            srtSubtitleFile = transEngine.mediaToSrt(self.output, oss, self.inputFile)

            self.print('\n\n转字幕完成\n\n')
        except:
            self.print('转字幕过程出错了')


class AliOss():
    def __init__(self):
        pass
    def auth(self, bucketName, endpointDomain, accessKeyId, accessKeySecret):
        self.bucketName = bucketName
        self.endpointDomain = endpointDomain
        self.accessKeyId = accessKeyId
        self.accessKeySecret = accessKeySecret
        self.auth = oss2.Auth(self.accessKeyId, self.accessKeySecret)
        self.bucket = oss2.Bucket(self.auth, self.endpointDomain, self.bucketName)

    def create(self):
        # 这面这行用于创建，并设置存储空间为私有读写权限。
        self.bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)

    def upload(self, source, destination):
        # 这个是上传文件到 oss
        # destination 上传文件到OSS时需要指定包含文件后缀在内的完整路径，例如abc/efg/123.jpg。
        # source 由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
        # 要返回远程文件的链接
        self.bucket.put_object_from_file(destination, source)
        remoteLink = r'https://' + urllib.parse.quote(
            '%s.%s/%s' % (self.bucketName, self.endpointDomain, destination))
        return remoteLink

    def download(self, source, destination):
        # 以下代码用于将指定的OSS文件下载到本地文件：
        # source 从OSS下载文件时需要指定包含文件后缀在内的完整路径，例如abc/efg/123.jpg。
        # destination由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
        self.bucket.get_object_to_file(source, destination)


    def delete(self, cloudFile):
        # cloudFile 表示删除OSS文件时需要指定包含文件后缀在内的完整路径，例如abc/efg/123.jpg。string 格式哦
        self.bucket.delete_object(cloudFile)


class AliTrans():
    def __init__(self):
        pass
    def setupApi(self, appKey, language, accessKeyId, accessKeySecret):
        self.appKey = appKey
        self.accessKeyId = accessKeyId
        self.accessKeySecret = accessKeySecret

    def fileTrans(self, output, accessKeyId, accessKeySecret, appKey, fileLink):
        # 地域ID，常量内容，请勿改变
        REGION_ID = "cn-shanghai"
        PRODUCT = "nls-filetrans"
        DOMAIN = "filetrans.cn-shanghai.aliyuncs.com"
        API_VERSION = "2018-08-17"
        POST_REQUEST_ACTION = "SubmitTask"
        GET_REQUEST_ACTION = "GetTaskResult"
        # 请求参数key
        KEY_APP_KEY = "appkey"
        KEY_FILE_LINK = "file_link"
        KEY_VERSION = "version"
        KEY_ENABLE_WORDS = "enable_words"
        # 是否开启智能分轨
        KEY_AUTO_SPLIT = "auto_split"
        # 响应参数key
        KEY_TASK = "Task"
        KEY_TASK_ID = "TaskId"
        KEY_STATUS_TEXT = "StatusText"
        KEY_RESULT = "Result"
        # 状态值
        STATUS_SUCCESS = "SUCCESS"
        STATUS_RUNNING = "RUNNING"
        STATUS_QUEUEING = "QUEUEING"
        # 创建AcsClient实例
        client = AcsClient(accessKeyId, accessKeySecret, REGION_ID)
        # 提交录音文件识别请求
        postRequest = CommonRequest()
        postRequest.set_domain(DOMAIN)
        postRequest.set_version(API_VERSION)
        postRequest.set_product(PRODUCT)
        postRequest.set_action_name(POST_REQUEST_ACTION)
        postRequest.set_method('POST')
        # 新接入请使用4.0版本，已接入(默认2.0)如需维持现状，请注释掉该参数设置
        # 设置是否输出词信息，默认为false，开启时需要设置version为4.0
        task = {KEY_APP_KEY: appKey, KEY_FILE_LINK: fileLink, KEY_VERSION: "4.0", KEY_ENABLE_WORDS: False}
        # 开启智能分轨，如果开启智能分轨 task中设置KEY_AUTO_SPLIT : True
        # task = {KEY_APP_KEY : appKey, KEY_FILE_LINK : fileLink, KEY_VERSION : "4.0", KEY_ENABLE_WORDS : False, KEY_AUTO_SPLIT : True}
        task = json.dumps(task)
        # print(task)
        postRequest.add_body_params(KEY_TASK, task)
        taskId = ""
        try:
            postResponse = client.do_action_with_exception(postRequest)
            postResponse = json.loads(postResponse)
            statusText = postResponse[KEY_STATUS_TEXT]
            if statusText == STATUS_SUCCESS:
                output.print("录音文件识别请求成功响应！\n")
                taskId = postResponse[KEY_TASK_ID]
            else:
                output.print("录音文件识别请求失败！\n")
                return
        except ServerException as e:
            output.print(e)
        except ClientException as e:
            output.print(e)
        # 创建CommonRequest，设置任务ID
        getRequest = CommonRequest()
        getRequest.set_domain(DOMAIN)
        getRequest.set_version(API_VERSION)
        getRequest.set_product(PRODUCT)
        getRequest.set_action_name(GET_REQUEST_ACTION)
        getRequest.set_method('GET')
        getRequest.add_query_param(KEY_TASK_ID, taskId)
        # 提交录音文件识别结果查询请求
        # 以轮询的方式进行识别结果的查询，直到服务端返回的状态描述符为"SUCCESS"、"SUCCESS_WITH_NO_VALID_FRAGMENT"，
        # 或者为错误描述，则结束轮询。
        statusText = ""
        while True:
            try:
                self.getResponse = client.do_action_with_exception(getRequest)
                self.getResponse = json.loads(self.getResponse)
                statusText = self.getResponse[KEY_STATUS_TEXT]
                if statusText == STATUS_RUNNING or statusText == STATUS_QUEUEING:
                    # 继续轮询
                    if statusText == STATUS_QUEUEING:
                        output.print('云端任务正在排队中，3 秒后重新查询\n')
                    elif statusText == STATUS_RUNNING:
                        output.print('音频转文字中，3 秒后重新查询\n')
                    time.sleep(3)
                else:
                    # 退出轮询
                    break
            except ServerException as e:
                output.print(e)
                pass
            except ClientException as e:
                output.print(e)
                pass
        if statusText == STATUS_SUCCESS:
            output.print("录音文件识别成功！\n")
        else:
            output.print("录音文件识别失败！\n")
        return

    def subGen(self, output, oss, audioFile):

        # 确定本地音频文件名
        audioFileFullName = os.path.basename(audioFile)

        # 确定当前日期
        localTime = time.localtime(time.time())
        year = localTime.tm_year
        month = localTime.tm_mon
        day = localTime.tm_mday

        # 用当前日期给 oss 文件指定上传路径
        remoteFile = '%s/%s/%s/%s' % (year, month, day, audioFileFullName)
        # 目标链接要转换成 base64 的

        output.print('上传 oss 目标路径：' + remoteFile + '\n')

        # 上传音频文件 upload audio to cloud
        output.print('上传音频中\n')
        remoteLink = oss.upload(audioFile, remoteFile)

        # 识别文字 recognize
        output, print('正在识别中\n')
        self.fileTrans(output, self.accessKeyId, self.accessKeySecret, self.appKey, remoteLink)

        # 删除文件

        print('识别完成，现在删除 oss 上的音频文件：' + remoteFile + '\n')
        oss.delete(remoteFile)

        # 新建一个列表，用于存放字幕
        subtitles = list()
        try:
            for i in range(len(self.getResponse['Result']['Sentences'])):
                startSeconds = self.getResponse['Result']['Sentences'][i]['BeginTime'] // 1000
                startMicroseconds = self.getResponse['Result']['Sentences'][i]['BeginTime'] % 1000 * 1000
                endSeconds = self.getResponse['Result']['Sentences'][i]['EndTime'] // 1000
                endMicroseconds = self.getResponse['Result']['Sentences'][i]['EndTime'] % 1000 * 1000

                # 设定字幕起始时间
                if startSeconds == 0:
                    startTime = datetime.timedelta(microseconds=startMicroseconds)
                else:
                    startTime = datetime.timedelta(seconds=startSeconds, microseconds=startMicroseconds)

                # 设定字幕终止时间
                if endSeconds == 0:
                    endTime = datetime.timedelta(microseconds=endMicroseconds)
                else:
                    endTime = datetime.timedelta(seconds=endSeconds, microseconds=endMicroseconds)

                # 设定字幕内容
                subContent = self.getResponse['Result']['Sentences'][i]['Text']

                # 字幕的内容还需要去掉未尾的标点
                subContent = re.sub('(.)$|(。)$|(. )$', '', subContent)

                # 合成 srt 类
                subtitle = srt.Subtitle(index=i, start=startTime, end=endTime, content=subContent)

                # 把合成的 srt 类字幕，附加到列表
                subtitles.append(subtitle)
        except:
            output.print('云端数据转字幕的过程中出错了，可能是没有识别到文字\n')
            subtitles = [srt.Subtitle(index=0, start=datetime.timedelta(0), end=datetime.timedelta(microseconds=480000), content=' ', proprietary='')]


        # 生成 srt 格式的字幕
        srtSub = srt.compose(subtitles, reindex=True, start_index=1, strict=True)

        # 得到输入文件除了除了扩展名外的名字
        pathPrefix = os.path.splitext(audioFile)[0]

        # 得到要写入的 srt 文件名
        srtPath = '%s.srt' % (pathPrefix)

        # 写入字幕
        with open(srtPath, 'w+', encoding='utf-8') as srtFile:
            srtFile.write(srtSub)

        return srtPath

    def wavGen(self, output, mediaFile):
        # 得到输入文件除了除了扩展名外的名字
        pathPrefix = os.path.splitext(mediaFile)[0]
        # ffmpeg 命令
        command = 'ffmpeg -hide_banner -y -i "%s" -ac 1 -ar 16000 "%s.wav"' % (mediaFile, pathPrefix)
        output.print('现在开始生成单声道、 16000Hz 的 wav 音频：%s \n' % command)
        subprocess.call(command, shell=True)
        return '%s.wav' % (pathPrefix)

    # 用媒体文件生成 srt
    def mediaToSrt(self, output, oss, mediaFile):
        # 先生成 wav 格式音频，并获得路径
        wavFile = self.wavGen(output, mediaFile)

        # 从 wav 音频文件生成 srt 字幕, 并得到生成字幕的路径
        srtFilePath = self.subGen(output, oss, wavFile)

        # 删除 wav 文件
        os.remove(wavFile)
        output.print('已删除 oss 音频文件\n')

        return srtFilePath


class TencentOss():
    def __init__(self):
        pass
    def auth(self, bucketName, endpointDomain, accessKeyId, accessKeySecret):
        self.bucketName = bucketName
        self.endpoint = endpointDomain

        self.region = re.search(r'\w+-\w+', self.endpoint)
        self.bucketDomain = 'https://%s.%s' % (self.bucketName, self.endpoint)

        self.secret_id = accessKeyId
        self.secret_key = accessKeySecret

        self.token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
        self.scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

        self.proxies = {
            'http': '127.0.0.1:80',  # 替换为用户的 HTTP代理地址
            'https': '127.0.0.1:443'  # 替换为用户的 HTTPS代理地址
        }

        self.config = CosConfig(Region=self.region, SecretId=self.secret_id, SecretKey=self.secret_key, Token=self.token,
                                Scheme=self.scheme, Endpoint=self.endpoint)
        self.client = CosS3Client(self.config)

    def create(self):
        #创建存储桶
        response = self.client.create_bucket(
            Bucket=self.bucketName
        )
        return response

    def upload(self, source, destination):
        #### 文件流简单上传（不支持超过5G的文件，推荐使用下方高级上传接口）
        # 强烈建议您以二进制模式(binary mode)打开文件,否则可能会导致错误
        with open(source, 'rb') as fp:
            response = self.client.put_object(
                Bucket=self.bucketName,
                Body=fp,
                Key=destination,
                StorageClass='STANDARD',
                EnableMD5=False
            )
        print(response['ETag'])
        remoteLink = 'https://' + urllib.parse.quote('%s.%s/%s' % (self.bucketName, self.endpoint, destination))
        return remoteLink

    def download(self, source, destination):
        #  获取文件到本地
        response = self.client.get_object(
            Bucket=self.bucketName,
            Key=source,
        )
        response['Body'].get_stream_to_file(destination)


    def delete(self, cloudFile):
        # cloudFile 表示删除OSS文件时需要指定包含文件后缀在内的完整路径，例如abc/efg/123.jpg。string 格式哦
        response = self.client.delete_object(
            Bucket=self.bucketName,
            Key=cloudFile
        )


class TencentTrans():
    def __init__(self):
        pass

    def setupApi(self, appKey, language, accessKeyId, accessKeySecret):
        self.appKey = appKey
        self.accessKeyId = accessKeyId
        self.accessKeySecret = accessKeySecret
        print(language)
        if language == '中文普通话':
            self.language = 'zh'
        elif language == '英语':
            self.language = 'en'
        elif language == '粤语':
            self.language = 'ca'

    def urlAudioToSrt(self, output, url, language):
        # 语言可以有：en, zh, ca
        # 16k_zh：16k 中文普通话通用；
        # 16k_en：16k 英语；
        # 16k_ca：16k 粤语。
        output.print('即将识别：' + url)
        try:
            # 此处<Your SecretId><Your SecretKey>需要替换成客户自己的账号信息
            cred = credential.Credential(self.accessKeyId, self.accessKeySecret)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "asr.tencentcloudapi.com"
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            clientProfile.signMethod = "TC3-HMAC-SHA256"
            client = asr_client.AsrClient(cred, "ap-shanghai", clientProfile)
            req = models.CreateRecTaskRequest()
            # params = {"EngineModelType":"16k_" + language,"ChannelNum":1,"ResTextFormat":0,"SourceType":0,"Url":url}
            params = {"EngineModelType": "16k_" + language, "ChannelNum": 1, "ResTextFormat": 0, "SourceType": 0,
                      "Url": url}
            req._deserialize(params)
            resp = client.CreateRecTask(req)
            print(resp.to_json_string())
            # windows 系统使用下面一行替换上面一行
            # print(resp.to_json_string().decode('UTF-8').encode('GBK') )
            resp = json.loads(resp.to_json_string())
            return resp['Data']['TaskId']

        except TencentCloudSDKException as err:
            output.print(err)

    def queryResult(self, output, taskid):
        # try:

        cred = credential.Credential(self.accessKeyId, self.accessKeySecret)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "asr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = asr_client.AsrClient(cred, "ap-shanghai", clientProfile)

        req = models.DescribeTaskStatusRequest()
        params = '{"TaskId":%s}' % (taskid)
        req.from_json_string(params)

        while True:

            try:
                resp = client.DescribeTaskStatus(req).to_json_string()
                resp = json.loads(resp)
                status = resp['Data']['Status']
                if status == 3:
                    # 出错了
                    output.print('服务器有点错误,错误原因是：' + resp['Data']['ErrorMsg'])
                    time.sleep(3)
                elif status != 0:
                    output.print("云端任务排队中，10秒之后再次查询\n")
                    time.sleep(10)
                elif status != 2:
                    output.print("任务进行中，3秒之后再次查询\n")
                    time.sleep(3)
                else:
                    # 退出轮询
                    break
            except ServerException as e:
                output.print(e)
                pass
            except ClientException as e:
                output.print(e)
                pass
        # 将返回的内容中的结果部分提取出来，转变成一个列表：['[0:0.940,0:3.250]  这是第一句话保留。', '[0:4.400,0:7.550]  这是第二句话咔嚓。', '[0:8.420,0:10.850]  这是第三句话保留。', '[0:11.980,0:14.730]  这是第四句话咔嚓。', '[0:15.480,0:18.250]  这是第五句话保留。']
        transResult = resp['Data']['Result'].splitlines()
        return transResult

        # except TencentCloudSDKException as err:
        #     print(err)

    def subGen(self, output, oss, audioFile):
        # 确定本地音频文件名
        audioFileFullName = os.path.basename(audioFile)

        # 确定当前日期
        localTime = time.localtime(time.time())
        year = localTime.tm_year
        month = localTime.tm_mon
        day = localTime.tm_mday

        # 用当前日期给 oss 文件指定上传路径
        remoteFile = '%s/%s/%s/%s' % (year, month, day, audioFileFullName)
        # 目标链接要转换成 base64 的
        output.print('\n上传目标路径：' + remoteFile + '\n\n')

        # 上传音频文件 upload audio to cloud
        output.print('上传音频中\n')
        remoteLink = oss.upload(audioFile, remoteFile)

        # 识别文字 recognize
        output.print('正在识别中\n')
        taskId = self.urlAudioToSrt(output, remoteLink, self.language)

        # 获取识别结果
        output.print('正在读取结果中\n')
        print(taskId)
        transResult = self.queryResult(output, taskId)

        # 删除文件
        oss.delete(remoteFile)

        # 新建一个列表，用于存放字幕
        subtitles = list()
        for i in range(len(transResult)):
            timestampAndSentence = transResult[i].split("  ")
            timestamp = timestampAndSentence[0].lstrip(r'[').rstrip(r']').split(',')
            startTimestamp = timestamp[0].split(':')
            startMinute = int(startTimestamp[0])
            startSecondsAndMicroseconds = startTimestamp[1].split('.')
            startSeconds = int(startSecondsAndMicroseconds[0]) + startMinute * 60
            startMicroseconds = int(startSecondsAndMicroseconds[1]) * 1000

            endTimestamp = timestamp[1].split(':')
            endMinute = int(endTimestamp[0])
            endSecondsAndMicroseconds = endTimestamp[1].split('.')
            endSeconds = int(endSecondsAndMicroseconds[0]) + endMinute * 60
            endMicroseconds = int(endSecondsAndMicroseconds[1]) * 1000

            sentence = timestampAndSentence[1]

            startTime = datetime.timedelta(seconds=startSeconds, microseconds=startMicroseconds)

            # 设定字幕终止时间
            if endSeconds == 0:
                endTime = datetime.timedelta(microseconds=endMicroseconds)
            else:
                endTime = datetime.timedelta(seconds=endSeconds, microseconds=endMicroseconds)

            # 字幕的内容还需要去掉未尾的标点
            subContent = re.sub('(.)$|(。)$|(. )$', '', sentence)

            # 合成 srt 类
            subtitle = srt.Subtitle(index=i, start=startTime, end=endTime, content=subContent)

            # 把合成的 srt 类字幕，附加到列表
            subtitles.append(subtitle)

        # 生成 srt 格式的字幕
        srtSub = srt.compose(subtitles, reindex=True, start_index=1, strict=True)

        # 得到输入文件除了除了扩展名外的名字
        pathPrefix = os.path.splitext(audioFile)[0]

        # 得到要写入的 srt 文件名
        srtPath = '%s.srt' % (pathPrefix)

        # 写入字幕
        with open(srtPath, 'w+', encoding='utf-8') as srtFile:
            srtFile.write(srtSub)

        return srtPath

    def wavGen(self, output, mediaFile):
        # 得到输入文件除了除了扩展名外的名字
        pathPrefix = os.path.splitext(mediaFile)[0]
        # ffmpeg 命令
        command = 'ffmpeg -hide_banner -y -i "%s" -ac 1 -ar 16000 "%s.wav"' % (mediaFile, pathPrefix)
        output.print('现在开始生成单声道、 16000Hz 的 wav 音频：\n' + command)
        subprocess.call(command, shell=True)
        return '%s.wav' % (pathPrefix)

    def mediaToSrt(self, output, oss, mediaFile):
        # 先生成 wav 格式音频，并获得路径
        wavFile = self.wavGen(output, mediaFile)

        # 从 wav 音频文件生成 srt 字幕, 并得到生成字幕的路径
        srtFilePath = self.subGen(output, oss, wavFile)

        # 删除 wav 文件
        os.remove(wavFile)
        output.print('已删除 oss 音频文件\n')

        return srtFilePath


def execute(command):
    # 判断一下系统，如果是windows系统，就直接将命令在命令行窗口中运行，避免在程序中运行时候的卡顿。
    # 主要是因为手上没有图形化的linux系统和mac os系统，不知道怎么打开他们的终端执行某个个命令，所以就将命令在程序中运行，输出到一个新窗口的文本编辑框。
    # system = platform.system()
    # if system == 'Windows':
    #     os.system('start cmd /k ' + command)
    # else:
    #     console = Console(main)
    #     console.runCommand(command)

    # 新方法，执行子进程，在新窗口输出
    thread = CommandThread() #新建一个子进程
    thread.command = command # 将要执行的命令赋予子进程
    window = Console(main) # 显示一个新窗口，用于显示子进程的输出
    output = window.consoleBox # 获得新窗口中的输出控件
    thread.signal.connect(output.print) # 将 子进程中的输出信号 连接到 新窗口输出控件的输出槽
    window.thread = thread  # 把这里的剪辑子进程赋值给新窗口，这样新窗口就可以在关闭的时候也把进程退出
    thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
