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
from moduels.tool.VoiceInputMethodAutoSrtThread import VoiceInputMethodAutoSrtThread
from moduels.tool.VoiciInputMethodTrans import VoiciInputMethodTrans
from moduels.tool.FFmpegWavGenThread import FFmpegWavGenThread


import os



class FFmpegAutoSrtTab(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = 常量.conn
        self.dbname = 常量.dbname
        self.ossTableName = 常量.ossTableName
        self.apiTableName = 常量.apiTableName
        self.preferenceTableName = 常量.preferenceTableName
        self.apiUpdateBroadCaster = 常量.apiUpdateBroadCaster
        self.initGui()

    def initGui(self):
        self.masterLayout = QVBoxLayout() # 主体纵向布局
        self.setLayout(self.masterLayout)

        # 音频文件转字幕
        if True:

            self.apiUpdateBroadCaster.signal.connect(self.fileTranscribeSubtitleUpdateEngineList) # 接收数据库变更的信号更新引擎

            self.fileTranscribeSubtitleGroup = QGroupBox(self.tr('通过录音文件识别引擎转字幕')) # 使用文件转语音的功能ui框架
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
            self.fileTranscribeSubtitleInputBoxAndButtonLayout.setContentsMargins(0,0,0,0)
            self.fileTranscribeSubtitleInputBoxAndButtonLayout.addWidget(self.fileTranscribeSubtitleInputEdit, 4)
            self.fileTranscribeSubtitleInputBoxAndButtonLayout.addWidget(self.fileTranscribeSubtitleInputButton,1)
            self.fileTranscribeSubtitleInputBoxAndButtonWidget = QWidget()
            self.fileTranscribeSubtitleInputBoxAndButtonWidget.setLayout(self.fileTranscribeSubtitleInputBoxAndButtonLayout)

            self.fileTranscribeSubtitleWidgetLayoutFormLayout = QFormLayout()
            self.fileTranscribeSubtitleWidgetLayoutFormLayout.addRow(self.fileTranscribeSubtitleInputHint, self.fileTranscribeSubtitleInputBoxAndButtonWidget)
            self.fileTranscribeSubtitleWidgetLayoutFormLayout.addRow(self.fileTranscribeSubtitleOutputHint, self.fileTranscribeSubtitleOutputEdit)
            self.fileTranscribeSubtitleWidgetLayoutFormLayout.addRow(self.fileTranscribeSubtitleEngineLabel, self.fileTranscribeSubtitleEngineComboBox)

            self.fileTranscribeSubtitleWidgetLayoutFormLayout.setWidget(3, QFormLayout.SpanningRole, self.fileTranscribeSubtitleRunButton)


            self.fileTranscribeSubtitleWidgetLayout.addLayout(self.fileTranscribeSubtitleWidgetLayoutFormLayout)

        self.masterLayout.addSpacing(30)

        # 通过语音输入法转字幕
        if True:

            self.voiceInputMethodSubtitleGroup = QGroupBox(self.tr('通过语音输入法转字幕'))  # 使用文件转语音的功能ui框架
            self.voiceInputMethodSubtitleWidgetLayout = QGridLayout()
            self.voiceInputMethodSubtitleGroup.setLayout(self.voiceInputMethodSubtitleWidgetLayout)


            self.voiceInputMethodSubtitleInputHint = QLabel(self.tr('输入文件：'))
            self.voiceInputMethodSubtitleInputEdit = MyQLine()
            self.voiceInputMethodSubtitleInputEdit.textChanged.connect(self.voiceInputMethodSubtitleInputEditChanged)
            self.voiceInputMethodSubtitleInputButton = QPushButton(self.tr('选择文件'))
            self.voiceInputMethodSubtitleInputButton.clicked.connect(self.voiceInputMethodSubtitleInputButtonClicked)

            self.voiceInputMethodSubtitleTimestampAuxHint = QLabel(self.tr('时间戳辅助文件：'))
            self.voiceInputMethodSubtitleTimestampEdit = MyQLine()
            self.voiceInputMethodSubtitleTimestampEdit.setPlaceholderText('选填，只要是合格的带时间戳的字幕文件就可以')
            self.voiceInputMethodSubtitleTimestampEdit.textChanged.connect(self.voiceInputMethodSubtitleTimestampEditChanged)
            self.voiceInputMethodSubtitleTimestampButton = QPushButton(self.tr('选择文件'))
            self.voiceInputMethodSubtitleTimestampButton.clicked.connect(self.voiceInputMethodSubtitleTimestampButtonClicked)

            self.voiceInputMethodSubtitleOutputHint = QLabel(self.tr('字幕输出文件：'))
            self.voiceInputMethodSubtitleOutputEdit = MyQLine()
            self.voiceInputMethodSubtitleOutputEdit.setReadOnly(True)


            self.voiceInputMethodSubtitle可选时间段Hint = QLabel(self.tr('可选截取片段：'))
            self.voiceInputMethodSubtitle截取时间hbox = QHBoxLayout()
            self.voiceInputMethodSubtitle截取时间start标签 = QLabel(self.tr('起始时间：'))
            self.voiceInputMethodSubtitle截取时间start输入框 = MyQLine()
            self.voiceInputMethodSubtitle截取时间start输入框.setAlignment(Qt.AlignCenter)
            self.voiceInputMethodSubtitle截取时间end标签 = QLabel(self.tr('结束时间：'))
            self.voiceInputMethodSubtitle截取时间end输入框 = MyQLine()
            self.voiceInputMethodSubtitle截取时间end输入框.setAlignment(Qt.AlignCenter)
            self.voiceInputMethodSubtitle截取时间hbox.addWidget(self.voiceInputMethodSubtitle截取时间start标签)
            self.voiceInputMethodSubtitle截取时间hbox.addWidget(self.voiceInputMethodSubtitle截取时间start输入框)
            self.voiceInputMethodSubtitle截取时间hbox.addWidget(self.voiceInputMethodSubtitle截取时间end标签)
            self.voiceInputMethodSubtitle截取时间hbox.addWidget(self.voiceInputMethodSubtitle截取时间end输入框)

            self.timeValidator = QRegExpValidator(self)
            self.timeValidator.setRegExp(QRegExp(r'[0-9]{0,2}:?[0-9]{0,2}:?[0-9]{0,2}\.?[0-9]{0,2}'))
            self.voiceInputMethodSubtitle截取时间start输入框.setValidator(self.timeValidator)
            self.voiceInputMethodSubtitle截取时间end输入框.setValidator(self.timeValidator)



            # 引擎相关
            if True:
                self.voiceInputMethodSubtitleVoiceInputShortcutLabel = QLabel(self.tr('语音输入快捷键：'))
                self.voiceInputMethodSubtitleVoiceInputShortcutComboBox = QComboBox()
                self.voiceInputMethodSubtitleVoiceInputShortcutComboBox.addItems(
                    ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12'])
                self.voiceInputMethodSubtitleVoiceInputShortcutComboBox.setCurrentText('f6')
                # self.validKeyList = ['alt', 'alt gr', 'ctrl', 'left alt', 'left ctrl', 'left shift', 'left windows', 'right alt', 'right ctrl', 'right shift', 'right windows', 'shift', 'windows']

                self.voiceInputMethodSubtitleAuditokMinDurHint = QLabel(self.tr('片段最短时间：'))
                self.voiceInputMethodSubtitleAuditokMinDurBox = QDoubleSpinBox()
                self.voiceInputMethodSubtitleAuditokMinDurBox.setMinimum(0.3)
                self.voiceInputMethodSubtitleAuditokMinDurBox.setSingleStep(1)
                self.voiceInputMethodSubtitleAuditokMinDurBox.setValue(0.3)

                self.voiceInputMethodSubtitleAuditokMaxDurHint = QLabel(self.tr('片段最长时间：'))
                self.voiceInputMethodSubtitleAuditokMaxDurBox = QDoubleSpinBox()
                self.voiceInputMethodSubtitleAuditokMaxDurBox.setMinimum(1)
                self.voiceInputMethodSubtitleAuditokMaxDurBox.setValue(10)

                self.voiceInputMethodSubtitleAuditokMinSilenceDurHint = QLabel(self.tr('段内静音最长时间：'))
                self.voiceInputMethodSubtitleAuditokMinSilenceDurBox = QDoubleSpinBox()
                self.voiceInputMethodSubtitleAuditokMinSilenceDurBox.setMinimum(0.05)
                self.voiceInputMethodSubtitleAuditokMinSilenceDurBox.setSingleStep(0.1)
                self.voiceInputMethodSubtitleAuditokMinSilenceDurBox.setValue(0.2)

                self.voiceInputMethodSubtitleAuditokEnergyThresholdHint = HintLabel(self.tr('声音能量阈值：'))
                self.voiceInputMethodSubtitleAuditokEnergyThresholdHint.hint = self.tr(' 它是用 log10 dot(x, x) / |x| 计算出的能量的 log 值')
                self.voiceInputMethodSubtitleAuditokEnergyThresholdBox = QSpinBox()
                self.voiceInputMethodSubtitleAuditokEnergyThresholdBox.setMinimum(1)
                self.voiceInputMethodSubtitleAuditokEnergyThresholdBox.setValue(50)

                self.voiceInputMethodSubtitleAuditokInputMethodSleepTimeHint = HintLabel(self.tr('输入法休息时间：'))
                self.voiceInputMethodSubtitleAuditokInputMethodSleepTimeHint.hint = self.tr('每次输入完需要休息一下，否则在文字出来后很快再按下快捷键，语音输入法有可能响应不过来')
                self.voiceInputMethodSubtitleAuditokInputMethodSleepTimeBox = QDoubleSpinBox()
                self.voiceInputMethodSubtitleAuditokInputMethodSleepTimeBox.setMinimum(1)
                self.voiceInputMethodSubtitleAuditokInputMethodSleepTimeBox.setSingleStep(0.2)
                self.voiceInputMethodSubtitleAuditokInputMethodSleepTimeBox.setValue(3)

                # self.voiceInputMethodSubtitleEngineParamLayout = QGridLayout()

                self.voiceInputMethodSubtitleEngineParamLayout = QHBoxLayout()
                self.voiceInputMethodSubtitleEngineParamForm1 = QFormLayout()
                self.voiceInputMethodSubtitleEngineParamForm1.addRow(self.voiceInputMethodSubtitleVoiceInputShortcutLabel, self.voiceInputMethodSubtitleVoiceInputShortcutComboBox)
                self.voiceInputMethodSubtitleEngineParamForm1.addRow(self.voiceInputMethodSubtitleAuditokMinDurHint, self.voiceInputMethodSubtitleAuditokMinDurBox)
                self.voiceInputMethodSubtitleEngineParamForm1.addRow(self.voiceInputMethodSubtitleAuditokMinSilenceDurHint, self.voiceInputMethodSubtitleAuditokMinSilenceDurBox)
                self.voiceInputMethodSubtitleEngineParamForm2 = QFormLayout()
                self.voiceInputMethodSubtitleEngineParamForm2.addRow(self.voiceInputMethodSubtitleAuditokInputMethodSleepTimeHint, self.voiceInputMethodSubtitleAuditokInputMethodSleepTimeBox)
                self.voiceInputMethodSubtitleEngineParamForm2.addRow(self.voiceInputMethodSubtitleAuditokMaxDurHint, self.voiceInputMethodSubtitleAuditokMaxDurBox)
                self.voiceInputMethodSubtitleEngineParamForm2.addRow(self.voiceInputMethodSubtitleAuditokEnergyThresholdHint, self.voiceInputMethodSubtitleAuditokEnergyThresholdBox)
                self.voiceInputMethodSubtitleEngineParamLayout.addLayout(self.voiceInputMethodSubtitleEngineParamForm1,3)
                self.voiceInputMethodSubtitleEngineParamLayout.addWidget(QLabel(),1)
                self.voiceInputMethodSubtitleEngineParamLayout.addLayout(self.voiceInputMethodSubtitleEngineParamForm2,3)

            self.voiceInputMethodSubtitleHelpButton = QPushButton(self.tr('查看帮助'))
            self.voiceInputMethodSubtitleSoundControlPanelButton = QPushButton(self.tr('声音控制面板'))
            self.voiceInputMethodSubtitleHalfAutoRunButton = QPushButton(self.tr('开始半自动运行'))
            self.voiceInputMethodSubtitleFullAutoRunButton = QPushButton(self.tr('开始全自动运行'))
            self.voiceInputMethodSubtitleHelpButton.clicked.connect(self.voiceInputMethodSubtitleHelpButtonClicked)
            self.voiceInputMethodSubtitleSoundControlPanelButton.clicked.connect(self.voiceInputMethodSubtitleSoundControlPanelButtonClicked)
            self.voiceInputMethodSubtitleHalfAutoRunButton.clicked.connect(self.voiceInputMethodSubtitleHalfAutoRunButtonClicked)
            self.voiceInputMethodSubtitleFullAutoRunButton.clicked.connect(self.voiceInputMethodSubtitleFullAutoRunButtonClicked)
            self.voiceInputMethodSubtitleButtonLayout = QHBoxLayout()
            self.voiceInputMethodSubtitleButtonLayout.addWidget(self.voiceInputMethodSubtitleHelpButton)
            self.voiceInputMethodSubtitleButtonLayout.addWidget(self.voiceInputMethodSubtitleSoundControlPanelButton)
            self.voiceInputMethodSubtitleButtonLayout.addWidget(self.voiceInputMethodSubtitleHalfAutoRunButton)
            self.voiceInputMethodSubtitleButtonLayout.addWidget(self.voiceInputMethodSubtitleFullAutoRunButton)

            self.voiceInputMethodSubtitleInputBoxAndButtonLayout = QHBoxLayout()
            self.voiceInputMethodSubtitleInputBoxAndButtonLayout.addWidget(self.voiceInputMethodSubtitleInputEdit, 3)
            self.voiceInputMethodSubtitleInputBoxAndButtonLayout.addWidget(self.voiceInputMethodSubtitleInputButton, 1)
            self.voiceInputMethodSubtitleInputBoxAndButtonLayout.setContentsMargins(0,0,0,0)
            self.voiceInputMethodSubtitleInputBoxAndButtonBox = QWidget()
            self.voiceInputMethodSubtitleInputBoxAndButtonBox.setContentsMargins(0,0,0,0)
            self.voiceInputMethodSubtitleInputBoxAndButtonBox.setLayout(self.voiceInputMethodSubtitleInputBoxAndButtonLayout)

            self.voiceInputMethodSubtitleTimestampAuxiBoxAndButtonLayout = QHBoxLayout()
            self.voiceInputMethodSubtitleTimestampAuxiBoxAndButtonLayout.addWidget(self.voiceInputMethodSubtitleTimestampEdit, 3)
            self.voiceInputMethodSubtitleTimestampAuxiBoxAndButtonLayout.addWidget(self.voiceInputMethodSubtitleTimestampButton, 1)
            self.voiceInputMethodSubtitleTimestampAuxiBoxAndButtonLayout.setContentsMargins(0,0,0,0)
            self.voiceInputMethodSubtitleTimestampAuxiBoxAndButtonBox = QWidget()
            self.voiceInputMethodSubtitleTimestampAuxiBoxAndButtonBox.setContentsMargins(0, 0, 0, 0)
            self.voiceInputMethodSubtitleTimestampAuxiBoxAndButtonBox.setLayout(self.voiceInputMethodSubtitleTimestampAuxiBoxAndButtonLayout)

            self.voiceInputMethodSubtitleInputOutputFormLayout = QFormLayout()
            self.voiceInputMethodSubtitleInputOutputFormLayout.addRow(self.voiceInputMethodSubtitleInputHint, self.voiceInputMethodSubtitleInputBoxAndButtonBox)
            # self.voiceInputMethodSubtitleInputOutputFormLayout.addRow(self.voiceInputMethodSubtitleTimestampAuxHint, self.voiceInputMethodSubtitleTimestampAuxiBoxAndButtonBox)
            self.voiceInputMethodSubtitleInputOutputFormLayout.addRow(self.voiceInputMethodSubtitleOutputHint, self.voiceInputMethodSubtitleOutputEdit)



            self.voiceInputMethodSubtitleWidgetLayout.addLayout(self.voiceInputMethodSubtitleInputOutputFormLayout, 1, 0, 1, 3)
            #
            self.voiceInputMethodSubtitleWidgetLayout.addWidget(self.voiceInputMethodSubtitle可选时间段Hint, 3, 0, 1, 1)
            self.voiceInputMethodSubtitleWidgetLayout.addLayout(self.voiceInputMethodSubtitle截取时间hbox, 3, 1, 1, 2)


            self.voiceInputMethodSubtitleWidgetLayout.addWidget(QLabel('   '), 4, 0, 1, 3)
            self.voiceInputMethodSubtitleWidgetLayout.addLayout(self.voiceInputMethodSubtitleEngineParamLayout, 5, 0, 1, 3)

            self.voiceInputMethodSubtitleWidgetLayout.addWidget(QLabel('   '), 6, 0, 1, 3)
            self.voiceInputMethodSubtitleWidgetLayout.addLayout(self.voiceInputMethodSubtitleButtonLayout, 7, 0, 1, 3)
            self.voiceInputMethodSubtitleWidgetLayout.setSpacing(15)

        self.masterLayout.addWidget(self.fileTranscribeSubtitleGroup)
        self.masterLayout.addWidget(self.voiceInputMethodSubtitleGroup)

        self.masterLayout.addStretch(0)




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
        apis = 常量.conn.cursor().execute('select name from %s' % 常量.apiTableName).fetchall()
        self.fileTranscribeSubtitleEngineComboBox.clear()
        if apis != None:
            for api in apis:
                self.fileTranscribeSubtitleEngineComboBox.addItem(api[0])
            self.fileTranscribeSubtitleEngineComboBox.setCurrentIndex(0)
            pass
        # 不在这里关数据库了

    def voiceInputMethodSubtitleInputButtonClicked(self):
        filename = QFileDialog().getOpenFileName(self, self.tr('打开文件'), None, self.tr('所有文件(*)'))
        if filename[0] != '':
            self.voiceInputMethodSubtitleInputEdit.setText(filename[0]) # 设定输入文件名字
            self.voiceInputMethodSubtitleOutputName = os.path.splitext(filename[0])[0] + '.srt' # 得到输出字幕文字
            self.voiceInputMethodSubtitleOutputEdit.setText(self.voiceInputMethodSubtitleOutputName) # 输出字幕文件设定字幕路径
        return True

    def voiceInputMethodSubtitleTimestampButtonClicked(self):
        filename = QFileDialog().getOpenFileName(self, self.tr('打开文件'), None, self.tr('所有文件(*)'))
        if filename[0] != '':
            self.voiceInputMethodSubtitleTimestampEdit.setText(filename[0]) # 设定输入文件名字
        return True

    def voiceInputMethodSubtitleInputEditChanged(self):
        filename = self.voiceInputMethodSubtitleInputEdit.text()
        # if filename != '':
        self.voiceInputMethodSubtitleOutputName = os.path.splitext(filename)[0] + '.srt'
        self.voiceInputMethodSubtitleOutputEdit.setText(self.voiceInputMethodSubtitleOutputName)
        return True
    def voiceInputMethodSubtitleTimestampEditChanged(self):
        if self.voiceInputMethodSubtitleTimestampEdit.text() == '':
            self.voiceInputMethodSubtitleAuditokMinDurHint.setEnabled(True)
            self.voiceInputMethodSubtitleAuditokMinDurBox.setEnabled(True)
            self.voiceInputMethodSubtitleAuditokMaxDurHint.setEnabled(True)
            self.voiceInputMethodSubtitleAuditokMaxDurBox.setEnabled(True)
            self.voiceInputMethodSubtitleAuditokMinSilenceDurHint.setEnabled(True)
            self.voiceInputMethodSubtitleAuditokMinSilenceDurBox.setEnabled(True)
            self.voiceInputMethodSubtitleAuditokEnergyThresholdHint.setEnabled(True)
            self.voiceInputMethodSubtitleAuditokEnergyThresholdBox.setEnabled(True)
        else:
            self.voiceInputMethodSubtitleAuditokMinDurHint.setEnabled(False)
            self.voiceInputMethodSubtitleAuditokMinDurBox.setEnabled(False)
            self.voiceInputMethodSubtitleAuditokMaxDurHint.setEnabled(False)
            self.voiceInputMethodSubtitleAuditokMaxDurBox.setEnabled(False)
            self.voiceInputMethodSubtitleAuditokMinSilenceDurHint.setEnabled(False)
            self.voiceInputMethodSubtitleAuditokMinSilenceDurBox.setEnabled(False)
            self.voiceInputMethodSubtitleAuditokEnergyThresholdHint.setEnabled(False)
            self.voiceInputMethodSubtitleAuditokEnergyThresholdBox.setEnabled(False)
        return True

    # 帮助按钮
    def voiceInputMethodSubtitleHelpButtonClicked(self):
        webbrowser.open(self.tr('https://www.bilibili.com/video/BV1wT4y177kD/'))

    def voiceInputMethodSubtitleSoundControlPanelButtonClicked(self):
        if 常量.platfm == 'Windows':
            os.system('control /name Microsoft.Sound')
        else:
            QMessageBox.information(self, '提示', '这个功能用于打开 Window 上的声音控制面板，方便打开立体声混音，将扬声器输出作为麦克风输入，只在 Windows 上有用')



    # 半自动
    def voiceInputMethodSubtitleHalfAutoRunButtonClicked(self):
        # if

        if self.voiceInputMethodSubtitleInputEdit.text() != '':
            self.initializeVoiceInputMethodSubtitle(0)

    # 全自动
    def voiceInputMethodSubtitleFullAutoRunButtonClicked(self):
        if self.voiceInputMethodSubtitleInputEdit.text() != '':
            self.initializeVoiceInputMethodSubtitle(1)

    # 启动语音输入法转字幕
    def initializeVoiceInputMethodSubtitle(self, mode):

        min_dur = self.voiceInputMethodSubtitleAuditokMinDurBox.value()  # 最短时间
        max_dur = self.voiceInputMethodSubtitleAuditokMaxDurBox.value()  # 最长时间
        max_silence = self.voiceInputMethodSubtitleAuditokMinSilenceDurBox.value()  # 允许在这个片段中存在的静音片段的最长时间
        energy_threshold = self.voiceInputMethodSubtitleAuditokEnergyThresholdBox.value()
        inputMethodHotkeySleepTime = self.voiceInputMethodSubtitleAuditokInputMethodSleepTimeBox.value()

        inputFilePath = self.voiceInputMethodSubtitleInputEdit.text()
        timestampAuxiFilePath = self.voiceInputMethodSubtitleTimestampEdit.text()
        outputFilePath = self.voiceInputMethodSubtitleOutputEdit.text()
        shortcutOfInputMethod = self.voiceInputMethodSubtitleVoiceInputShortcutComboBox.currentText()
        userDefinedEndtime = strTimeToSecondsTime(self.voiceInputMethodSubtitle截取时间end输入框.text())  # 用户输入的终止时间
        try:
            inputFileLength = getMediaTimeLength(inputFilePath)  # 得到输入的视频文件时长
        except (RuntimeError, FileNotFoundError):
            # Catch the exception raised by pymediainfo.MediaInfo.parse
            QMessageBox.information(self, self.tr('输入文件有误'), self.tr('输入文件有误'))
            return
        startTime = strTimeToSecondsTime(self.voiceInputMethodSubtitle截取时间start输入框.text())  # 确定起始时间，如果起始输入框没输入的话，返回的起始时间就是0
        if userDefinedEndtime > 0: # 要是用户定义了时长
            endTime = userDefinedEndtime  # 结束时间就为用户定义的时间
        else:
            endTime = inputFileLength # 要不然结束时间还是视频文件时长

        transEngine = VoiciInputMethodTrans(shortcutOfInputMethod)
        transEngine.min_dur = min_dur
        transEngine.max_dur = max_dur
        transEngine.max_silence = max_silence
        transEngine.energy_threshold = energy_threshold
        transEngine.inputMethodHotkeySleepTime = inputMethodHotkeySleepTime

        if userDefinedEndtime > 0:
            endTime = userDefinedEndtime  # 结束时间为用户定义的时间
        else:
            # try:  其实这里的 try 是没有用的，加不加无所谓。因为在 getMediaTimeLength 里面已经有 try，会返回 0，真正会返回错误信息的是在下面转码 wav 文件那步。
            # 一个媒体的时长为0是显然不正常的，所以我们可以在返回 0 的时候报错，停止进程。因为此时新窗口还没有出来，没有报错的文本框，所以就以 QMessageBox 提醒了
            endTime = getMediaTimeLength(self.voiceInputMethodSubtitleInputEdit.text())  # 结束时间即为媒体时长
            if endTime == 0:
                QMessageBox.information(self, self.tr('输入文件有误'), self.tr('输入文件有误，请检查输入文件路径'))
                return
        startTime = strTimeToSecondsTime(self.voiceInputMethodSubtitle截取时间start输入框.text())  # 确定起始时间

        thread = VoiceInputMethodAutoSrtThread()  # 控制输入法进程

        ffmpegWavGenThread = FFmpegWavGenThread()  # 得到 wav 文件进程，就是在这一步里，如果输入文件有问题，那么就会在新窗口中报错
        ffmpegWavGenThread.mediaFile = inputFilePath # 输入文件
        ffmpegWavGenThread.startTime = startTime # 起始时间
        ffmpegWavGenThread.endTime = endTime

        window = VoiceInputMethodTranscribeSubtitleWindow(常量.mainWindow)  # 新窗口
        output = window.hintConsoleBox

        window.thread = thread
        window.transEngine = transEngine
        window.ffmpegWavGenThread = ffmpegWavGenThread
        window.mode = mode  # 零代表半自动模式
        window.inputFiePath = inputFilePath  # 输入路径
        window.timestampFile = timestampAuxiFilePath  # 时间戳辅助文件
        window.outputFilePath = outputFilePath  # 输出路径
        window.shortcutOfInputMethod = shortcutOfInputMethod  # 输入法的快捷键
        window.startTime = startTime  # 确定起始时间, 作为第一条字幕的起始时间
        window.initParams()
