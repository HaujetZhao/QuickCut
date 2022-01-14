# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from moduels.component.MyQLine import MyQLine
from moduels.component.HintLabel import HintLabel
from moduels.component.NormalValue import 常量
from moduels.gui.Console import Console
from moduels.gui.VoiceInputMethodTranscribeSubtitleWindow import VoiceInputMethodTranscribeSubtitleWindow
from moduels.function.strTimeToSecondsTime import strTimeToSecondsTime
from moduels.function.getMediaTimeLength import getMediaTimeLength
from moduels.tool.FileTranscribeAutoSrtThread import FileTranscribeAutoSrtThread
from moduels.tool.FFmpegWavGenThread import FFmpegWavGenThread


import os



class FFmpegAutoSrtTab(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = 常量.conn
        self.dbname = 常量.数据库路径
        self.ossTableName = 常量.oss表名
        self.apiTableName = 常量.api表名
        self.preferenceTableName = 常量.首选项表名
        self.apiUpdateBroadCaster = 常量.apiUpdateBroadCaster
        self.initGui()

    def initGui(self):
        self.masterLayout = QVBoxLayout() # 主体纵向布局
        self.setLayout(self.masterLayout)

        self.GUI频文件转字幕()

        self.masterLayout.addSpacing(30)
        self.masterLayout.addWidget(self.fileTranscribeSubtitleGroup)
        self.masterLayout.addStretch(0)

    def GUI频文件转字幕(self):
        self.apiUpdateBroadCaster.signal.connect(self.fileTranscribeSubtitleUpdateEngineList)  # 接收数据库变更的信号更新引擎

        self.fileTranscribeSubtitleGroup = QGroupBox(self.tr('通过录音文件识别引擎转字幕'))  # 使用文件转语音的功能ui框架
        # self.fileTranscribeSubtitleWidgetLayout = QGridLayout()
        self.fileTranscribeSubtitleWidgetLayout = QVBoxLayout()
        self.fileTranscribeSubtitleGroup.setLayout(self.fileTranscribeSubtitleWidgetLayout)

        self.fileTranscribeSubtitleInputHint = QLabel(self.tr('输入文件：'))
        # self.fileTranscribeSubtitleInputHint.setAlignment(Qt.AlignRight)
        self.fileTranscribeSubtitleInputEdit = MyQLine()
        self.fileTranscribeSubtitleInputEdit.textChanged.connect(self.fileTranscribeSubtitleInputEditChanged)
        self.fileTranscribeSubtitleInputButton = QPushButton(self.tr('选择文件'))
        self.fileTranscribeSubtitleInputButton.clicked.connect(self.fileTranscribeSubtitleInputButtonClicked)

        self.fileTranscribeSubtitleOutputHint = QLabel(self.tr('字幕输出文件：'))
        self.fileTranscribeSubtitleOutputEdit = MyQLine()
        self.fileTranscribeSubtitleOutputEdit.setReadOnly(True)

        self.fileTranscribeSubtitleEngineLabel = QLabel(self.tr('字幕语音 API：'))
        self.fileTranscribeSubtitleEngineComboBox = QComboBox()

        apis = self.conn.cursor().execute('select name from %s' % self.apiTableName).fetchall()
        if apis != None:
            for api in apis:
                self.fileTranscribeSubtitleEngineComboBox.addItem(api[0])
            self.fileTranscribeSubtitleEngineComboBox.setCurrentIndex(0)
            pass

        self.fileTranscribeSubtitleRunButton = QPushButton(self.tr('开始运行'))
        self.fileTranscribeSubtitleRunButton.clicked.connect(self.fileTranscribeSubtitleRunButtonClicked)

        self.fileTranscribeSubtitleInputBoxAndButtonLayout = QHBoxLayout()
        self.fileTranscribeSubtitleInputBoxAndButtonLayout.setContentsMargins(0, 0, 0, 0)
        self.fileTranscribeSubtitleInputBoxAndButtonLayout.addWidget(self.fileTranscribeSubtitleInputEdit, 4)
        self.fileTranscribeSubtitleInputBoxAndButtonLayout.addWidget(self.fileTranscribeSubtitleInputButton, 1)
        self.fileTranscribeSubtitleInputBoxAndButtonWidget = QWidget()
        self.fileTranscribeSubtitleInputBoxAndButtonWidget.setLayout(self.fileTranscribeSubtitleInputBoxAndButtonLayout)

        self.fileTranscribeSubtitleWidgetLayoutFormLayout = QFormLayout()
        self.fileTranscribeSubtitleWidgetLayoutFormLayout.addRow(self.fileTranscribeSubtitleInputHint,
                                                                 self.fileTranscribeSubtitleInputBoxAndButtonWidget)
        self.fileTranscribeSubtitleWidgetLayoutFormLayout.addRow(self.fileTranscribeSubtitleOutputHint,
                                                                 self.fileTranscribeSubtitleOutputEdit)
        self.fileTranscribeSubtitleWidgetLayoutFormLayout.addRow(self.fileTranscribeSubtitleEngineLabel,
                                                                 self.fileTranscribeSubtitleEngineComboBox)

        self.fileTranscribeSubtitleWidgetLayoutFormLayout.setWidget(3, QFormLayout.SpanningRole,
                                                                    self.fileTranscribeSubtitleRunButton)

        self.fileTranscribeSubtitleWidgetLayout.addLayout(self.fileTranscribeSubtitleWidgetLayoutFormLayout)

    def fileTranscribeSubtitleInputButtonClicked(self):
        filename = QFileDialog().getOpenFileName(self, self.tr('打开文件'), None, self.tr('所有文件(*)'))
        if filename[0] != '':
            self.fileTranscribeSubtitleInputEdit.setText(filename[0])
            self.fileTranscribeSubtitleOutputName = os.path.splitext(filename[0])[0] + '.srt'
            self.fileTranscribeSubtitleOutputEdit.setText(self.fileTranscribeSubtitleOutputName)
        return True

    def fileTranscribeSubtitleInputEditChanged(self):
        filename = self.fileTranscribeSubtitleInputEdit.text()
        # if filename != '':
        self.fileTranscribeSubtitleOutputName = os.path.splitext(filename)[0] + '.srt'
        self.fileTranscribeSubtitleOutputEdit.setText(self.fileTranscribeSubtitleOutputName)
        return True

    def fileTranscribeSubtitleRunButtonClicked(self):
        if self.fileTranscribeSubtitleInputEdit.text() != '':
            window = Console(常量.mainWindow)

            output = window.consoleBox
            outputForFFmpeg = window.consoleBoxForFFmpeg

            thread = FileTranscribeAutoSrtThread(常量.mainWindow)

            thread.inputFile = self.fileTranscribeSubtitleInputEdit.text()

            thread.output = output

            thread.apiEngine = self.fileTranscribeSubtitleEngineComboBox.currentText()

            thread.signal.connect(output.print)
            thread.signalForFFmpeg.connect(outputForFFmpeg.print)

            window.thread = thread  # 把这里的剪辑子进程赋值给新窗口，这样新窗口就可以在关闭的时候也把进程退出

            thread.start()

    def fileTranscribeSubtitleUpdateEngineList(self):
        ########改用主数据库
        apis = 常量.conn.cursor().execute('select name from %s' % 常量.api表名).fetchall()
        self.fileTranscribeSubtitleEngineComboBox.clear()
        if apis != None:
            for api in apis:
                self.fileTranscribeSubtitleEngineComboBox.addItem(api[0])
            self.fileTranscribeSubtitleEngineComboBox.setCurrentIndex(0)
            pass
        # 不在这里关数据库了
