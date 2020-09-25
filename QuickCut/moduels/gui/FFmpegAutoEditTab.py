# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from moduels.component.MyQLine import MyQLine
from moduels.component.HintLabel import HintLabel
from moduels.component.HintCombobox import HintCombobox
from moduels.component.NormalValue import 常量
from moduels.gui.Console import Console
from moduels.tool.AutoEditThread import AutoEditThread

import re

class FFmpegAutoEditTab(QWidget):
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
        self.masterLayout = QVBoxLayout()

        # 输入输出文件部分
        if True:
            self.inputOutputLayout = QGridLayout()
            self.inputOutputLayoutBox = QWidget()
            self.inputOutputLayoutBox.setLayout(self.inputOutputLayout)
            self.inputHintLabel = QLabel(self.tr('输入文件'))
            self.outputHintLabel = QLabel(self.tr('输出路径'))
            self.inputLineEdit = MyQLine()
            self.inputLineEdit.signal.connect(self.lineEditHasDrop)
            self.outputLineEdit = MyQLine()
            self.chooseInputFileButton = QPushButton(self.tr('选择文件'))
            self.chooseInputFileButton.clicked.connect(self.chooseInputFileButtonClicked)
            self.chooseOutputFileButton = QPushButton(self.tr('选择保存位置'))
            self.chooseOutputFileButton.clicked.connect(self.chooseOutputFileButtonClicked)
            self.inputOutputLayout.addWidget(self.inputHintLabel, 0, 0, 1, 1)
            self.inputOutputLayout.addWidget(self.inputLineEdit, 0, 1, 1, 1)
            self.inputOutputLayout.addWidget(self.chooseInputFileButton, 0, 2, 1, 1)
            self.inputOutputLayout.addWidget(self.outputHintLabel, 1, 0, 1, 1)
            self.inputOutputLayout.addWidget(self.outputLineEdit, 1, 1, 1, 1)
            self.inputOutputLayout.addWidget(self.chooseOutputFileButton, 1, 2, 1, 1)



        # 一般选项
        if True:
            self.normalOptionLayout = QHBoxLayout()
            # self.normalOptionLayout.setVerticalSpacing(20)
            # self.normalOptionLayout.setHorizontalSpacing(100)

            self.quietSpeedFactorLabel = QLabel(self.tr('安静片段倍速：'))
            self.silentSpeedFactorEdit = QDoubleSpinBox()
            self.silentSpeedFactorEdit.setMaximum(999999999)
            self.silentSpeedFactorEdit.setAlignment(Qt.AlignCenter)
            self.silentSpeedFactorEdit.setValue(8)
            self.silentSpeedFactorEdit.setMinimum(1)
            self.soundedSpeedFactorLabel = QLabel(self.tr('响亮片段倍速：'))
            self.soundedSpeedFactorEdit = QDoubleSpinBox()
            self.soundedSpeedFactorEdit.setMaximum(999999999)
            self.soundedSpeedFactorEdit.setAlignment(Qt.AlignCenter)
            self.soundedSpeedFactorEdit.setMinimum(1)
            self.soundedSpeedFactorEdit.setValue(1)
            self.frameMarginLabel = QLabel(self.tr('片段间缓冲帧数：'))
            self.frameMarginEdit = QSpinBox()
            self.frameMarginEdit.setAlignment(Qt.AlignCenter)
            self.frameMarginEdit.setValue(3)
            self.soundThresholdLabel = QLabel(self.tr('声音检测相对阈值：'))
            self.soundThresholdEdit = QDoubleSpinBox()
            self.soundThresholdEdit.setMaximum(1)
            self.soundThresholdEdit.setAlignment(Qt.AlignCenter)
            self.soundThresholdEdit.setDecimals(3)
            self.soundThresholdEdit.setSingleStep(0.005)
            self.soundThresholdEdit.setValue(0.025)

            # print(self.soundedSpeedFactorEdit.DefaultStepType)
            self.extractFrameOptionHint = HintLabel(self.tr('提取帧选项：'))
            self.extractFrameOptionHint.hint = self.tr('这里可以选择硬件加速编码器、调整提取帧的质量')
            self.extractFrameOptionBox = HintCombobox()
            self.extractFrameOptionBox.setEditable(True)
            self.extractFrameOptionBox.hint = self.tr('这里可以选择硬件加速编码器、调整提取帧的质量')
            self.extractFrameOptionBox.addItems(['-c:v mjpeg -qscale:v 3', '-c:v mjpeg_qsv -qscale:v 3'])


            self.frameQualityLabel = QLabel(self.tr('提取帧质量：'))
            self.frameQualityEdit = QSpinBox()
            self.frameQualityEdit.setAlignment(Qt.AlignCenter)
            self.frameQualityEdit.setMinimum(1)
            self.frameQualityEdit.setValue(3)

            self.outputOptionHint = HintLabel(self.tr('输出文件选项：'))
            self.outputOptionHint.hint = self.tr('在这里可以选择对应你设备的硬件加速编码器，Intel 对应 qsv，AMD 对应 amf，Nvidia 对应 nvenc, 苹果电脑对应 videotoolbox')
            # self.outputOptionHint.mouse
            self.outputOptionBox = HintCombobox()
            self.outputOptionBox.hint = self.tr('在这里可以选择对应你设备的硬件加速编码器，Intel 对应 qsv，AMD 对应 amf，Nvidia 对应 nvenc, 苹果电脑对应 videotoolbox')
            self.outputOptionBox.setEditable(True)
            self.outputOptionBox.addItem('')
            self.outputOptionBox.addItem('-c:v h264_qsv -qscale 15')
            self.outputOptionBox.addItem('-c:v h264_amf -qscale 15')
            self.outputOptionBox.addItem('-c:v h264_nvenc -qscale 15')
            self.outputOptionBox.addItem('-c:v h264_videotoolbox -qscale 15')
            self.outputOptionBox.addItem('-c:v hevc_qsv -qscale 15')
            self.outputOptionBox.addItem('-c:v hevc_amf -qscale 15')
            self.outputOptionBox.addItem('-c:v hevc_nvenc -qscale 15')
            self.outputOptionBox.addItem('-c:v hevc_videotoolbox -qscale 15')



            self.subtitleKeywordAutocutSwitch = QCheckBox(self.tr('生成自动字幕并依据字幕中的关键句自动剪辑'))
            self.subtitleKeywordAutocutSwitch.clicked.connect(self.subtitleKeywordAutocutSwitchClicked)

            self.subtitleEngineLabel = QLabel(self.tr('字幕语音 API：'))
            self.subtitleEngineComboBox = QComboBox()
            ########改用主数据库
            apis = self.conn.cursor().execute('select name from %s' % self.apiTableName).fetchall()
            if apis != None:
                for api in apis:
                    self.subtitleEngineComboBox.addItem(api[0])
                self.subtitleEngineComboBox.setCurrentIndex(0)
                pass
            # 不在这里关数据库了()
            self.apiUpdateBroadCaster.signal.connect(self.updateEngineList)
            self.cutKeywordLabel = QLabel(self.tr('剪去片段关键句：'))
            self.cutKeywordLineEdit = QLineEdit()
            self.cutKeywordLineEdit.setAlignment(Qt.AlignCenter)
            self.cutKeywordLineEdit.setText(self.tr('删除'))
            self.saveKeywordLabel = QLabel(self.tr('保留片段关键句：'))
            self.saveKeywordLineEdit = QLineEdit()
            self.saveKeywordLineEdit.setAlignment(Qt.AlignCenter)
            self.saveKeywordLineEdit.setText(self.tr('保留'))

            self.subtitleEngineLabel.setEnabled(False)
            self.subtitleEngineComboBox.setEnabled(False)
            self.cutKeywordLabel.setEnabled(False)
            self.cutKeywordLineEdit.setEnabled(False)
            self.saveKeywordLabel.setEnabled(False)
            self.saveKeywordLineEdit.setEnabled(False)



            self.form1 = QFormLayout()
            self.form1.setSpacing(10)
            self.form1.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow) # FieldsStayAtSizeHint 	ExpandingFieldsGrow AllNonFixedFieldsGrow
            self.form1.addRow(self.quietSpeedFactorLabel, self.silentSpeedFactorEdit)
            self.form1.addRow(self.soundedSpeedFactorLabel, self.soundedSpeedFactorEdit)
            self.form1.addWidget(QLabel())
            self.form1.addRow(self.frameMarginLabel, self.frameMarginEdit)
            self.form1.addRow(self.soundThresholdLabel, self.soundThresholdEdit)
            self.form1.addWidget(QLabel())
            self.form1.addRow(self.extractFrameOptionHint, self.extractFrameOptionBox)
            self.form1.addRow(self.outputOptionHint, self.outputOptionBox)
            self.form1.addWidget(QLabel())
            self.form1.addWidget(QLabel())
            # self.form1.addWidget(self.subtitleKeywordAutocutSwitch)
            self.form1.setWidget(10, QFormLayout.SpanningRole, self.subtitleKeywordAutocutSwitch)
            self.form1.addRow(self.subtitleEngineLabel, self.subtitleEngineComboBox)
            self.form1.addRow(self.cutKeywordLabel, self.cutKeywordLineEdit)
            self.form1.addRow(self.saveKeywordLabel, self.saveKeywordLineEdit)
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


        # 运行按钮
        if True:
            self.bottomButtonLayout = QHBoxLayout()
            self.runButton = QPushButton(self.tr('运行'))
            self.runButton.clicked.connect(self.runButtonClicked)
            # self.bottomButtonLayout.addWidget(self.runButton)

        self.masterLayout.addWidget(self.inputOutputLayoutBox)
        self.masterLayout.addStretch(0)
        self.masterLayout.addWidget(self.optionBox)
        self.masterLayout.addStretch(0)
        self.masterLayout.addWidget(self.runButton)

        self.setLayout(self.masterLayout)

    def lineEditHasDrop(self, path):
        outputName = os.path.splitext(path)[0] + '_out' + os.path.splitext(path)[1]
        self.outputLineEdit.setText(outputName)
        return True

    def chooseInputFileButtonClicked(self):
        filename = QFileDialog().getOpenFileName(self, self.tr('打开文件'), None, self.tr('所有文件(*)'))
        if filename[0] != '':
            self.inputLineEdit.setText(filename[0])
            outputName = re.sub(r'(\.[^\.]+)$', r'_out\1', filename[0])
            self.outputLineEdit.setText(outputName)
        return True

    def chooseOutputFileButtonClicked(self):
        filename = QFileDialog().getSaveFileName(self, self.tr('设置输出保存的文件名'), self.tr('输出视频.mp4'), self.tr('所有文件(*)'))
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
            window = Console(常量.mainWindow)

            output = window.consoleBox
            outputForFFmpeg = window.consoleBoxForFFmpeg

            thread = AutoEditThread(常量.mainWindow)
            thread.output = output
            thread.inputFile = self.inputLineEdit.text()
            thread.outputFile = self.outputLineEdit.text()
            thread.silentSpeed = self.silentSpeedFactorEdit.value()
            thread.soundedSpeed = self.soundedSpeedFactorEdit.value()
            thread.frameMargin = self.frameMarginEdit.value()
            thread.silentThreshold = self.soundThresholdEdit.value()
            thread.extractFrameOption = self.extractFrameOptionBox.currentText()
            thread.ffmpegOutputOption = self.outputOptionBox.currentText()
            thread.whetherToUseOnlineSubtitleKeywordAutoCut = self.subtitleKeywordAutocutSwitch.isChecked()
            thread.apiEngine = self.subtitleEngineComboBox.currentText()
            thread.cutKeyword = self.cutKeywordLineEdit.text()
            thread.saveKeyword = self.saveKeywordLineEdit.text()

            thread.signal.connect(output.print)
            thread.signalForFFmpeg.connect(outputForFFmpeg.print)

            window.thread = thread  # 把这里的剪辑子进程赋值给新窗口，这样新窗口就可以在关闭的时候也把进程退出

            thread.start()

    def updateEngineList(self):
        ########改用主数据库
        apis = conn.cursor().execute('select name from %s' % apiTableName).fetchall()
        self.subtitleEngineComboBox.clear()
        if apis != None:
            for api in apis:
                self.subtitleEngineComboBox.addItem(api[0])
            self.subtitleEngineComboBox.setCurrentIndex(0)
            pass
        # 不在这里关数据库了
