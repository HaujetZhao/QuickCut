# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from moduels.component.MyQLine import MyQLine
from moduels.component.HintLabel import HintLabel
from moduels.component.HintCombobox import HintCombobox
from moduels.component.NormalValue import 常量
from moduels.gui.Console import Console
from moduels.tool.AutoEditThread import AutoEditThread

import re, os

class FFmpegAutoEditTab(QWidget):
    def __init__(self):
        super().__init__()
        self.preferenceTableName = 常量.首选项表名
        self.apiUpdateBroadCaster = 常量.apiUpdateBroadCaster
        self.initGui()

    def initGui(self):
        self.masterLayout = QVBoxLayout()

        # 输入输出文件部分
        self.GUI输入文件部分()

        # 一般选项
        self.GUI一般选项()

        # 运行按钮
        self.bottomButtonLayout = QHBoxLayout()
        self.runButton = QPushButton(self.tr('运行'))
        self.runButton.clicked.connect(self.runButtonClicked)
        # self.bottomButtonLayout.addWidget(self.runButton)

        self.masterLayout.addWidget(self.输入输出布局框)
        self.masterLayout.addStretch(0)
        self.masterLayout.addWidget(self.optionBox)
        self.masterLayout.addStretch(0)
        self.masterLayout.addWidget(self.runButton)

        self.setLayout(self.masterLayout)

    def GUI输入文件部分(self):
        self.输入输出布局 = QGridLayout()
        self.输入输出布局框 = QWidget()
        self.输入输出布局框.setLayout(self.输入输出布局)

        self.输入提示标签 = QLabel(self.tr('输入文件'))
        self.输出提示标签 = QLabel(self.tr('输出路径'))
        self.字幕提示标签 = QLabel(self.tr('辅助字幕'))

        self.输入路径框 = MyQLine()
        self.输入路径框.signal.connect(self.输入框有文件拖入)
        self.输出路径框 = MyQLine()
        self.字幕路径框 = MyQLine()

        # self.输入路径框.setText(r'D:/Users/Haujet/Desktop/vid.mp4')
        # self.输出路径框.setText(r'D:/Users/Haujet/Desktop/vid2.mp4')

        self.选择输入按钮 = QPushButton(self.tr('选择文件'))
        self.选择输入按钮.clicked.connect(self.选择输入按钮被按下)
        self.选择输出按钮 = QPushButton(self.tr('选择保存位置'))
        self.选择输出按钮.clicked.connect(self.选择输出按钮被按下)
        self.选择字幕按钮 = QPushButton(self.tr('选择辅助字幕'))
        self.选择字幕按钮.clicked.connect(self.选择字幕按钮被按下)

        self.输入输出布局.addWidget(self.输入提示标签, 0, 0, 1, 1)
        self.输入输出布局.addWidget(self.输入路径框, 0, 1, 1, 1)
        self.输入输出布局.addWidget(self.选择输入按钮, 0, 2, 1, 1)

        self.输入输出布局.addWidget(self.输出提示标签, 1, 0, 1, 1)
        self.输入输出布局.addWidget(self.输出路径框, 1, 1, 1, 1)
        self.输入输出布局.addWidget(self.选择输出按钮, 1, 2, 1, 1)

        self.输入输出布局.addWidget(self.字幕提示标签, 2, 0, 1, 1)
        self.输入输出布局.addWidget(self.字幕路径框, 2, 1, 1, 1)
        self.输入输出布局.addWidget(self.选择字幕按钮, 2, 2, 1, 1)

    def GUI一般选项(self):
        self.normalOptionLayout = QHBoxLayout()
        # self.normalOptionLayout.setVerticalSpacing(20)
        # self.normalOptionLayout.setHorizontalSpacing(100)

        self.quietSpeedFactorLabel = QLabel(self.tr('安静片段倍速：'))
        self.安静片段倍速编辑框 = QDoubleSpinBox()
        self.安静片段倍速编辑框.setMaximum(999999999)
        self.安静片段倍速编辑框.setAlignment(Qt.AlignCenter)
        self.安静片段倍速编辑框.setValue(8)
        self.安静片段倍速编辑框.setMinimum(1)
        self.soundedSpeedFactorLabel = QLabel(self.tr('响亮片段倍速：'))
        self.响亮片段倍速编辑框 = QDoubleSpinBox()
        self.响亮片段倍速编辑框.setMaximum(999999999)
        self.响亮片段倍速编辑框.setAlignment(Qt.AlignCenter)
        self.响亮片段倍速编辑框.setMinimum(1)
        self.响亮片段倍速编辑框.setValue(1)
        self.frameMarginLabel = QLabel(self.tr('片段间缓冲帧数：'))
        self.片段间缓冲帧数编辑框 = QSpinBox()
        self.片段间缓冲帧数编辑框.setAlignment(Qt.AlignCenter)
        self.片段间缓冲帧数编辑框.setValue(3)
        self.soundThresholdLabel = QLabel(self.tr('声音检测相对阈值：'))
        self.声音阈值编辑框 = QDoubleSpinBox()
        self.声音阈值编辑框.setMaximum(1)
        self.声音阈值编辑框.setAlignment(Qt.AlignCenter)
        self.声音阈值编辑框.setDecimals(3)
        self.声音阈值编辑框.setSingleStep(0.005)
        self.声音阈值编辑框.setValue(0.025)



        self.outputOptionHint = HintLabel(self.tr('输出文件选项：'))
        self.输出选项编辑框 = HintCombobox()
        self.输出选项编辑框.hint = self.tr('在这里可以选择对应你设备的硬件加速编码器，Intel 对应 qsv，AMD 对应 amf，Nvidia 对应 nvenc, 苹果电脑对应 videotoolbox')
        self.输出选项编辑框.setEditable(True)
        self.输出选项编辑框.addItem('-c:v libx264 -crf 23')
        self.输出选项编辑框.addItem('-c:v h264_qsv -qscale 15')
        self.输出选项编辑框.addItem('-c:v h264_amf -qscale 15')
        self.输出选项编辑框.addItem('-c:v h264_nvenc -qscale 15')
        self.输出选项编辑框.addItem('-c:v h264_videotoolbox -qscale 15')
        self.输出选项编辑框.addItem('-c:v libx265 -crf 23')
        self.输出选项编辑框.addItem('-c:v hevc_qsv -qscale 15')
        self.输出选项编辑框.addItem('-c:v hevc_amf -qscale 15')
        self.输出选项编辑框.addItem('-c:v hevc_nvenc -qscale 15')
        self.输出选项编辑框.addItem('-c:v hevc_videotoolbox -qscale 15')

        self.只处理音频开关 = QCheckBox(self.tr('只处理和输出音频，忽略视频（用于快速预览效果）'))

        self.使用辅助字幕开关 = QCheckBox(self.tr('使用辅助字幕，依据字幕中的关键句自动剪辑'))
        self.使用辅助字幕开关.clicked.connect(self.使用辅助字幕开关被单击)

        self.cutKeywordLabel = QLabel(self.tr('剪去片段关键句：'))
        self.剪去片段关键词编辑框 = QLineEdit()
        self.剪去片段关键词编辑框.setAlignment(Qt.AlignCenter)
        self.剪去片段关键词编辑框.setText(self.tr('删除'))
        self.saveKeywordLabel = QLabel(self.tr('保留片段关键句：'))
        self.保留片段关键词编辑框 = QLineEdit()
        self.保留片段关键词编辑框.setAlignment(Qt.AlignCenter)
        self.保留片段关键词编辑框.setText(self.tr('保留'))

        self.cutKeywordLabel.setEnabled(False)
        self.剪去片段关键词编辑框.setEnabled(False)
        self.saveKeywordLabel.setEnabled(False)
        self.保留片段关键词编辑框.setEnabled(False)
        self.字幕路径框.setEnabled(False)
        self.字幕提示标签.setEnabled(False)
        self.选择字幕按钮.setEnabled(False)



        self.form1 = QFormLayout()
        self.form1.setSpacing(10)
        self.form1.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow) # FieldsStayAtSizeHint 	ExpandingFieldsGrow AllNonFixedFieldsGrow
        self.form1.addRow(self.quietSpeedFactorLabel, self.安静片段倍速编辑框)
        self.form1.addRow(self.soundedSpeedFactorLabel, self.响亮片段倍速编辑框)
        self.form1.addWidget(QLabel())
        self.form1.addRow(self.frameMarginLabel, self.片段间缓冲帧数编辑框)
        self.form1.addRow(self.soundThresholdLabel, self.声音阈值编辑框)
        self.form1.setWidget(5, QFormLayout.SpanningRole, self.只处理音频开关)
        self.form1.addWidget(QLabel())
        self.form1.addRow(self.outputOptionHint, self.输出选项编辑框)
        self.form1.addWidget(QLabel())
        # self.form1.addWidget(self.subtitleKeywordAutocutSwitch)
        self.form1.setWidget(10, QFormLayout.SpanningRole, self.使用辅助字幕开关)
        self.form1.addRow(self.cutKeywordLabel, self.剪去片段关键词编辑框)
        self.form1.addRow(self.saveKeywordLabel, self.保留片段关键词编辑框)
        # self.form1.setWidget(11, QFormLayout.SpanningRole, self.subtitleKeywordAutocutSwitch)
        # self.form1.add(QLabel())



        # self.normalOptionLayout.addWidget(QLabel(),1)
        # self.normalOptionLayout.addLayout(self.form1,3)
        # self.normalOptionLayout.addWidget(QLabel(),1)


        self.optionBoxLayout = QHBoxLayout()
        self.optionBoxLayout.addWidget(QLabel(''), 1)
        self.optionBoxLayout.addLayout(self.form1, 3)
        self.optionBoxLayout.addWidget(QLabel(''), 1)
        self.optionBox = QWidget()
        self.optionBox.setLayout(self.optionBoxLayout)

    def 输入框有文件拖入(self, path):
        outputName = os.path.splitext(path)[0] + '_out' + os.path.splitext(path)[1]
        self.输出路径框.setText(outputName)
        return True

    def 选择输入按钮被按下(self):
        filename = QFileDialog().getOpenFileName(self, self.tr('打开文件'), None, self.tr('所有文件(*)'))
        if filename[0] != '':
            self.输入路径框.setText(filename[0])
            outputName = re.sub(r'(\.[^\.]+)$', r'_out\1', filename[0])
            self.输出路径框.setText(outputName)
        return True

    def 选择输出按钮被按下(self):
        filename = QFileDialog().getSaveFileName(self, self.tr('设置输出保存的文件名'), self.tr('输出视频.mp4'), self.tr('所有文件(*)'))
        self.输出路径框.setText(filename[0])
        return True

    def 选择字幕按钮被按下(self):
        filename = QFileDialog().getOpenFileName(self, self.tr('选择字幕文件'), None, self.tr('所有文件(*)'))
        if filename[0]:
            self.字幕路径框.setText(filename[0])
        return True
        ...

    def 使用辅助字幕开关被单击(self):
        if self.使用辅助字幕开关.isChecked() == 0:
            self.cutKeywordLabel.setEnabled(False)
            self.剪去片段关键词编辑框.setEnabled(False)
            self.saveKeywordLabel.setEnabled(False)
            self.保留片段关键词编辑框.setEnabled(False)
            self.字幕路径框.setEnabled(False)
            self.字幕提示标签.setEnabled(False)
            self.选择字幕按钮.setEnabled(False)
        else:
            self.cutKeywordLabel.setEnabled(True)
            self.剪去片段关键词编辑框.setEnabled(True)
            self.saveKeywordLabel.setEnabled(True)
            self.保留片段关键词编辑框.setEnabled(True)
            self.字幕路径框.setEnabled(True)
            self.字幕提示标签.setEnabled(True)
            self.选择字幕按钮.setEnabled(True)

    def runButtonClicked(self):
        if self.输入路径框.text() and self.输出路径框.text():
            控制台窗口 = Console(常量.mainWindow)

            重要信息输出框 = 控制台窗口.consoleBox
            FFmpeg信息输出框 = 控制台窗口.consoleBoxForFFmpeg

            线程 = AutoEditThread(常量.mainWindow)
            线程.output = 重要信息输出框
            线程.输入文件 = self.输入路径框.text()
            线程.输出文件 = self.输出路径框.text()
            线程.字幕文件 = self.字幕路径框.text()
            线程.静音片段倍速 = self.安静片段倍速编辑框.value()
            线程.响亮片段倍速 = self.响亮片段倍速编辑框.value()
            线程.片段间缓冲帧数 = self.片段间缓冲帧数编辑框.value()
            线程.静音阈值 = self.声音阈值编辑框.value()
            线程.只处理音频 = self.只处理音频开关.isChecked()
            线程.输出选项 = self.输出选项编辑框.currentText()
            线程.使用辅助字幕 = self.使用辅助字幕开关.isChecked()
            线程.剪去片段关键词 = self.剪去片段关键词编辑框.text()
            线程.保留片段关键词 = self.保留片段关键词编辑框.text()

            线程.signal.connect(重要信息输出框.print)
            线程.signalForFFmpeg.connect(FFmpeg信息输出框.print)

            控制台窗口.thread = 线程  # 把这里的剪辑子进程赋值给新窗口，这样新窗口就可以在关闭的时候也把进程退出

            线程.start()

