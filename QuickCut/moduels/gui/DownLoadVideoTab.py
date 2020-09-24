# -*- coding: UTF-8 -*-

import os
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from moduels.component.MyQLine import MyQLine
from moduels.component.NormalValue import 常量

class DownLoadVideoTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initGui()

    def initGui(self):
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        self.userPath = os.path.expanduser('~').replace('\\', '/')
        self.userVideoPath = self.userPath + '/Videos'
        self.userDownloadPath = self.userPath + '/Downloads'
        self.userDesktopPath = self.userPath + '/Desktop'

        # annie
        if True:
            self.annieGroup = QGroupBox(self.tr('使用 Annie 下载视频'))
            self.annieLayout = QVBoxLayout()
            self.annieGroup.setLayout(self.annieLayout)
            self.masterLayout.addWidget(self.annieGroup)

            self.annieInputLinkHint = QLabel(self.tr('视频链接：'))
            self.annieInputBox = QLineEdit()
            self.annieSavePathHint = QLabel(self.tr('保存路径：'))
            self.annieSaveBox = QComboBox()
            self.annieSaveBox.setEditable(True)
            self.annieSaveBox.addItems(
                [self.userPath, self.userVideoPath, self.userDownloadPath, self.userDesktopPath])

            self.annieDownloadFormatHint = QLabel(self.tr('下载格式(流id)：'))
            self.annieDownloadFormatBox = QLineEdit()
            self.annieDownloadFormatBox.setPlaceholderText(self.tr('不填则默认下载最高画质'))
            self.annieDownloadFormatBox.setAlignment(Qt.AlignCenter)

            self.annieCookiesHint = QLabel('Cookies')
            self.annieCookiesBox = MyQLine()
            self.annieCookiesBox.setPlaceholderText(self.tr('默认不用填'))
            self.annieCookiesButton = QPushButton(self.tr('选择文件'))
            self.annieCookiesButton.clicked.connect(self.annieCookiesButtonClicked)

            self.annieProxyHint = QLabel(self.tr('代理：'))
            self.annieProxyBox = QComboBox()
            self.annieProxyBox.setEditable(True)
            self.annieProxyBox.addItems(
                ['', 'http://127.0.0.1:5000/', 'socks5://127.0.0.1:5000/'])

            self.anniePlayListBox = QCheckBox(self.tr('下载视频列表'))

            self.annieCheckInfoButton = QPushButton(self.tr('列出流id'))
            # self.annieCheckInfoButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            self.annieCheckInfoButton.clicked.connect(self.annieCheckInfoButtonClicked)
            self.annieDownloadButton = QPushButton(self.tr('开始下载视频'))
            self.annieDownloadButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            self.annieDownloadButton.clicked.connect(self.annieDownloadButtonClicked)

            self.annieInputLinkWidgetLayout = QHBoxLayout()  # 输入链接
            self.annieInputLinkWidgetLayout.addWidget(self.annieInputBox, 2)
            self.annieInputLinkWidgetLayout.addWidget(self.anniePlayListBox, 1)
            self.annieInputLinkWidgetLayout.setContentsMargins(0,0,0,0)
            self.annieInputLinkWidget = QWidget()
            self.annieInputLinkWidget.setLayout(self.annieInputLinkWidgetLayout)
            self.annieInputLinkWidget.setContentsMargins(0,0,0,0)

            self.annieStreamIdWidgetLayout = QHBoxLayout() # 流 id
            self.annieStreamIdWidgetLayout.addWidget(self.annieDownloadFormatBox, 2)
            self.annieStreamIdWidgetLayout.addWidget(self.annieCheckInfoButton, 1)
            self.annieStreamIdWidgetLayout.setContentsMargins(0, 0, 0, 0)
            self.annieStreamIdWidget = QWidget()
            self.annieStreamIdWidget.setLayout(self.annieStreamIdWidgetLayout)
            self.annieStreamIdWidget.setContentsMargins(0, 0, 0, 0)

            self.annieCookiesWidgetLayout = QHBoxLayout() # cookies
            self.annieCookiesWidgetLayout.addWidget(self.annieCookiesBox, 2)
            self.annieCookiesWidgetLayout.addWidget(self.annieCookiesButton, 1)
            self.annieCookiesWidgetLayout.setContentsMargins(0, 0, 0, 0)
            self.annieCookiesWidget = QWidget()
            self.annieCookiesWidget.setLayout(self.annieCookiesWidgetLayout)
            self.annieCookiesWidget.setContentsMargins(0, 0, 0, 0)


            self.annieFormLayout = QFormLayout()
            self.annieFormLayout.addRow(self.annieInputLinkHint, self.annieInputLinkWidget)
            self.annieFormLayout.addRow(self.annieSavePathHint, self.annieSaveBox)
            self.annieFormLayout.addRow(self.annieDownloadFormatHint, self.annieStreamIdWidget)
            self.annieFormLayout.addRow(self.annieCookiesHint, self.annieCookiesWidget)
            self.annieFormLayout.addRow(self.annieProxyHint, self.annieProxyBox)

            self.annieHboxLayout = QHBoxLayout()
            self.annieHboxLayout.setContentsMargins(0, 0, 0, 0)
            self.annieHboxLayout.addLayout(self.annieFormLayout, 3)
            self.annieHboxLayout.addWidget(self.annieDownloadButton, 0)

            self.annieLayout.addLayout(self.annieHboxLayout)# 在主垂直布局添加选项的表单布局
            self.annieLayout.addStretch(1)


        self.masterLayout.addSpacing(5)

        # you-get
        if True:
            self.youGetGroup = QGroupBox(self.tr('使用 You-Get 下载视频'))
            self.youGetLayout = QVBoxLayout()
            self.youGetGroup.setLayout(self.youGetLayout)
            self.masterLayout.addWidget(self.youGetGroup)

            self.youGetInputLinkHint = QLabel(self.tr('视频链接：'))
            self.youGetInputBox = QLineEdit()
            self.youGetSavePathHint = QLabel(self.tr('保存路径：'))
            self.youGetSaveBox = QComboBox()
            self.youGetSaveBox.setEditable(True)
            self.youGetSaveBox.addItems(
                [self.userPath, self.userVideoPath, self.userDownloadPath, self.userDesktopPath])

            self.youGetDownloadFormatHint = QLabel(self.tr('下载格式(流id)：'))
            self.youGetDownloadFormatBox = QLineEdit()
            self.youGetDownloadFormatBox.setPlaceholderText(self.tr('不填则默认下载最高画质'))
            self.youGetDownloadFormatBox.setAlignment(Qt.AlignCenter)

            self.youGetCookiesHint = QLabel('Cookies')
            self.youGetCookiesBox = MyQLine()
            self.youGetCookiesBox.setPlaceholderText(self.tr('默认不用填'))
            self.youGetCookiesButton = QPushButton(self.tr('选择文件'))
            self.youGetCookiesButton.clicked.connect(self.youGetCookiesButtonClicked)

            self.youGetProxyHint = QLabel(self.tr('代理：'))
            self.youGetProxyBox = QComboBox()
            self.youGetProxyBox.setEditable(True)
            self.youGetProxyBox.addItems(
                ['--no-proxy', '--http-proxy 127.0.0.1:5000', '--extractor-proxy 127.0.0.1:5000',
                 '--socks-proxy 127.0.0.1:5000'])

            self.youGetPlayListBox = QCheckBox(self.tr('下载视频列表'))

            self.youGetCheckInfoButton = QPushButton(self.tr('列出流id'))
            # self.youGetCheckInfoButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            self.youGetCheckInfoButton.clicked.connect(self.youGetCheckInfoButtonClicked)
            self.youGetDownloadButton = QPushButton(self.tr('开始下载视频'))
            self.youGetDownloadButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            self.youGetDownloadButton.clicked.connect(self.youGetDownloadButtonClicked)

            self.youGetInputLinkWidgetLayout = QHBoxLayout()  # 输入链接
            self.youGetInputLinkWidgetLayout.addWidget(self.youGetInputBox, 2)
            self.youGetInputLinkWidgetLayout.addWidget(self.youGetPlayListBox, 1)
            self.youGetInputLinkWidgetLayout.setContentsMargins(0, 0, 0, 0)
            self.youGetInputLinkWidget = QWidget()
            self.youGetInputLinkWidget.setLayout(self.youGetInputLinkWidgetLayout)
            self.youGetInputLinkWidget.setContentsMargins(0, 0, 0, 0)

            self.youGetStreamIdWidgetLayout = QHBoxLayout()  # 流 id
            self.youGetStreamIdWidgetLayout.addWidget(self.youGetDownloadFormatBox, 2)
            self.youGetStreamIdWidgetLayout.addWidget(self.youGetCheckInfoButton, 1)
            self.youGetStreamIdWidgetLayout.setContentsMargins(0, 0, 0, 0)
            self.youGetStreamIdWidget = QWidget()
            self.youGetStreamIdWidget.setLayout(self.youGetStreamIdWidgetLayout)
            self.youGetStreamIdWidget.setContentsMargins(0, 0, 0, 0)

            self.youGetCookiesWidgetLayout = QHBoxLayout()  # cookies
            self.youGetCookiesWidgetLayout.addWidget(self.youGetCookiesBox, 2)
            self.youGetCookiesWidgetLayout.addWidget(self.youGetCookiesButton, 1)
            self.youGetCookiesWidgetLayout.setContentsMargins(0, 0, 0, 0)
            self.youGetCookiesWidget = QWidget()
            self.youGetCookiesWidget.setLayout(self.youGetCookiesWidgetLayout)
            self.youGetCookiesWidget.setContentsMargins(0, 0, 0, 0)

            self.youGetFormLayout = QFormLayout()
            self.youGetFormLayout.addRow(self.youGetInputLinkHint, self.youGetInputLinkWidget)
            self.youGetFormLayout.addRow(self.youGetSavePathHint, self.youGetSaveBox)
            self.youGetFormLayout.addRow(self.youGetDownloadFormatHint, self.youGetStreamIdWidget)
            self.youGetFormLayout.addRow(self.youGetCookiesHint, self.youGetCookiesWidget)
            self.youGetFormLayout.addRow(self.youGetProxyHint, self.youGetProxyBox)

            self.youGetHboxLayout = QHBoxLayout()
            self.youGetHboxLayout.setContentsMargins(0, 0, 0, 0)
            self.youGetHboxLayout.addLayout(self.youGetFormLayout, 3)
            self.youGetHboxLayout.addWidget(self.youGetDownloadButton, 0)

            self.youGetLayout.addLayout(self.youGetHboxLayout)  # 在主垂直布局添加选项的表单布局
            self.youGetLayout.addStretch(1)


        self.masterLayout.addSpacing(5)

        # youtube-dl
        if True:
            self.youTubeDlGroup = QGroupBox(self.tr('使用 Youtube-dl 下载视频'))
            self.youTubeDlLayout = QVBoxLayout()
            self.youTubeDlGroup.setLayout(self.youTubeDlLayout)
            self.masterLayout.addWidget(self.youTubeDlGroup)

            self.youTubeDlInputLinkHint = QLabel(self.tr('视频链接：'))
            self.youTubeDlInputBox = QLineEdit()
            self.youTubeDlSavePathHint = QLabel(self.tr('保存路径：'))
            self.youTubeDlSaveBox = QComboBox()
            self.youTubeDlSaveBox.setEditable(True)
            self.youTubeDlSaveBox.addItems(
                [self.userVideoPath, self.userPath, self.userDownloadPath, self.userDesktopPath])

            self.youTubeDlSaveNameFormatHint = QLabel(self.tr('文件命名格式：'))
            self.youTubeDlSaveNameFormatBox = QLineEdit()
            self.youTubeDlSaveNameFormatBox.setReadOnly(True)
            self.youTubeDlSaveNameFormatBox.setPlaceholderText(self.tr('不填则使用默认下载名'))
            self.youTubeDlSaveNameFormatBox.setText(
                '%(title)s from：%(uploader)s %(resolution)s %(fps)s fps %(id)s.%(ext)s')

            self.youTubeDlDownloadFormatHint = QLabel(self.tr('格式id：'))
            self.youTubeDlDownloadFormatBox = QLineEdit()
            self.youTubeDlDownloadFormatBox.setPlaceholderText(self.tr('不填则默认下载最高画质'))
            self.youTubeDlDownloadFormatBox.setAlignment(Qt.AlignCenter)

            self.youTubeDlOnlyDownloadSubtitleBox = QCheckBox(self.tr('只下载字幕'))

            self.youTubeDlCookiesHint = QLabel('Cookies')
            self.youTubeDlCookiesBox = MyQLine()
            self.youTubeDlCookiesBox.setPlaceholderText(self.tr('默认不用填'))
            self.youTubeDlCookiesButton = QPushButton(self.tr('选择文件'))
            self.youTubeDlCookiesButton.clicked.connect(self.youtubeDlCookiesButtonClicked)

            self.youTubeDlProxyHint = QLabel(self.tr('代理：'))
            self.youTubeDlProxyBox = QComboBox()
            self.youTubeDlProxyBox.setEditable(True)
            self.youTubeDlProxyBox.addItems(['', 'socks5://127.0.0.1:5000', '127.0.0.1:5000'])

            self.youTubeDlCheckInfoButton = QPushButton(self.tr('列出格式id'))
            # self.youTubeDlCheckInfoButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            self.youTubeDlCheckInfoButton.clicked.connect(self.youTubeDlCheckInfoButtonClicked)
            self.youTubeDlDownloadButton = QPushButton(self.tr('开始下载视频'))
            self.youTubeDlDownloadButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            self.youTubeDlDownloadButton.clicked.connect(self.youTubeDlDownloadButtonClicked)

            self.youTubeDlInputLinkWidgetLayout = QHBoxLayout()  # 输入链接
            self.youTubeDlInputLinkWidgetLayout.addWidget(self.youTubeDlInputBox, 2)
            self.youTubeDlInputLinkWidgetLayout.addWidget(self.youTubeDlOnlyDownloadSubtitleBox, 1)
            self.youTubeDlInputLinkWidgetLayout.setContentsMargins(0, 0, 0, 0)
            self.youTubeDlInputLinkWidget = QWidget()
            self.youTubeDlInputLinkWidget.setLayout(self.youTubeDlInputLinkWidgetLayout)
            self.youTubeDlInputLinkWidget.setContentsMargins(0, 0, 0, 0)

            self.youTubeDlStreamIdWidgetLayout = QHBoxLayout()  # 流 id
            self.youTubeDlStreamIdWidgetLayout.addWidget(self.youTubeDlDownloadFormatBox, 2)
            self.youTubeDlStreamIdWidgetLayout.addWidget(self.youTubeDlCheckInfoButton, 1)
            self.youTubeDlStreamIdWidgetLayout.setContentsMargins(0, 0, 0, 0)
            self.youTubeDlStreamIdWidget = QWidget()
            self.youTubeDlStreamIdWidget.setLayout(self.youTubeDlStreamIdWidgetLayout)
            self.youTubeDlStreamIdWidget.setContentsMargins(0, 0, 0, 0)

            self.youTubeDlCookiesWidgetLayout = QHBoxLayout()  # cookies
            self.youTubeDlCookiesWidgetLayout.addWidget(self.youTubeDlCookiesBox, 2)
            self.youTubeDlCookiesWidgetLayout.addWidget(self.youTubeDlCookiesButton, 1)
            self.youTubeDlCookiesWidgetLayout.setContentsMargins(0, 0, 0, 0)
            self.youTubeDlCookiesWidget = QWidget()
            self.youTubeDlCookiesWidget.setLayout(self.youTubeDlCookiesWidgetLayout)
            self.youTubeDlCookiesWidget.setContentsMargins(0, 0, 0, 0)

            self.youTubeDlFormLayout = QFormLayout()
            self.youTubeDlFormLayout.addRow(self.youTubeDlInputLinkHint, self.youTubeDlInputLinkWidget)
            self.youTubeDlFormLayout.addRow(self.youTubeDlSavePathHint, self.youTubeDlSaveBox)
            self.youTubeDlFormLayout.addRow(self.youTubeDlSaveNameFormatHint, self.youTubeDlSaveNameFormatBox)
            self.youTubeDlFormLayout.addRow(self.youTubeDlDownloadFormatHint, self.youTubeDlStreamIdWidget)
            self.youTubeDlFormLayout.addRow(self.youTubeDlCookiesHint, self.youTubeDlCookiesWidget)
            self.youTubeDlFormLayout.addRow(self.youTubeDlProxyHint, self.youTubeDlProxyBox)

            self.youTubeDlHboxLayout = QHBoxLayout()
            self.youTubeDlHboxLayout.setContentsMargins(0, 0, 0, 0)
            self.youTubeDlHboxLayout.addLayout(self.youTubeDlFormLayout, 3)
            self.youTubeDlHboxLayout.addWidget(self.youTubeDlDownloadButton, 0)

            self.youTubeDlLayout.addLayout(self.youTubeDlHboxLayout)  # 在主垂直布局添加选项的表单布局
            self.youTubeDlLayout.addStretch(1)


    def annieCookiesButtonClicked(self):
        filename = QFileDialog().getOpenFileName(self, self.tr('打开文件'), None, self.tr('所有文件(*)'))
        if filename[0] != '':
            self.annieCookiesBox.setText(filename[0])
        return True

    def youGetCookiesButtonClicked(self):
        filename = QFileDialog().getOpenFileName(self, self.tr('打开文件'), None, self.tr('所有文件(*)'))
        if filename[0] != '':
            self.youGetCookiesBox.setText(filename[0])
        return True

    def youtubeDlCookiesButtonClicked(self):
        filename = QFileDialog().getOpenFileName(self, self.tr('打开文件'), None, self.tr('所有文件(*)'))
        if filename[0] != '':
            self.youTubeDlCookiesBox.setText(filename[0])
        return True

    def annieCheckInfoButtonClicked(self):
        try:
            os.environ.pop('HTTP_PROXY')
        except:
            pass
        if self.annieInputBox.text != '':
            finalCommand = '''annie'''
            if self.annieCookiesBox.text() != '':
                finalCommand += ''' -c %s''' % self.annieCookiesBox.text()
            if self.annieProxyBox.currentText() != '':
                os.environ.update(dict({'HTTP_PROXY':self.annieProxyBox.currentText()}))
            finalCommand += ''' -i %s''' % self.annieInputBox.text()
            thread = CommandThread()
            thread.command = finalCommand
            window = Console(mainWindow)
            window.thread = thread
            output = window.consoleBox
            outputForFFmpeg = window.consoleBoxForFFmpeg
            thread.output = output
            thread.signal.connect(output.print)
            thread.signalForFFmpeg.connect(outputForFFmpeg.print)
            thread.start()

    def youGetCheckInfoButtonClicked(self):
        if self.youGetInputBox.text != '':
            finalCommand = '''you-get'''
            if self.youGetCookiesBox.text() != '':
                finalCommand += ''' --cookies %s''' % self.youGetCookiesBox.text()
            if self.youGetProxyBox.currentText() != '':
                finalCommand += ''' %s''' % self.youGetProxyBox.currentText()
            finalCommand += ''' -i %s''' % self.youGetInputBox.text()
            thread = CommandThread()
            thread.command = finalCommand
            window = Console(mainWindow)
            window.thread = thread
            output = window.consoleBox
            outputForFFmpeg = window.consoleBoxForFFmpeg
            thread.output = output
            thread.signal.connect(output.print)
            thread.signalForFFmpeg.connect(outputForFFmpeg.print)
            thread.start()

    def youTubeDlCheckInfoButtonClicked(self):
        if self.youTubeDlInputBox.text != '':
            finalCommand = '''youtube-dl'''
            if self.youTubeDlCookiesBox.text() != '':
                finalCommand += ''' --cookies %s''' % self.youTubeDlCookiesBox.text()
            if self.youTubeDlProxyBox.currentText() != '':
                finalCommand += ''' --proxy %s''' % self.youTubeDlProxyBox.currentText()
            finalCommand += ''' -F %s''' % self.youTubeDlInputBox.text()
            thread = CommandThread()
            thread.command = finalCommand
            window = Console(mainWindow)
            window.thread = thread
            output = window.consoleBox
            outputForFFmpeg = window.consoleBoxForFFmpeg
            thread.output = output
            thread.signal.connect(output.print)
            thread.signalForFFmpeg.connect(outputForFFmpeg.print)
            thread.start()

    def annieDownloadButtonClicked(self):
        try:
            os.environ.pop('HTTP_PROXY')
        except:
            pass
        if self.annieInputBox.text != '':
            finalCommand = '''annie -C'''
            if self.annieSaveBox.currentText() != '':
                finalCommand += ''' -o "%s"''' % self.annieSaveBox.currentText()
            if self.annieDownloadFormatBox.text() != '':
                finalCommand += ''' -f %s''' % self.annieDownloadFormatBox.text()
            if self.annieCookiesBox.text() != '':
                finalCommand += ''' -c "%s"''' % self.annieCookiesBox.text()
            if self.annieProxyBox.currentText() != '':
                os.environ.update(dict({'HTTP_PROXY':self.annieProxyBox.currentText()}))
            if self.anniePlayListBox.isChecked() != False:
                finalCommand += ''' -p'''
            finalCommand += ''' %s''' % self.annieInputBox.text()
            thread = CommandThread()
            thread.command = finalCommand
            window = Console(mainWindow)
            window.thread = thread
            output = window.consoleBox
            outputForFFmpeg = window.consoleBoxForFFmpeg
            thread.output = output
            thread.signal.connect(output.print)
            thread.signalForFFmpeg.connect(outputForFFmpeg.print)
            thread.start()

    def youGetDownloadButtonClicked(self):
        if self.youGetInputBox.text != '':
            finalCommand = '''you-get -f'''
            if self.youGetSaveBox.currentText() != '':
                finalCommand += ''' -o "%s"''' % self.youGetSaveBox.currentText()
            if self.youGetDownloadFormatBox.text() != '':
                finalCommand += ''' --format %s''' % self.youGetDownloadFormatBox.text()
            if self.youGetCookiesBox.text() != '':
                finalCommand += ''' --cookies "%s"''' % self.youGetCookiesBox.text()
            if self.youGetProxyBox.currentText() != '':
                finalCommand += ''' %s''' % self.youGetProxyBox.currentText()
            if self.youGetPlayListBox.isChecked() != False:
                finalCommand += ''' --playlist'''
            finalCommand += ''' %s''' % self.youGetInputBox.text()
            thread = CommandThread()
            thread.command = finalCommand
            window = Console(mainWindow)
            window.thread = thread
            output = window.consoleBox
            outputForFFmpeg = window.consoleBoxForFFmpeg
            thread.output = output
            thread.signal.connect(output.print)
            thread.signalForFFmpeg.connect(outputForFFmpeg.print)
            thread.start()

    def youTubeDlDownloadButtonClicked(self):
        if self.youTubeDlInputBox.text != '':
            finalCommand = '''youtube-dl --write-sub --all-subs'''
            if self.youTubeDlSaveBox.currentText() != '':
                outputFolder = self.youTubeDlSaveBox.currentText()
                if self.youTubeDlSaveBox.currentText()[-1] != '/':
                    outputFolder += '/'
                finalCommand += ''' -o "%s''' % outputFolder
            if self.youTubeDlSaveNameFormatBox.text() != '':
                finalCommand += '''%s"''' % self.youTubeDlSaveNameFormatBox.text()
            if self.youTubeDlCookiesBox.text() != '':
                finalCommand += ''' --cookies "%s"''' % self.youTubeDlCookiesBox.text()
            if self.youTubeDlProxyBox.currentText() != '':
                finalCommand += ''' --proxy %s''' % self.youTubeDlProxyBox.currentText()
            if self.youTubeDlDownloadFormatBox.text() != '':
                finalCommand += ''' -f %s''' % self.youTubeDlDownloadFormatBox.text()
            if self.youTubeDlOnlyDownloadSubtitleBox.isChecked() != False:
                finalCommand += ''' --skip-download'''
            finalCommand += ''' %s''' % self.youTubeDlInputBox.text()
            thread = CommandThread()
            thread.command = finalCommand
            window = Console(mainWindow)
            window.thread = thread
            output = window.consoleBox
            outputForFFmpeg = window.consoleBoxForFFmpeg
            thread.output = output
            thread.signal.connect(output.print)
            thread.signalForFFmpeg.connect(outputForFFmpeg.print)
            thread.start()
