class FFmpegSplitVideoTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initGui()

    def initGui(self):
        self.masterLayout = QVBoxLayout()


        # self.masterLayout.addStretch(0)

        self.setLayout(self.masterLayout)

        # 输出文件选项
        if True:
            self.ffmpegOutputOptionGroup = QGroupBox(self.tr('总选项'))
            self.masterLayout.addWidget(self.ffmpegOutputOptionGroup)
            self.ffmpegOutputOptionLayout = QGridLayout()
            self.ffmpegOutputOptionGroup.setLayout(self.ffmpegOutputOptionLayout)
            self.ffmpegOutputOptionHint = HintLabel(self.tr('输出文件选项(默认可为空，但可选硬件加速)：'))
            self.ffmpegOutputOptionHint.hint = self.tr('在这里可以选择对应你设备的硬件加速编码器，Intel 对应 qsv，AMD 对应 amf，Nvidia 对应 nvenc, 苹果电脑对应 videotoolbox')
            self.ffmpegOutputOptionBox = HintCombobox()
            self.ffmpegOutputOptionBox.hint = self.tr('在这里可以选择对应你设备的硬件加速编码器，Intel 对应 qsv，AMD 对应 amf，Nvidia 对应 nvenc, 苹果电脑对应 videotoolbox')
            self.ffmpegOutputOptionBox.setEditable(True)
            self.ffmpegOutputOptionBox.addItem('')
            self.ffmpegOutputOptionBox.addItem('-c:v h264_qsv -qscale 15')
            self.ffmpegOutputOptionBox.addItem('-c:v h264_amf -qscale 15')
            self.ffmpegOutputOptionBox.addItem('-c:v h264_nvenc -qscale 15')
            self.ffmpegOutputOptionBox.addItem('-c:v h264_videotoolbox -qscale 15')
            self.ffmpegOutputOptionBox.addItem('-c:v hevc_qsv -qscale 15')
            self.ffmpegOutputOptionBox.addItem('-c:v hevc_amf -qscale 15')
            self.ffmpegOutputOptionBox.addItem('-c:v hevc_nvenc -qscale 15')
            self.ffmpegOutputOptionBox.addItem('-c:v hevc_videotoolbox -qscale 15')
            self.ffmpegOutputOptionLayout.addWidget(self.ffmpegOutputOptionHint, 0, 0, 1, 1)
            self.ffmpegOutputOptionLayout.addWidget(self.ffmpegOutputOptionBox, 0, 1, 1, 2)

        self.masterLayout.addSpacing(5)

        # 根据字幕分割片段
        if True:
            self.subtitleSplitVideoGroup = QGroupBox(self.tr('对字幕中的每一句剪出对应的视频片段'))
            self.subtitleSplitVideoLayout = QVBoxLayout()
            self.subtitleSplitVideoGroup.setLayout(self.subtitleSplitVideoLayout)
            self.masterLayout.addWidget(self.subtitleSplitVideoGroup)

            self.subtitleSplitInputHint = QLabel(self.tr('输入视频：'))
            self.subtitleSplitInputBox = MyQLine()
            self.subtitleSplitInputBox.textChanged.connect(self.setSubtitleSplitOutputFolder)
            self.subtitleSplitInputButton = QPushButton(self.tr('选择文件'))
            self.subtitleSplitInputButton.clicked.connect(self.subtitleSplitInputButtonClicked)

            self.subtitleHint = QLabel(self.tr('输入字幕：'))
            self.subtitleSplitSubtitleFileInputBox = MyQLine()
            self.subtitleSplitSubtitleFileInputBox.setPlaceholderText(self.tr('支持 srt、ass、vtt 字幕，或者内置字幕的 mkv'))
            self.subtitleButton = QPushButton(self.tr('选择文件'))
            self.subtitleButton.clicked.connect(self.subtitleSplitSubtitleFileInputButtonClicked)

            self.outputHint = QLabel(self.tr('输出文件夹：'))
            self.subtitleSplitOutputBox = QLineEdit()
            self.subtitleSplitOutputBox.setReadOnly(True)

            self.subtitleSplitSwitch = QCheckBox(self.tr('指定时间段'))
            self.subtitleSplitStartTimeHint = QLabel(self.tr('起始时刻：'))
            self.subtitleSplitStartTimeHint.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.subtitleSplitStartTimeBox = QLineEdit()
            self.subtitleSplitStartTimeBox.setAlignment(Qt.AlignCenter)
            self.subtitleSplitEndTimeHint = QLabel(self.tr('截止时刻：'))
            self.subtitleSplitEndTimeHint.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.subtitleSplitEndTimeBox = QLineEdit()
            self.subtitleSplitEndTimeBox.setAlignment(Qt.AlignCenter)

            self.timeValidator = QRegExpValidator(self)
            self.timeValidator.setRegExp(QRegExp(r'[0-9]{0,2}:?[0-9]{0,2}:?[0-9]{0,2}\.?[0-9]{0,2}'))
            self.subtitleSplitStartTimeBox.setValidator(self.timeValidator)
            self.subtitleSplitEndTimeBox.setValidator(self.timeValidator)

            self.subtitleSplitStartTimeHint.hide()
            self.subtitleSplitStartTimeBox.hide()
            self.subtitleSplitEndTimeHint.hide()
            self.subtitleSplitEndTimeBox.hide()
            self.subtitleSplitSwitch.clicked.connect(self.onSubtitleSplitSwitchClicked)

            self.subtitleOffsetHint = QLabel(self.tr('字幕时间偏移：'))
            self.subtitleOffsetBox = QDoubleSpinBox()
            self.subtitleOffsetBox.setAlignment(Qt.AlignCenter)
            self.subtitleOffsetBox.setDecimals(2)
            self.subtitleOffsetBox.setValue(0)
            self.subtitleOffsetBox.setMinimum(-100)
            self.subtitleOffsetBox.setSingleStep(0.1)

            self.exportClipSubtitleSwitch = QCheckBox(self.tr('同时导出分段srt字幕'))
            self.exportClipSubtitleSwitch.setChecked(True)

            self.subtitleNumberPerClipHint = QLabel(self.tr('每多少句剪为一段：'))
            self.subtitleNumberPerClipHint.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.subtitleNumberPerClipBox = QSpinBox()
            self.subtitleNumberPerClipBox.setValue(1)
            self.subtitleNumberPerClipBox.setAlignment(Qt.AlignCenter)
            self.subtitleNumberPerClipBox.setMinimum(1)

            self.subtitleSplitButton = QPushButton(self.tr('运行'))
            self.subtitleSplitButton.clicked.connect(self.onSubtitleSplitRunButtonClicked)
            self.subtitleSplitButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

            self.subtitleSplitVideoInputWidgetLayout = QHBoxLayout()  # 输入文件
            self.subtitleSplitVideoInputWidgetLayout.addWidget(self.subtitleSplitInputBox, 2)
            self.subtitleSplitVideoInputWidgetLayout.addWidget(self.subtitleSplitInputButton, 1)
            self.subtitleSplitVideoInputWidgetLayout.setContentsMargins(0, 0, 0, 0)
            self.subtitleSplitVideoInputWidget = QWidget()
            self.subtitleSplitVideoInputWidget.setLayout(self.subtitleSplitVideoInputWidgetLayout)
            self.subtitleSplitVideoInputWidget.setContentsMargins(0, 0, 0, 0)

            self.subtitleSplitVideoSubtitleFileWidgetLayout = QHBoxLayout()  # 输入字幕
            self.subtitleSplitVideoSubtitleFileWidgetLayout.addWidget(self.subtitleSplitSubtitleFileInputBox, 2)
            self.subtitleSplitVideoSubtitleFileWidgetLayout.addWidget(self.subtitleButton, 1)
            self.subtitleSplitVideoSubtitleFileWidgetLayout.setContentsMargins(0, 0, 0, 0)
            self.subtitleSplitVideoSubtitleFileWidget = QWidget()
            self.subtitleSplitVideoSubtitleFileWidget.setLayout(self.subtitleSplitVideoSubtitleFileWidgetLayout)
            self.subtitleSplitVideoSubtitleFileWidget.setContentsMargins(0, 0, 0, 0)

            self.subtitleSplitVideoStartEndTimeWidgetLayout = QHBoxLayout()  # 起始和终止时间
            self.subtitleSplitVideoStartEndTimeWidgetLayout.addWidget(self.subtitleSplitStartTimeHint, 1)
            self.subtitleSplitVideoStartEndTimeWidgetLayout.addWidget(self.subtitleSplitStartTimeBox, 1)
            self.subtitleSplitVideoStartEndTimeWidgetLayout.addSpacing(50)
            self.subtitleSplitVideoStartEndTimeWidgetLayout.addWidget(self.subtitleSplitEndTimeHint, 1)
            self.subtitleSplitVideoStartEndTimeWidgetLayout.addWidget(self.subtitleSplitEndTimeBox, 1)
            self.subtitleSplitVideoStartEndTimeWidgetLayout.setContentsMargins(0, 0, 0, 0)
            self.subtitleSplitVideoStartEndTimeWidget = QWidget()
            self.subtitleSplitVideoStartEndTimeWidget.setLayout(self.subtitleSplitVideoStartEndTimeWidgetLayout)
            self.subtitleSplitVideoStartEndTimeWidget.setContentsMargins(0, 0, 0, 0)

            self.subtitleSplitVideoCentenceOptionWidgetLayout = QHBoxLayout()  # 指定时间段
            self.subtitleSplitVideoCentenceOptionWidgetLayout.addWidget(self.exportClipSubtitleSwitch, 1)
            self.subtitleSplitVideoCentenceOptionWidgetLayout.addWidget(self.subtitleNumberPerClipHint, 1)
            self.subtitleSplitVideoCentenceOptionWidgetLayout.addWidget(self.subtitleNumberPerClipBox, 1)
            self.subtitleSplitVideoCentenceOptionWidgetLayout.setContentsMargins(0, 0, 0, 0)
            self.subtitleSplitVideoCentenceOptionWidget = QWidget()
            self.subtitleSplitVideoCentenceOptionWidget.setLayout(self.subtitleSplitVideoCentenceOptionWidgetLayout)
            self.subtitleSplitVideoCentenceOptionWidget.setContentsMargins(0, 0, 0, 0)

            self.subtitleSplitVdeoFormLayout = QFormLayout()
            self.subtitleSplitVdeoFormLayout.addRow(self.subtitleSplitInputHint, self.subtitleSplitVideoInputWidget) # 输入文件
            self.subtitleSplitVdeoFormLayout.addRow(self.subtitleHint, self.subtitleSplitVideoSubtitleFileWidget) # 输入字幕
            self.subtitleSplitVdeoFormLayout.addRow(self.outputHint, self.subtitleSplitOutputBox) # 输出文件
            self.subtitleSplitVdeoFormLayout.addRow(self.subtitleSplitSwitch, self.subtitleSplitVideoStartEndTimeWidget) # 起始和终止时间
            self.subtitleSplitVdeoFormLayout.addRow(self.subtitleOffsetHint, self.subtitleOffsetBox) # 起始和终止时间
            self.subtitleSplitVdeoFormLayout.setWidget(5, QFormLayout.SpanningRole, self.subtitleSplitVideoCentenceOptionWidget) # 多少句为一段


            self.subtitleSplitVdeoHboxLayout = QHBoxLayout()
            self.subtitleSplitVdeoHboxLayout.setContentsMargins(0, 0, 0, 0)
            self.subtitleSplitVdeoHboxLayout.addLayout(self.subtitleSplitVdeoFormLayout, 3)
            self.subtitleSplitVdeoHboxLayout.addWidget(self.subtitleSplitButton, 0)

            self.subtitleSplitVideoLayout.addLayout(self.subtitleSplitVdeoHboxLayout)  # 在主垂直布局添加选项的表单布局
            self.subtitleSplitVideoLayout.addStretch(1)



        self.masterLayout.addSpacing(5)

        # 根据时长分割片段
        if True:
            self.durationSplitVideoGroup = QGroupBox(self.tr('根据指定时长分割片段'))
            self.durationSplitVideoLayout = QVBoxLayout()
            self.durationSplitVideoGroup.setLayout(self.durationSplitVideoLayout)
            self.masterLayout.addWidget(self.durationSplitVideoGroup)

            self.durationSplitVideoInputHint = QLabel(self.tr('输入路径：'))
            self.durationSplitVideoInputBox = MyQLine()
            self.durationSplitVideoInputBox.textChanged.connect(self.setSubtitleSplitOutputFolder)
            self.durationSplitVideoInputButton = QPushButton(self.tr('选择文件'))

            self.durationSplitVideoOutputHint = QLabel(self.tr('输出文件夹：'))
            self.durationSplitVideoOutputBox = QLineEdit()
            self.durationSplitVideoOutputBox.setReadOnly(True)



            self.durationSplitVideoDurationPerClipHint = QLabel(self.tr('片段时长：'))
            self.durationSplitVideoDurationPerClipBox = QLineEdit()
            self.durationSplitVideoDurationPerClipBox.setAlignment(Qt.AlignCenter)

            self.durationSplitVideoCutHint = QCheckBox(self.tr('指定时间段'))
            self.durationSplitVideoInputSeekStartHint = QLabel(self.tr('起始时刻：'))
            self.durationSplitVideoInputSeekStartBox = QLineEdit()
            self.durationSplitVideoInputSeekStartBox.setAlignment(Qt.AlignCenter)
            self.durationSplitVideoEndTimeHint = QLabel(self.tr('截止时刻：'))
            self.durationSplitVideoEndTimeBox = QLineEdit()
            self.durationSplitVideoEndTimeBox.setAlignment(Qt.AlignCenter)
            self.durationSplitVideoCutHint.clicked.connect(self.onDurationSplitSwitchClicked)

            self.timeValidator = QRegExpValidator(self)
            self.timeValidator.setRegExp(QRegExp(r'[0-9]{0,2}:?[0-9]{0,2}:?[0-9]{0,2}\.?[0-9]{0,2}'))
            self.durationSplitVideoDurationPerClipBox.setValidator(self.timeValidator)
            self.durationSplitVideoInputSeekStartBox.setValidator(self.timeValidator)
            self.durationSplitVideoEndTimeBox.setValidator(self.timeValidator)

            self.durationSplitVideoRunButton = QPushButton(self.tr('运行'))
            self.durationSplitVideoRunButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

            self.durationSplitVideoInputSeekStartHint.hide()
            self.durationSplitVideoInputSeekStartBox.hide()
            self.durationSplitVideoEndTimeHint.hide()
            self.durationSplitVideoEndTimeBox.hide()

            self.durationSplitVideoInputBox.textChanged.connect(self.setdurationSplitOutputFolder)
            self.durationSplitVideoInputButton.clicked.connect(self.durationSplitInputButtonClicked)
            self.durationSplitVideoRunButton.clicked.connect(self.onDurationSplitRunButtonClicked)


            self.durationSplitVideoInputWidgetLayout = QHBoxLayout()  # 输入文件
            self.durationSplitVideoInputWidgetLayout.addWidget(self.durationSplitVideoInputBox, 2)
            self.durationSplitVideoInputWidgetLayout.addWidget(self.durationSplitVideoInputButton, 1)
            self.durationSplitVideoInputWidgetLayout.setContentsMargins(0, 0, 0, 0)
            self.durationSplitVideoInputWidget = QWidget()
            self.durationSplitVideoInputWidget.setLayout(self.durationSplitVideoInputWidgetLayout)
            self.durationSplitVideoInputWidget.setContentsMargins(0, 0, 0, 0)

            self.durationSplitVideoStartEndTimeWidgetLayout = QHBoxLayout()  # 指定时间段
            self.durationSplitVideoStartEndTimeWidgetLayout.addWidget(self.durationSplitVideoInputSeekStartHint, 1)
            self.durationSplitVideoStartEndTimeWidgetLayout.addWidget(self.durationSplitVideoInputSeekStartBox, 1)
            self.durationSplitVideoStartEndTimeWidgetLayout.addSpacing(50)
            self.durationSplitVideoStartEndTimeWidgetLayout.addWidget(self.durationSplitVideoEndTimeHint, 1)
            self.durationSplitVideoStartEndTimeWidgetLayout.addWidget(self.durationSplitVideoEndTimeBox, 1)
            self.durationSplitVideoStartEndTimeWidgetLayout.setContentsMargins(0, 0, 0, 0)
            self.durationSplitVideoStartEndTimeWidget = QWidget()
            self.durationSplitVideoStartEndTimeWidget.setLayout(self.durationSplitVideoStartEndTimeWidgetLayout)
            self.durationSplitVideoStartEndTimeWidget.setContentsMargins(0, 0, 0, 0)

            self.durationSplitVdeoFormLayout = QFormLayout()
            self.durationSplitVdeoFormLayout.addRow(self.durationSplitVideoInputHint, self.durationSplitVideoInputWidget)
            self.durationSplitVdeoFormLayout.addRow(self.durationSplitVideoOutputHint, self.durationSplitVideoOutputBox)
            self.durationSplitVdeoFormLayout.addRow(self.durationSplitVideoDurationPerClipHint, self.durationSplitVideoDurationPerClipBox)
            self.durationSplitVdeoFormLayout.addRow(self.durationSplitVideoCutHint, self.durationSplitVideoStartEndTimeWidget)

            self.durationSplitVdeoHboxLayout = QHBoxLayout()
            self.durationSplitVdeoHboxLayout.setContentsMargins(0, 0, 0, 0)
            self.durationSplitVdeoHboxLayout.addLayout(self.durationSplitVdeoFormLayout, 3)
            self.durationSplitVdeoHboxLayout.addWidget(self.durationSplitVideoRunButton, 0)

            self.durationSplitVideoLayout.addLayout(self.durationSplitVdeoHboxLayout)  # 在主垂直布局添加选项的表单布局
            self.durationSplitVideoLayout.addStretch(1)

        self.masterLayout.addSpacing(5)

        # 根据大小分割片段
        if True:
            self.sizeSplitVideoGroup = QGroupBox(self.tr('根据指定大小分割片段'))
            self.sizeSplitVideoLayout = QVBoxLayout()
            self.sizeSplitVideoGroup.setLayout(self.sizeSplitVideoLayout)
            self.masterLayout.addWidget(self.sizeSplitVideoGroup)

            self.sizeSplitVideoInputHint = QLabel(self.tr('输入路径：'))
            self.sizeSplitVideoInputBox = MyQLine()
            self.sizeSplitVideoInputButton = QPushButton(self.tr('选择文件'))

            self.sizeSplitVideoOutputHint = QLabel(self.tr('输出文件夹：'))
            self.sizeSplitVideoOutputBox = MyQLine()
            self.sizeSplitVideoOutputBox.setReadOnly(True)

            self.sizeSplitVideoOutputSizeHint = QLabel(self.tr('片段大小(MB)：'))
            self.sizeSplitVideoOutputSizeBox = QLineEdit()
            self.sizeSplitVideoOutputSizeBox.setAlignment(Qt.AlignCenter)

            self.sizeValidator = QRegExpValidator(self)
            self.sizeValidator.setRegExp(QRegExp(r'\d+\.?\d*'))
            self.sizeSplitVideoOutputSizeBox.setValidator(self.sizeValidator)

            self.sizeSplitVideoCutHint = QCheckBox(self.tr('指定时间段'))
            self.sizeSplitVideoCutHint.clicked.connect(self.onSizeSplitSwitchClicked)
            self.sizeSplitVideoInputSeekStartHint = QLabel(self.tr('起始时刻：'))
            self.sizeSplitVideoInputSeekStartBox = QLineEdit()
            self.sizeSplitVideoInputSeekStartBox.setAlignment(Qt.AlignCenter)
            self.sizeSplitVideoEndTimeHint = QLabel(self.tr('截止时刻：'))
            self.sizeSplitVideoEndTimeBox = QLineEdit()
            self.sizeSplitVideoEndTimeBox.setAlignment(Qt.AlignCenter)

            self.timeValidator = QRegExpValidator(self)
            self.timeValidator.setRegExp(QRegExp(r'[0-9]{0,2}:?[0-9]{0,2}:?[0-9]{0,2}\.?[0-9]{0,2}'))
            self.sizeSplitVideoInputSeekStartBox.setValidator(self.timeValidator)
            self.sizeSplitVideoEndTimeBox.setValidator(self.timeValidator)

            self.sizeSplitVideoRunButton = QPushButton(self.tr('运行'))
            self.sizeSplitVideoRunButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

            self.sizeSplitVideoInputSeekStartHint.hide()
            self.sizeSplitVideoInputSeekStartBox.hide()
            self.sizeSplitVideoEndTimeHint.hide()
            self.sizeSplitVideoEndTimeBox.hide()

            self.sizeSplitVideoInputBox.textChanged.connect(self.setSizeSplitOutputFolder)
            self.sizeSplitVideoInputButton.clicked.connect(self.sizeSplitInputButtonClicked)
            self.sizeSplitVideoRunButton.clicked.connect(self.onSizeSplitRunButtonClicked)


            self.sizeSplitVideoInputWidgetLayout = QHBoxLayout()  # 输入文件
            self.sizeSplitVideoInputWidgetLayout.addWidget(self.sizeSplitVideoInputBox, 2)
            self.sizeSplitVideoInputWidgetLayout.addWidget(self.sizeSplitVideoInputButton, 1)
            self.sizeSplitVideoInputWidgetLayout.setContentsMargins(0, 0, 0, 0)
            self.sizeSplitVideoInputWidget = QWidget()
            self.sizeSplitVideoInputWidget.setLayout(self.sizeSplitVideoInputWidgetLayout)
            self.sizeSplitVideoInputWidget.setContentsMargins(0, 0, 0, 0)

            self.sizeSplitVideoStartEndTimeWidgetLayout = QHBoxLayout()  # 指定时间段
            self.sizeSplitVideoStartEndTimeWidgetLayout.addWidget(self.sizeSplitVideoInputSeekStartHint, 1)
            self.sizeSplitVideoStartEndTimeWidgetLayout.addWidget(self.sizeSplitVideoInputSeekStartBox, 1)
            self.sizeSplitVideoStartEndTimeWidgetLayout.addSpacing(50)
            self.sizeSplitVideoStartEndTimeWidgetLayout.addWidget(self.sizeSplitVideoEndTimeHint, 1)
            self.sizeSplitVideoStartEndTimeWidgetLayout.addWidget(self.sizeSplitVideoEndTimeBox, 1)
            self.sizeSplitVideoStartEndTimeWidgetLayout.setContentsMargins(0, 0, 0, 0)
            self.sizeSplitVideoStartEndTimeWidget = QWidget()
            self.sizeSplitVideoStartEndTimeWidget.setLayout(self.sizeSplitVideoStartEndTimeWidgetLayout)
            self.sizeSplitVideoStartEndTimeWidget.setContentsMargins(0, 0, 0, 0)

            self.sizeSplitVdeoFormLayout = QFormLayout()
            self.sizeSplitVdeoFormLayout.addRow(self.sizeSplitVideoInputHint, self.sizeSplitVideoInputWidget)
            self.sizeSplitVdeoFormLayout.addRow(self.sizeSplitVideoOutputHint, self.sizeSplitVideoOutputBox)
            self.sizeSplitVdeoFormLayout.addRow(self.sizeSplitVideoOutputSizeHint, self.sizeSplitVideoOutputSizeBox)
            self.sizeSplitVdeoFormLayout.addRow(self.sizeSplitVideoCutHint, self.sizeSplitVideoStartEndTimeWidget)

            self.sizeSplitVdeoHboxLayout = QHBoxLayout()
            self.sizeSplitVdeoHboxLayout.setContentsMargins(0, 0, 0, 0)
            self.sizeSplitVdeoHboxLayout.addLayout(self.sizeSplitVdeoFormLayout, 3)
            self.sizeSplitVdeoHboxLayout.addWidget(self.sizeSplitVideoRunButton, 0)

            self.sizeSplitVideoLayout.addLayout(self.sizeSplitVdeoHboxLayout)  # 在主垂直布局添加选项的表单布局
            self.sizeSplitVideoLayout.addStretch(1)


    def onSubtitleSplitSwitchClicked(self):
        if self.subtitleSplitSwitch.isChecked():
            self.subtitleSplitStartTimeHint.show()
            self.subtitleSplitStartTimeBox.show()
            self.subtitleSplitEndTimeHint.show()
            self.subtitleSplitEndTimeBox.show()
        else:
            self.subtitleSplitStartTimeHint.hide()
            self.subtitleSplitStartTimeBox.hide()
            self.subtitleSplitEndTimeHint.hide()
            self.subtitleSplitEndTimeBox.hide()

    def onDurationSplitSwitchClicked(self):
        if self.durationSplitVideoCutHint.isChecked():
            self.durationSplitVideoInputSeekStartHint.show()
            self.durationSplitVideoInputSeekStartBox.show()
            self.durationSplitVideoEndTimeHint.show()
            self.durationSplitVideoEndTimeBox.show()
        else:
            self.durationSplitVideoInputSeekStartHint.hide()
            self.durationSplitVideoInputSeekStartBox.hide()
            self.durationSplitVideoEndTimeHint.hide()
            self.durationSplitVideoEndTimeBox.hide()

    def onSizeSplitSwitchClicked(self):
        if self.sizeSplitVideoCutHint.isChecked():
            self.sizeSplitVideoInputSeekStartHint.show()
            self.sizeSplitVideoInputSeekStartBox.show()
            self.sizeSplitVideoEndTimeHint.show()
            self.sizeSplitVideoEndTimeBox.show()
        else:
            self.sizeSplitVideoInputSeekStartHint.hide()
            self.sizeSplitVideoInputSeekStartBox.hide()
            self.sizeSplitVideoEndTimeHint.hide()
            self.sizeSplitVideoEndTimeBox.hide()

    def setSubtitleSplitOutputFolder(self):
        inputPath = self.subtitleSplitInputBox.text()
        if inputPath != '':
            outputFolder = os.path.splitext(inputPath)[0] + '/'
            self.subtitleSplitOutputBox.setText(outputFolder)
        else:
            self.subtitleSplitOutputBox.setText('')

    def setdurationSplitOutputFolder(self):
        inputPath = self.durationSplitVideoInputBox.text()
        if inputPath != '':
            outputFolder = os.path.splitext(inputPath)[0] + '/'
            self.durationSplitVideoOutputBox.setText(outputFolder)
        else:
            self.durationSplitVideoOutputBox.setText('')

    def setSizeSplitOutputFolder(self):
        inputPath = self.sizeSplitVideoInputBox.text()
        if inputPath != '':
            outputFolder = os.path.splitext(inputPath)[0] + '/'
            self.sizeSplitVideoOutputBox.setText(outputFolder)
        else:
            self.sizeSplitVideoOutputBox.setText('')

    def subtitleSplitInputButtonClicked(self):
        filename = QFileDialog().getOpenFileName(self, self.tr('打开文件'), None, self.tr('所有文件(*)'))
        if filename[0] != '':
            self.subtitleSplitInputBox.setText(filename[0])
        return True

    def subtitleSplitSubtitleFileInputButtonClicked(self):
        filename = QFileDialog().getOpenFileName(self, self.tr('打开文件'), None, self.tr('所有文件(*)'))
        if filename[0] != '':
            self.subtitleSplitSubtitleFileInputBox.setText(filename[0])
        return True

    def durationSplitInputButtonClicked(self):
        filename = QFileDialog().getOpenFileName(self, self.tr('打开文件'), None, self.tr('所有文件(*)'))
        if filename[0] != '':
            self.durationSplitVideoInputBox.setText(filename[0])
        return True

    def sizeSplitInputButtonClicked(self):
        filename = QFileDialog().getOpenFileName(self, self.tr('打开文件'), None, self.tr('所有文件(*)'))
        if filename[0] != '':
            self.sizeSplitVideoInputBox.setText(filename[0])
        return True

    def onSubtitleSplitRunButtonClicked(self):
        inputFile = self.subtitleSplitInputBox.text()
        subtitleFile = self.subtitleSplitSubtitleFileInputBox.text()
        outputFolder = self.subtitleSplitOutputBox.text()

        cutSwitchValue = self.subtitleSplitSwitch.isChecked()
        cutStartTime = self.subtitleSplitStartTimeBox.text()
        cutEndTime = self.subtitleSplitEndTimeBox.text()

        subtitleOffset = self.subtitleOffsetBox.value()

        if inputFile != '' and subtitleFile != '':
            window = Console(mainWindow)

            output = window.consoleBox
            outputForFFmpeg = window.consoleBoxForFFmpeg

            thread = SubtitleSplitVideoThread(mainWindow)

            thread.ffmpegOutputOption = self.ffmpegOutputOptionBox.currentText()

            thread.inputFile = inputFile
            thread.subtitleFile = subtitleFile
            thread.outputFolder = outputFolder

            thread.cutSwitchValue = cutSwitchValue
            thread.cutStartTime = cutStartTime
            thread.cutEndTime = cutEndTime
            thread.subtitleOffset = subtitleOffset

            thread.exportClipSubtitle = self.exportClipSubtitleSwitch.isChecked()
            thread.subtitleNumberPerClip = self.subtitleNumberPerClipBox.value()

            thread.output = output

            thread.signal.connect(output.print)
            thread.signalForFFmpeg.connect(outputForFFmpeg.print)

            window.thread = thread  # 把这里的剪辑子进程赋值给新窗口，这样新窗口就可以在关闭的时候也把进程退出

            thread.start()
            print(123)

    def onDurationSplitRunButtonClicked(self):
        inputFile = self.durationSplitVideoInputBox.text()
        outputFolder = self.durationSplitVideoOutputBox.text()

        durationPerClip = self.durationSplitVideoDurationPerClipBox.text()

        cutSwitchValue = self.durationSplitVideoCutHint.isChecked()
        cutStartTime = self.durationSplitVideoInputSeekStartBox.text()
        cutEndTime = self.durationSplitVideoEndTimeBox.text()

        if inputFile != '' and durationPerClip != '':
            window = Console(mainWindow)

            output = window.consoleBox
            outputForFFmpeg = window.consoleBoxForFFmpeg

            thread = DurationSplitVideoThread(mainWindow)

            thread.ffmpegOutputOption = self.ffmpegOutputOptionBox.currentText()


            thread.inputFile = inputFile
            thread.outputFolder = outputFolder

            thread.durationPerClip = durationPerClip

            thread.cutSwitchValue = cutSwitchValue
            thread.cutStartTime = cutStartTime
            thread.cutEndTime = cutEndTime

            thread.output = output
            thread.outputForFFmpeg = outputForFFmpeg

            thread.signal.connect(output.print)
            thread.signalForFFmpeg.connect(outputForFFmpeg.print)

            window.thread = thread  # 把这里的剪辑子进程赋值给新窗口，这样新窗口就可以在关闭的时候也把进程退出

            thread.start()

    def onSizeSplitRunButtonClicked(self):
        inputFile = self.sizeSplitVideoInputBox.text()
        outputFolder = self.sizeSplitVideoOutputBox.text()

        sizePerClip = self.sizeSplitVideoOutputSizeBox.text()

        cutSwitchValue = self.sizeSplitVideoCutHint.isChecked()
        cutStartTime = self.sizeSplitVideoInputSeekStartBox.text()
        cutEndTime = self.sizeSplitVideoEndTimeBox.text()

        if inputFile != '' and sizePerClip != '':
            window = Console(mainWindow)

            output = window.consoleBox
            outputForFFmpeg = window.consoleBoxForFFmpeg

            thread = SizeSplitVideoThread(mainWindow)

            thread.ffmpegOutputOption = self.ffmpegOutputOptionBox.currentText()


            thread.inputFile = inputFile
            thread.outputFolder = outputFolder

            thread.sizePerClip = sizePerClip

            thread.cutSwitchValue = cutSwitchValue
            thread.cutStartTime = cutStartTime
            thread.cutEndTime = cutEndTime

            thread.output = output

            thread.signal.connect(output.print)
            thread.signalForFFmpeg.connect(outputForFFmpeg.print)

            window.thread = thread  # 把这里的剪辑子进程赋值给新窗口，这样新窗口就可以在关闭的时候也把进程退出

            thread.start()