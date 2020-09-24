# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import os

# try:
from moduels.component.MyQLine import MyQLine
from moduels.component.MyQLine import MyQLine
from moduels.component.NormalValue import 常量
# except:
#     from QuickCut.


class FFmpegMainTab(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = 常量.conn
        self.ossTableName = 常量.ossTableName
        self.apiTableName = 常量.apiTableName
        self.preferenceTableName = 常量.preferenceTableName
        self.presetTableName = 常量.presetTableName
        self.cursor = self.conn.cursor()
        self.initGui()
        self.initValue()


    def initGui(self):
        self.输入输出vbox = QVBoxLayout()
        # 构造输入一、输入二和输出选项
        if True:
            # 输入1
            if True:
                self.输入1标签 = QLabel(self.tr('输入1路径：'))
                self.输入1路径框 = MyQLine()
                self.输入1路径框.setPlaceholderText(self.tr('这里输入要处理的视频、音频文件'))
                self.输入1路径框.signal.connect(self.lineEditHasDrop)
                self.输入1路径框.setToolTip(self.tr('这里输入要处理的视频、音频文件'))
                self.输入1路径框.textChanged.connect(self.generateFinalCommand)
                self.输入1选择文件按钮 = QPushButton(self.tr('选择文件'))
                self.输入1选择文件按钮.clicked.connect(self.chooseFile1ButtonClicked)
                self.输入1路径hbox = QHBoxLayout()
                self.输入1路径hbox.addWidget(self.输入1标签, 0)
                self.输入1路径hbox.addWidget(self.输入1路径框, 1)
                self.输入1路径hbox.addWidget(self.输入1选择文件按钮, 0)

                self.输入1截取时间hbox = QHBoxLayout()
                self.输入1截取时间勾选框 = QCheckBox(self.tr('截取片段'))
                self.输入1截取时间勾选框.clicked.connect(self.inputOneCutCheckboxClicked)
                self.输入1截取时间勾选框.clicked.connect(self.generateFinalCommand)
                self.输入1截取时间start标签 = QLabel(self.tr('起始时间：'))
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
                self.输入1选项标签 = QLabel(self.tr('输入1选项：'))
                self.输入1选项输入框 = MyQLine()
                self.输入1选项输入框.textChanged.connect(self.generateFinalCommand)
                self.输入1选项hbox.addWidget(self.输入1选项标签)
                self.输入1选项hbox.addWidget(self.输入1选项输入框)

                self.输入1vbox = QVBoxLayout()
                self.输入1vbox.addLayout(self.输入1路径hbox)
                self.输入1vbox.addLayout(self.输入1选项hbox)
                self.输入1vbox.addLayout(self.输入1截取时间hbox)

            # 输入2
            if True:
                self.输入2标签 = QLabel(self.tr('输入2路径：'))
                self.输入2路径框 = MyQLine()
                self.输入2路径框.setPlaceholderText(self.tr('输入2是选填的，只有涉及同时处理两个文件的操作才需要输入2'))
                self.输入2路径框.setToolTip(self.tr('输入2是选填的，只有涉及同时处理两个文件的操作才需要输入2'))
                self.输入2路径框.textChanged.connect(self.generateFinalCommand)
                self.输入2选择文件按钮 = QPushButton(self.tr('选择文件'))
                self.输入2选择文件按钮.clicked.connect(self.chooseFile2ButtonClicked)
                self.输入2路径hbox = QHBoxLayout()
                self.输入2路径hbox.addWidget(self.输入2标签, 0)
                self.输入2路径hbox.addWidget(self.输入2路径框, 1)
                self.输入2路径hbox.addWidget(self.输入2选择文件按钮, 0)

                self.输入2截取时间hbox = QHBoxLayout()
                self.输入2截取时间勾选框 = QCheckBox(self.tr('截取片段'))
                self.输入2截取时间勾选框.clicked.connect(self.inputTwoCutCheckboxClicked)
                self.输入2截取时间勾选框.clicked.connect(self.generateFinalCommand)
                self.输入2截取时间start标签 = QLabel(self.tr('起始时间：'))
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
                self.输入2选项标签 = QLabel(self.tr('输入2选项：'))
                self.输入2选项输入框 = MyQLine()
                self.输入2选项输入框.textChanged.connect(self.generateFinalCommand)
                self.输入2选项hbox.addWidget(self.输入2选项标签)
                self.输入2选项hbox.addWidget(self.输入2选项输入框)

                self.输入2vbox = QVBoxLayout()
                self.输入2vbox.addLayout(self.输入2路径hbox)
                self.输入2vbox.addLayout(self.输入2选项hbox)
                self.输入2vbox.addLayout(self.输入2截取时间hbox)

            self.timeValidator = QRegExpValidator(self)
            self.timeValidator.setRegExp(QRegExp(r'[0-9]{0,2}:?[0-9]{0,2}:?[0-9]{0,2}\.?[0-9]{0,2}'))
            self.输入1截取时间start输入框.setValidator(self.timeValidator)
            self.输入1截取时间end输入框.setValidator(self.timeValidator)
            self.输入2截取时间start输入框.setValidator(self.timeValidator)
            self.输入2截取时间end输入框.setValidator(self.timeValidator)

            # 输出
            if True:
                self.输出标签 = QLabel(self.tr('输出：'))
                self.输出路径框 = MyQLine()
                self.输出路径框.setPlaceholderText(self.tr('文件名填什么后缀，就会输出什么格式'))
                self.输出路径框.setToolTip(self.tr('这里填写输出文件保存路径'))
                self.输出路径框.textChanged.connect(self.generateFinalCommand)
                self.输出选择文件按钮 = QPushButton(self.tr('选择保存位置'))
                self.输出选择文件按钮.clicked.connect(self.chooseOutputFileButtonClicked)
                self.输出路径hbox = QHBoxLayout()
                self.输出路径hbox.addWidget(self.输出标签, 0)
                self.输出路径hbox.addWidget(self.输出路径框, 1)
                self.输出路径hbox.addWidget(self.输出选择文件按钮, 0)

                self.输出分辨率hbox = QHBoxLayout()
                self.输出分辨率勾选框 = QCheckBox(self.tr('新分辨率'))
                self.输出分辨率勾选框.clicked.connect(self.outputResolutionCheckboxClicked)
                self.输出分辨率勾选框.clicked.connect(self.generateFinalCommand)

                self.X轴分辨率输入框 = self.ResolutionEdit()
                self.X轴分辨率输入框.setAlignment(Qt.AlignCenter)
                self.X轴分辨率输入框.textChanged.connect(self.generateFinalCommand)
                self.分辨率乘号标签 = self.ClickableResolutionTimesLable()
                self.Y轴分辨率输入框 = self.ResolutionEdit()
                self.Y轴分辨率输入框.setAlignment(Qt.AlignCenter)
                self.Y轴分辨率输入框.textChanged.connect(self.generateFinalCommand)
                self.分辨率预设按钮 = QPushButton(self.tr('分辨率预设'))
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

                self.输出选项标签 = QLabel(self.tr('输出选项：'))
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
                self.主布局.addSpacing(30)
                self.主布局.addLayout(self.输入2vbox)
                self.主布局.addSpacing(30)
                self.主布局.addLayout(self.输出vbox)

            # 输入输出布局放到一个控件
            self.主布局控件 = QWidget()
            self.主布局控件.setLayout(self.主布局)

        # 预设列表
        if True:
            self.预设列表提示标签 = QLabel(self.tr('选择预设：'))
            self.预设列表 = QListWidget()
            self.预设列表.itemClicked.connect(self.presetItemSelected)
            self.预设列表.itemDoubleClicked.connect(self.addPresetButtonClicked)

            self.添加预设按钮 = QPushButton('+')
            self.删除预设按钮 = QPushButton('-')
            # self.修改预设按钮 = QPushButton('修改选中预设')
            self.上移预设按钮 = QPushButton('↑')
            self.下移预设按钮 = QPushButton('↓')
            self.查看预设帮助按钮 = QPushButton(self.tr('查看该预设帮助'))
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
            self.总命令编辑框.setPlaceholderText(self.tr('这里是自动生成的总命令'))

            self.总命令编辑框.setMaximumHeight(200)
            self.总命令执行按钮 = QPushButton(self.tr('运行'))
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

    def initValue(self):
        # 检查杂项文件夹是否存在
        self.createMiscFolder()

        # 检查数据库是否存在
        self.createDB()

        # 刷新预设列表
        self.refreshList()

        # 定义一个变量，用于判断输入文件，输出文件的选项是否有被手工修改过
        self.commandOptionsChanged = False

    # 如果输入文件是拖进去的
    def lineEditHasDrop(self, path):
        outputName = os.path.splitext(path)[0] + '_out' + os.path.splitext(path)[1]
        self.输出路径框.setText(outputName)
        return True

    # 选择输入文件1
    def chooseFile1ButtonClicked(self):
        filename = QFileDialog().getOpenFileName(self, '打开文件', None, '所有文件(*)')
        if filename[0] != '':
            self.输入1路径框.setText(filename[0])
            outputName = re.sub(r'(\.[^\.]+)$', r'_out\1', filename[0])
            self.输出路径框.setText(outputName)
        self.commandOptionsChanged = False
        return True

    # 选择输入文件2
    def chooseFile2ButtonClicked(self):
        filename = QFileDialog().getOpenFileName(self, '打开文件', None, '所有文件(*)')
        if filename[0] != '':
            self.输入2路径框.setText(filename[0])
        self.commandOptionsChanged = False
        return True

    # 选择输出文件
    def chooseOutputFileButtonClicked(self):
        filename = QFileDialog().getSaveFileName(self, '设置输出保存的文件名', '输出视频.mp4', '所有文件(*)')
        self.输出路径框.setText(filename[0])
        self.commandOptionsChanged = False
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
            self.commandOptionsChanged = True
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
                    # print(False)
                    self.finalCommand = self.finalCommand + ' ' + '-vf "scale=%s:%s"' % (outputResizeX, outputResizeY)
                elif 'scale' in outputOption:
                    # print(True)
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
        outputPath = self.输出路径框.text()
        if os.path.exists(outputPath):
            overwrite = QMessageBox.information(
                self, self.tr('覆盖确认'), self.tr('输出路径对应的文件已存在，是否要覆盖？'),
                QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
            if overwrite != QMessageBox.Yes:
                return
        if finalCommand != '':
            execute(finalCommand)

    # 检查杂项文件夹是否存在
    def createMiscFolder(self):
        if not os.path.exists('./misc'):
            os.mkdir('./misc')

    # 检查数据库是否存在
    def createDB(self):
        ########改用主数据库
        cursor = self.conn.cursor()
        result = cursor.execute('select * from sqlite_master where name = "%s";' % (self.presetTableName))
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
            # print('新建了表单')

            # 新建一个空预设
            # 不使用预设
            presetName = self.tr('不使用预设')
            cursor.execute('''
                            insert into %s 
                            (name, outputOption) 
                            values (
                            '%s',
                            '-c copy'
                            );'''
                           % (presetTableName, presetName))

            # h264 压制
            presetName = self.tr('H264压制')
            description = '''<body><h4>H264压制视频</h4><p>输入文件一，模板中选择 Video ( h264 ) ，输出选项会自动设置好，点击 Run ，粘贴编码，等待压制完成即可。</p><p> </p><h4>选项帮助：</h4><h5>输出文件选项：</h5><p>-c:v 设置视频编码器</p><p>-crf 恒定视频质量的参数</p><p>-preset 压制速度，可选项：ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo</p><p>-qcomp 量化曲线压缩因子（Quantizer curve compression factor）</p><p>-psy-rd 用 psy-rd:psy-trellis 的格式设置 心理视觉优化强度（ strength of psychovisual optimization, in psy-rd:psy-trellis format）</p><p>-aq-mode 设置 AQ 方法，可选值为：</p><ul><li>none (<em>0</em>) 帧内宏块全部使用同一或者固定的表</li><li>variance (<em>1</em>) 使用方差动态计算每个宏块的</li><li>autovariance (<em>2</em>) 方差自适应模式，会先遍历一次全部宏块，统计出一些中间参数，之后利用这些参数，对每个宏块计算 </li></ul><p>-aq-strength 设置 AQ 强度，在平面和纹理区域 减少 方块和模糊。</p><p> </p><p> </p><h4>注意事项</h4><p>注意，压制视频的话，输入文件放一个就行了哈，别放两个输入，FFmpeg 会自动把最高分辨率的视频流和声道数最多的音频流合并输出的。</p><p> </p><h4>相关科普</h4><p>压制过程中你可以从命令行看到实时压制速度、总码率、体积、压制到视频几分几秒了。</p><p>相关解释：H264是一个很成熟的视频编码格式，兼容性也很好，一般你所见到的视频多数都是这个编码，小白压制视频无脑选这个就行了。</p><p>这个参数下，画质和体积能得到较好的平衡，一般能把手机相机拍摄的视频压制到原来体积的1/3左右，甚至更小，画质也没有明显的损失。</p><p>控制视频大小有两种方法：</p><ul><li><p>恒定画面质量，可变码率。也就是 crf 方式</p></li><p>这时，编码器会根据你要求的画面质量，自动分配码率，给复杂的画面部分多分配点码率，给简单的画面少分配点码率，可以得到画面质量均一的输出视频，这是最推荐的压制方式。不过无法准确预测输出文件的大小。假如你的视频全程都是非常复杂、包含大量背景运动的画面，那么可能压制出来的视频，比原视频还要大。这里的压制方式用的就是 恒定画面质量 的方式。</p><li><p>恒定码率</p></li></ul><p>这时，编码器会根据你的要求，给每一秒都分配相同的码率，可以准确预测输出文件的大小。但是，由于码率恒定，可能有些复杂的片段，你分配的码率不够用，就会画质下降，有些静态部分多的画面，就浪费了很多码率，所以一般不推荐用。如果你想用这个方案，请参阅 <a href='#控制码率压制视频'>控制码率压制视频</a> </p><p>针对恒定码率的缺点，有个改进方案就是 2-pass （二压），详见 <a href='#h264 二压视频（两次操作）'>h264 二压视频（两次操作）</a> </p><p>此处输出选项里的 -crf 23 是画质控制参数。取值 0 - 51 ，越小画质越高，同时体积越大。 0 代表无损画质，体积超大。一般认为， -crf 18 的时候，人眼就几乎无法看出画质有损失了，大于 -crf 28 的时候，人眼就开始看到比较明显的画质损失。没有特殊要求的话，默认用 -crf 23 就行了。压制画质要求很高的视频就用 -crf 18 。</p><p>此处输出选项里的 -preset medium 代表压制编码速度适中，可选值有 ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo ，设置越慢，压制时间越长，画质控制越出色，设置越快，信息丢失就越严重，图像质量越差。</p><p>为什么 placebo 是纯粹的浪费时间？ </p><p>相同码率下，相比于 veryslow，placebo 只提升不到 1% 的视频质量（同样码率下），但消耗非常多的时间。veryslow 比 slower 提升 3% ； slower 比 slow 提升 5% ，slow 比 medium 提升 5%-10% 。</p><p>相同码率下，相较于 medium：slow 编码所需时间增加大约 40% ；到 slower 增加大约 100% ，到 veryslow 增加大约 280% 。</p><p>相同码率下，相较于 medium ： fast 节约 10% 编码时间； faster 节约 25% ； ultrafast 节约 55%（但代价是更低的画质）</p><p>如果你的原视频是 rgb 像素格式的，建议使用 -c:v libx264rgb ，来避免转化成 yuv420 时的画质损失。</p></body>'''
            cursor.execute('''
                            insert into %s 
                            (name, outputOption, description) 
                            values (
                            '%s', 
                            '-c:v libx264 -crf 23 -preset slow -qcomp 0.5 -psy-rd 0.3:0 -aq-mode 2 -aq-strength 0.8 -b:a 256k',
                            '%s'
                            );'''
                           % (presetTableName, presetName, description.replace("'", "''")))

            # h264 压制 Intel 硬件加速
            presetName = self.tr('H264压制 Intel 硬件加速')
            description = '''<body><p>关于使用硬件加速：</p><p>目前硬件加速支持两种编码格式：H264 和 H265</p><p>有3种加速方法，分别对应三家的硬件：Inter、AMD、Nvidia</p><p>不过在苹果电脑上，不管你用的哪家的硬件，都是使用 videotoolbox 编码器。</p><p>需要注意的是，即便你的电脑拥有 Nvidia 显卡，可能也用不了 Nvidia 的硬件加速编码，因为 Nvidia 硬件加速依赖于显卡内部的一种特定的 GPU 的物理部分，专用于编码。只有在 GTX10 和 RTX20 以上的显卡才搭载有这个物理部分。</p><p>使用硬件编码器进行编码，只需要将输出选项中的编码器改成硬件编码器即可，其中：</p><ul><li><code>-c:v h264_qsv</code> 对应 Intel H264 编码</li><li><code>-c:v h264_amf</code> 对应 AMD H264 编码</li><li><code>-c:v h264_nvenc</code> 对应 Nvidia H264 编码</li><li><code>-c:v h264_videotoolbox</code> 对应苹果电脑的 H264 编码</li><li><code>-c:v hevc_qsv</code> 对应 Intel H265 编码</li><li><code>-c:v hevc_amf</code> 对应 AMDH265 编码</li><li><code>-c:v hevc_nvenc</code> 对应 Nvidia H265 编码</li><li><code>-c:v hevc_videotoolbox</code> 对应苹果电脑的 H265 编码</li></ul><p><code>-c:v</code> 表示视频（Video）的编码器（codec）</p><p>在使用硬件加速编码器的时候，控制输出视频的质量是使用 <code>qscale</code> 参数，他的数值可以从 <code>0.1 - 255</code> 不等，数值越小，画质越高，码率越大，输出文件体积越大。同一个数值对于不同的编码器画质的影响效果不同。所以你需要自己测试，在玛律大小和视频画质之间找到一个平衡的 <code>qscale</code> 数值。</p><p>目前所有的硬件加速选项都是类似这样的：<code>-c:v h264_qsv -qscale 15</code> ，这表示使用英特尔 h264 硬件加速编码器，视频质量参数为15。你可以更改里面的数值，以达到你期望的画质效果。</p></body>'''
            cursor.execute('''
                            insert into %s 
                            (name, outputOption, description) 
                            values (
                            '%s', 
                            '-c:v h264_qsv -qscale 15 -b:a 256k',
                            '%s'
                            );'''
                           % (presetTableName, presetName, description.replace("'", "''")))

            # h264 压制 AMD 硬件加速
            presetName = self.tr('H264压制 AMD 硬件加速')
            description = '''<body><p>关于使用硬件加速：</p><p>目前硬件加速支持两种编码格式：H264 和 H265</p><p>有3种加速方法，分别对应三家的硬件：Inter、AMD、Nvidia</p><p>不过在苹果电脑上，不管你用的哪家的硬件，都是使用 videotoolbox 编码器。</p><p>需要注意的是，即便你的电脑拥有 Nvidia 显卡，可能也用不了 Nvidia 的硬件加速编码，因为 Nvidia 硬件加速依赖于显卡内部的一种特定的 GPU 的物理部分，专用于编码。只有在 GTX10 和 RTX20 以上的显卡才搭载有这个物理部分。</p><p>使用硬件编码器进行编码，只需要将输出选项中的编码器改成硬件编码器即可，其中：</p><ul><li><code>-c:v h264_qsv</code> 对应 Intel H264 编码</li><li><code>-c:v h264_amf</code> 对应 AMD H264 编码</li><li><code>-c:v h264_nvenc</code> 对应 Nvidia H264 编码</li><li><code>-c:v h264_videotoolbox</code> 对应苹果电脑的 H264 编码</li><li><code>-c:v hevc_qsv</code> 对应 Intel H265 编码</li><li><code>-c:v hevc_amf</code> 对应 AMDH265 编码</li><li><code>-c:v hevc_nvenc</code> 对应 Nvidia H265 编码</li><li><code>-c:v hevc_videotoolbox</code> 对应苹果电脑的 H265 编码</li></ul><p><code>-c:v</code> 表示视频（Video）的编码器（codec）</p><p>在使用硬件加速编码器的时候，控制输出视频的质量是使用 <code>qscale</code> 参数，他的数值可以从 <code>0.1 - 255</code> 不等，数值越小，画质越高，码率越大，输出文件体积越大。同一个数值对于不同的编码器画质的影响效果不同。所以你需要自己测试，在玛律大小和视频画质之间找到一个平衡的 <code>qscale</code> 数值。</p><p>目前所有的硬件加速选项都是类似这样的：<code>-c:v h264_qsv -qscale 15</code> ，这表示使用英特尔 h264 硬件加速编码器，视频质量参数为15。你可以更改里面的数值，以达到你期望的画质效果。</p></body>'''
            cursor.execute('''
                            insert into %s 
                            (name, outputOption, description) 
                            values (
                            '%s', 
                            '-c:v h264_amf -qscale 15 -b:a 256k',
                            '%s'
                            );'''
                           % (presetTableName, presetName, description.replace("'", "''")))

            # h264 压制 Nvidia 硬件加速
            presetName = self.tr('H264压制 Nvidia 硬件加速')
            description = '''<body><p>关于使用硬件加速：</p><p>目前硬件加速支持两种编码格式：H264 和 H265</p><p>有3种加速方法，分别对应三家的硬件：Inter、AMD、Nvidia</p><p>不过在苹果电脑上，不管你用的哪家的硬件，都是使用 videotoolbox 编码器。</p><p>需要注意的是，即便你的电脑拥有 Nvidia 显卡，可能也用不了 Nvidia 的硬件加速编码，因为 Nvidia 硬件加速依赖于显卡内部的一种特定的 GPU 的物理部分，专用于编码。只有在 GTX10 和 RTX20 以上的显卡才搭载有这个物理部分。</p><p>使用硬件编码器进行编码，只需要将输出选项中的编码器改成硬件编码器即可，其中：</p><ul><li><code>-c:v h264_qsv</code> 对应 Intel H264 编码</li><li><code>-c:v h264_amf</code> 对应 AMD H264 编码</li><li><code>-c:v h264_nvenc</code> 对应 Nvidia H264 编码</li><li><code>-c:v h264_videotoolbox</code> 对应苹果电脑的 H264 编码</li><li><code>-c:v hevc_qsv</code> 对应 Intel H265 编码</li><li><code>-c:v hevc_amf</code> 对应 AMDH265 编码</li><li><code>-c:v hevc_nvenc</code> 对应 Nvidia H265 编码</li><li><code>-c:v hevc_videotoolbox</code> 对应苹果电脑的 H265 编码</li></ul><p><code>-c:v</code> 表示视频（Video）的编码器（codec）</p><p>在使用硬件加速编码器的时候，控制输出视频的质量是使用 <code>qscale</code> 参数，他的数值可以从 <code>0.1 - 255</code> 不等，数值越小，画质越高，码率越大，输出文件体积越大。同一个数值对于不同的编码器画质的影响效果不同。所以你需要自己测试，在玛律大小和视频画质之间找到一个平衡的 <code>qscale</code> 数值。</p><p>目前所有的硬件加速选项都是类似这样的：<code>-c:v h264_qsv -qscale 15</code> ，这表示使用英特尔 h264 硬件加速编码器，视频质量参数为15。你可以更改里面的数值，以达到你期望的画质效果。</p></body>'''
            cursor.execute('''
                            insert into %s 
                            (name, outputOption, description) 
                            values (
                            '%s', 
                            '-c:v h264_nvenc -qscale 15 -b:a 256k',
                            '%s'
                            );'''
                           % (presetTableName, presetName, description.replace("'", "''")))

            # h264 压制 Mac 硬件加速
            presetName = self.tr('H264压制 Mac 硬件加速')
            description = '''<body><p>关于使用硬件加速：</p><p>目前硬件加速支持两种编码格式：H264 和 H265</p><p>有3种加速方法，分别对应三家的硬件：Inter、AMD、Nvidia</p><p>不过在苹果电脑上，不管你用的哪家的硬件，都是使用 videotoolbox 编码器。</p><p>需要注意的是，即便你的电脑拥有 Nvidia 显卡，可能也用不了 Nvidia 的硬件加速编码，因为 Nvidia 硬件加速依赖于显卡内部的一种特定的 GPU 的物理部分，专用于编码。只有在 GTX10 和 RTX20 以上的显卡才搭载有这个物理部分。</p><p>使用硬件编码器进行编码，只需要将输出选项中的编码器改成硬件编码器即可，其中：</p><ul><li><code>-c:v h264_qsv</code> 对应 Intel H264 编码</li><li><code>-c:v h264_amf</code> 对应 AMD H264 编码</li><li><code>-c:v h264_nvenc</code> 对应 Nvidia H264 编码</li><li><code>-c:v h264_videotoolbox</code> 对应苹果电脑的 H264 编码</li><li><code>-c:v hevc_qsv</code> 对应 Intel H265 编码</li><li><code>-c:v hevc_amf</code> 对应 AMDH265 编码</li><li><code>-c:v hevc_nvenc</code> 对应 Nvidia H265 编码</li><li><code>-c:v hevc_videotoolbox</code> 对应苹果电脑的 H265 编码</li></ul><p><code>-c:v</code> 表示视频（Video）的编码器（codec）</p><p>在使用硬件加速编码器的时候，控制输出视频的质量是使用 <code>qscale</code> 参数，他的数值可以从 <code>0.1 - 255</code> 不等，数值越小，画质越高，码率越大，输出文件体积越大。同一个数值对于不同的编码器画质的影响效果不同。所以你需要自己测试，在玛律大小和视频画质之间找到一个平衡的 <code>qscale</code> 数值。</p><p>目前所有的硬件加速选项都是类似这样的：<code>-c:v h264_qsv -qscale 15</code> ，这表示使用英特尔 h264 硬件加速编码器，视频质量参数为15。你可以更改里面的数值，以达到你期望的画质效果。</p></body>'''
            cursor.execute('''
                                        insert into %s 
                                        (name, outputOption, description) 
                                        values (
                                        '%s', 
                                        '-c:v h264_videotoolbox -qscale 15 -b:a 256k',
                                        '%s'
                                        );'''
                           % (presetTableName, presetName, description.replace("'", "''")))

            # h265压制
            presetName = self.tr('H265压制')
            description = '''h265 编码'''
            cursor.execute('''
                            insert into %s 
                            (name, outputOption, description) 
                            values (
                            "%s", 
                            "-c:v libx265 -crf 28 -b:a 256k",
                            '%s'
                            );'''
                           % (presetTableName, presetName, description.replace("'", "''")))

            # h265压制 Intel 硬件加速
            presetName = self.tr('H265压制 Intel 硬件加速')
            description = '''<body><p>关于使用硬件加速：</p><p>目前硬件加速支持两种编码格式：H264 和 H265</p><p>有3种加速方法，分别对应三家的硬件：Inter、AMD、Nvidia</p><p>不过在苹果电脑上，不管你用的哪家的硬件，都是使用 videotoolbox 编码器。</p><p>需要注意的是，即便你的电脑拥有 Nvidia 显卡，可能也用不了 Nvidia 的硬件加速编码，因为 Nvidia 硬件加速依赖于显卡内部的一种特定的 GPU 的物理部分，专用于编码。只有在 GTX10 和 RTX20 以上的显卡才搭载有这个物理部分。</p><p>使用硬件编码器进行编码，只需要将输出选项中的编码器改成硬件编码器即可，其中：</p><ul><li><code>-c:v h264_qsv</code> 对应 Intel H264 编码</li><li><code>-c:v h264_amf</code> 对应 AMD H264 编码</li><li><code>-c:v h264_nvenc</code> 对应 Nvidia H264 编码</li><li><code>-c:v h264_videotoolbox</code> 对应苹果电脑的 H264 编码</li><li><code>-c:v hevc_qsv</code> 对应 Intel H265 编码</li><li><code>-c:v hevc_amf</code> 对应 AMDH265 编码</li><li><code>-c:v hevc_nvenc</code> 对应 Nvidia H265 编码</li><li><code>-c:v hevc_videotoolbox</code> 对应苹果电脑的 H265 编码</li></ul><p><code>-c:v</code> 表示视频（Video）的编码器（codec）</p><p>在使用硬件加速编码器的时候，控制输出视频的质量是使用 <code>qscale</code> 参数，他的数值可以从 <code>0.1 - 255</code> 不等，数值越小，画质越高，码率越大，输出文件体积越大。同一个数值对于不同的编码器画质的影响效果不同。所以你需要自己测试，在玛律大小和视频画质之间找到一个平衡的 <code>qscale</code> 数值。</p><p>目前所有的硬件加速选项都是类似这样的：<code>-c:v h264_qsv -qscale 15</code> ，这表示使用英特尔 h264 硬件加速编码器，视频质量参数为15。你可以更改里面的数值，以达到你期望的画质效果。</p></body>'''
            cursor.execute('''
                            insert into %s 
                            (name, outputOption, description) 
                            values (
                            "%s", 
                            "-c:v hevc_qsv -qscale 15 -b:a 256k",
                            '%s'
                            );'''
                           % (presetTableName, presetName, description.replace("'", "''")))

            # h265压制 AMD 硬件加速
            presetName = self.tr('H265压制 AMD 硬件加速')
            description = '''<body><p>关于使用硬件加速：</p><p>目前硬件加速支持两种编码格式：H264 和 H265</p><p>有3种加速方法，分别对应三家的硬件：Inter、AMD、Nvidia</p><p>不过在苹果电脑上，不管你用的哪家的硬件，都是使用 videotoolbox 编码器。</p><p>需要注意的是，即便你的电脑拥有 Nvidia 显卡，可能也用不了 Nvidia 的硬件加速编码，因为 Nvidia 硬件加速依赖于显卡内部的一种特定的 GPU 的物理部分，专用于编码。只有在 GTX10 和 RTX20 以上的显卡才搭载有这个物理部分。</p><p>使用硬件编码器进行编码，只需要将输出选项中的编码器改成硬件编码器即可，其中：</p><ul><li><code>-c:v h264_qsv</code> 对应 Intel H264 编码</li><li><code>-c:v h264_amf</code> 对应 AMD H264 编码</li><li><code>-c:v h264_nvenc</code> 对应 Nvidia H264 编码</li><li><code>-c:v h264_videotoolbox</code> 对应苹果电脑的 H264 编码</li><li><code>-c:v hevc_qsv</code> 对应 Intel H265 编码</li><li><code>-c:v hevc_amf</code> 对应 AMDH265 编码</li><li><code>-c:v hevc_nvenc</code> 对应 Nvidia H265 编码</li><li><code>-c:v hevc_videotoolbox</code> 对应苹果电脑的 H265 编码</li></ul><p><code>-c:v</code> 表示视频（Video）的编码器（codec）</p><p>在使用硬件加速编码器的时候，控制输出视频的质量是使用 <code>qscale</code> 参数，他的数值可以从 <code>0.1 - 255</code> 不等，数值越小，画质越高，码率越大，输出文件体积越大。同一个数值对于不同的编码器画质的影响效果不同。所以你需要自己测试，在玛律大小和视频画质之间找到一个平衡的 <code>qscale</code> 数值。</p><p>目前所有的硬件加速选项都是类似这样的：<code>-c:v h264_qsv -qscale 15</code> ，这表示使用英特尔 h264 硬件加速编码器，视频质量参数为15。你可以更改里面的数值，以达到你期望的画质效果。</p></body>'''
            cursor.execute('''
                            insert into %s 
                            (name, outputOption, description) 
                            values (
                            "%s", 
                            "-c:v hevc_amf -qscale 15 -b:a 256k",
                            '%s'
                            );'''
                           % (presetTableName, presetName, description.replace("'", "''")))

            # h265压制 Nvidia 硬件加速
            presetName = self.tr('H265压制 Nvidia 硬件加速')
            description = '''<body><p>关于使用硬件加速：</p><p>目前硬件加速支持两种编码格式：H264 和 H265</p><p>有3种加速方法，分别对应三家的硬件：Inter、AMD、Nvidia</p><p>不过在苹果电脑上，不管你用的哪家的硬件，都是使用 videotoolbox 编码器。</p><p>需要注意的是，即便你的电脑拥有 Nvidia 显卡，可能也用不了 Nvidia 的硬件加速编码，因为 Nvidia 硬件加速依赖于显卡内部的一种特定的 GPU 的物理部分，专用于编码。只有在 GTX10 和 RTX20 以上的显卡才搭载有这个物理部分。</p><p>使用硬件编码器进行编码，只需要将输出选项中的编码器改成硬件编码器即可，其中：</p><ul><li><code>-c:v h264_qsv</code> 对应 Intel H264 编码</li><li><code>-c:v h264_amf</code> 对应 AMD H264 编码</li><li><code>-c:v h264_nvenc</code> 对应 Nvidia H264 编码</li><li><code>-c:v h264_videotoolbox</code> 对应苹果电脑的 H264 编码</li><li><code>-c:v hevc_qsv</code> 对应 Intel H265 编码</li><li><code>-c:v hevc_amf</code> 对应 AMDH265 编码</li><li><code>-c:v hevc_nvenc</code> 对应 Nvidia H265 编码</li><li><code>-c:v hevc_videotoolbox</code> 对应苹果电脑的 H265 编码</li></ul><p><code>-c:v</code> 表示视频（Video）的编码器（codec）</p><p>在使用硬件加速编码器的时候，控制输出视频的质量是使用 <code>qscale</code> 参数，他的数值可以从 <code>0.1 - 255</code> 不等，数值越小，画质越高，码率越大，输出文件体积越大。同一个数值对于不同的编码器画质的影响效果不同。所以你需要自己测试，在玛律大小和视频画质之间找到一个平衡的 <code>qscale</code> 数值。</p><p>目前所有的硬件加速选项都是类似这样的：<code>-c:v h264_qsv -qscale 15</code> ，这表示使用英特尔 h264 硬件加速编码器，视频质量参数为15。你可以更改里面的数值，以达到你期望的画质效果。</p></body>'''
            cursor.execute('''
                            insert into %s 
                            (name, outputOption, description) 
                            values (
                            "%s", 
                            "-c:v hevc_nvenc -qscale 15 -b:a 256k",
                            '%s'
                            );'''
                           % (presetTableName, presetName, description.replace("'", "''")))

            # h265压制 Mac 硬件加速
            presetName = self.tr('H265压制 Mac 硬件加速')
            description = '''<body><p>关于使用硬件加速：</p><p>目前硬件加速支持两种编码格式：H264 和 H265</p><p>有3种加速方法，分别对应三家的硬件：Inter、AMD、Nvidia</p><p>不过在苹果电脑上，不管你用的哪家的硬件，都是使用 videotoolbox 编码器。</p><p>需要注意的是，即便你的电脑拥有 Nvidia 显卡，可能也用不了 Nvidia 的硬件加速编码，因为 Nvidia 硬件加速依赖于显卡内部的一种特定的 GPU 的物理部分，专用于编码。只有在 GTX10 和 RTX20 以上的显卡才搭载有这个物理部分。</p><p>使用硬件编码器进行编码，只需要将输出选项中的编码器改成硬件编码器即可，其中：</p><ul><li><code>-c:v h264_qsv</code> 对应 Intel H264 编码</li><li><code>-c:v h264_amf</code> 对应 AMD H264 编码</li><li><code>-c:v h264_nvenc</code> 对应 Nvidia H264 编码</li><li><code>-c:v h264_videotoolbox</code> 对应苹果电脑的 H264 编码</li><li><code>-c:v hevc_qsv</code> 对应 Intel H265 编码</li><li><code>-c:v hevc_amf</code> 对应 AMDH265 编码</li><li><code>-c:v hevc_nvenc</code> 对应 Nvidia H265 编码</li><li><code>-c:v hevc_videotoolbox</code> 对应苹果电脑的 H265 编码</li></ul><p><code>-c:v</code> 表示视频（Video）的编码器（codec）</p><p>在使用硬件加速编码器的时候，控制输出视频的质量是使用 <code>qscale</code> 参数，他的数值可以从 <code>0.1 - 255</code> 不等，数值越小，画质越高，码率越大，输出文件体积越大。同一个数值对于不同的编码器画质的影响效果不同。所以你需要自己测试，在玛律大小和视频画质之间找到一个平衡的 <code>qscale</code> 数值。</p><p>目前所有的硬件加速选项都是类似这样的：<code>-c:v h264_qsv -qscale 15</code> ，这表示使用英特尔 h264 硬件加速编码器，视频质量参数为15。你可以更改里面的数值，以达到你期望的画质效果。</p></body>'''
            cursor.execute('''
                                        insert into %s 
                                        (name, outputOption, description) 
                                        values (
                                        "%s", 
                                        "-c:v hevc_videotoolbox -qscale 15 -b:a 256k",
                                        '%s'
                                        );'''
                           % (presetTableName, presetName, description.replace("'", "''")))


            # h264 恒定比特率压制
            presetName = self.tr('H264压制目标比特率6000k')
            description = '''h264恒定比特率压制'''
            cursor.execute('''
                            insert into %s 
                            (name, outputOption, description)
                            values (
                            "%s", 
                            "-b:a 256k -b:v 6000k",
                            '%s'
                            );'''
                           % (presetTableName, presetName, description.replace("'", "''")))

            # h264 恒定比特率二压
            presetName = self.tr('H264 二压 目标比特率2000k')
            description = '''h264恒定比特率二压'''
            extraCode = r"""nullPath = '/dev/null'
connector = '&&'
print(1)
platfm = platform.system()
print(2)
removeCommand = 'rm'
if platfm == 'Windows':
    nullPath = 'NUL'
    removeCommand = 'del'
print(3)
inputOne = self.输入1路径框.text()
inputOneWithoutExt = os.path.splitext(inputOne)[0]
outFile = self.输出路径框.text()
outFileWithoutExt = os.path.splitext(outFile)[0]
logFileName = outFileWithoutExt + r'-0.log'
print(logFileName)
if platfm == 'Windows':
    logFileName = logFileName.replace('/', '\\')
logTreeFileName = outFileWithoutExt + r'-0.log.mbtree'
if platfm == 'Windows':
    logTreeFileName = logTreeFileName.replace('/', '\\')
tempCommand = self.finalCommand.replace('"' + outFile + '"', r'-passlogfile "%s"' % (outFileWithoutExt) + ' "' + outFile + '"')
self.finalCommand = r'''ffmpeg -y -hide_banner -i "%s" -passlogfile "%s"  -c:v libx264 -pass 1 -an -f rawvideo "%s" %s %s %s %s "%s" %s %s "%s"''' % (inputOne, outFileWithoutExt, nullPath, connector, tempCommand, connector, removeCommand, logFileName, connector, removeCommand,logTreeFileName)
"""
            extraCode = extraCode.replace("'", "''")
            cursor.execute('''
                            insert into %s 
                            (name, outputOption, extraCode, description)
                            values (
                            "%s", 
                            "-c:v libx264 -pass 2 -b:v 2000k -preset slow -b:a 256k", 
                            '%s',
                            '%s'
                            );''' % (presetTableName, presetName, extraCode, description.replace("'", "''")))

            # 复制视频流到mp4容器
            presetName = self.tr('复制视频流到mp4容器')
            cursor.execute('''
                            insert into %s
                            (name, outputExt, outputOption)
                            values (
                            '%s', 
                            'mp4', 
                            '-c:v copy -b:a 256k'
                            );''' % (presetTableName, presetName))

            # 将输入文件打包到mkv格式容器
            presetName = self.tr('将输入文件打包到mkv格式容器')
            cursor.execute('''
                            insert into %s
                            (name, outputExt, outputOption)
                            values (
                            '%s', 
                            'mkv', 
                            '-c copy'
                            );'''
                           % (presetTableName, presetName))

            # 转码到mp3格式
            presetName = self.tr('转码到mp3格式')
            cursor.execute('''
                            insert into %s
                            (name, outputExt, outputOption)
                            values (
                            '%s', 
                            'mp3', 
                            '-vn -b:a 256k'
                            );''' % (presetTableName, presetName))

            # GIF (15fps 480p)
            presetName = self.tr('GIF (15fps 480p)')
            description = '''GIF (15fps 480p)'''
            cursor.execute('''
                            insert into %s 
                            (name, outputExt, outputOption, description)
                            values (
                            '%s', 
                            'gif', 
                            '-filter_complex "[0:v] scale=480:-1, fps=15, split [a][b];[a] palettegen [p];[b][p] paletteuse"',
                            '%s'
                            );''' % (presetTableName, presetName, description.replace("'", "''")))

            # 区域模糊
            presetName = self.tr('区域模糊')
            outputOption = '''-vf "split [main][tmp]; [tmp] crop=宽:高:X轴位置:Y轴位置, boxblur=luma_radius=25:luma_power=2:enable='between(t,第几秒开始,第几秒结束)'[tmp]; [main][tmp] overlay=X轴位置:Y轴位置"'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 视频两倍速
            presetName = self.tr('视频两倍速')
            outputOption = '''-filter_complex "[0:v]setpts=1/2*PTS[v];[0:a]atempo=2 [a]" -map "[v]" -map "[a]" '''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 音频两倍速
            presetName = self.tr('音频两倍速')
            outputOption = '''-filter_complex "[0:a]atempo=2.0[a]" -map "[a]"'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 视频0.5倍速 + 光流法补帧到60帧
            presetName = self.tr('视频0.5倍速 + 光流法补帧到60帧')
            outputOption = '''-filter_complex "[0:v]setpts=2*PTS[v];[0:a]atempo=1/2 [a];[v]minterpolate='mi_mode=mci:mc_mode=aobmc:me_mode=bidir:mb_size=16:vsbmc=1:fps=60'[v]" -map "[v]" -map "[a]" -max_muxing_queue_size 1024'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 光流法补帧到60帧
            presetName = self.tr('光流法补帧到60帧')
            outputOption = '''-filter_complex "[0:v]scale=-2:-2[v];[v]minterpolate='mi_mode=mci:mc_mode=aobmc:me_mode=bidir:mb_size=16:vsbmc=1:fps=60'" -max_muxing_queue_size 1024'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 视频倒放
            presetName = self.tr('视频倒放')
            outputOption = '''-vf reverse -af areverse'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 音频倒放
            presetName = self.tr('音频倒放')
            outputOption = '''-af areverse'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 设置画面比例
            presetName = self.tr('设置画面比例')
            outputOption = '''-aspect:0 16:9'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 视频流时间戳偏移，用于同步音画
            presetName = self.tr('视频流时间戳偏移，用于同步音画')
            inputOneOption = '''-itsoffset 1'''
            inputOneOption = inputOneOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, inputOneOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, inputOneOption))

            # 从视频区间每秒提取n张照片
            presetName = self.tr('从视频区间每秒提取n张照片')
            outputOption = ''' -r 1 -q:v 2 -f image2 -tatget pal-dvcd-r'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputExt, outputOption)
                            values (
                            '%s', 
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, r'%03d.jpg', outputOption))

            # 截取指定数量的帧保存为图片
            presetName = self.tr('截取指定数量的帧保存为图片')
            outputOption = '''-vframes 5'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputExt, outputOption)
                            values (
                            '%s', 
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, r'%03d.jpg', outputOption))

            # 一图流
            presetName = self.tr('一图流')
            outputOption = '''-c:v libx264 -tune stillimage -c:a aac -shortest'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, inputOneOption, outputOption)
                            values (
                            '%s', 
                            '-loop 1', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 裁切视频画面
            presetName = self.tr('裁切视频画面')
            outputOption = '''-strict -2 -vf crop=w:h:x:y'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 视频旋转度数
            presetName = self.tr('视频旋转度数')
            outputOption = '''-c copy -metadata:s:v:0 rotate=90'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 水平翻转画面
            presetName = self.tr('水平翻转画面')
            outputOption = '''-vf "hflip" '''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 垂直翻转画面
            presetName = self.tr('垂直翻转画面')
            outputOption = '''-vf "vflip" '''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 设定至指定分辨率，并且自动填充黑边
            presetName = self.tr('设定至指定分辨率，并且自动填充黑边')
            outputOption = '''-vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" '''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 视频或音乐添加封面图片
            presetName = self.tr('视频或音乐添加封面图片')
            outputOption = '''-map 0 -map 1 -c copy -c:v:1 jpg -disposition:v:1 attached_pic'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 声音响度标准化
            presetName = self.tr('声音响度标准化')
            outputOption = '''-af "loudnorm=i=-24.0:lra=7.0:tp=-2.0:" -c:v copy'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 音量大小调节
            presetName = self.tr('音量大小调节')
            outputOption = '''-af "volume=1.0"'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 静音第一个声道
            presetName = self.tr('静音第一个声道')
            outputOption = '''-map_channel -1 -map_channel 0.0.1 '''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 静音所有声道
            presetName = self.tr('静音所有声道')
            outputOption = '''-map_channel [-1]"'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 交换左右声道
            presetName = self.tr('交换左右声道')
            outputOption = '''-map_channel 0.0.1 -map_channel 0.0.0 '''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

            # 两个音频流混合到一个文件
            presetName = self.tr('两个音频流混合到一个文件')
            outputOption = '''-filter_complex "[0:1] [1:1] amerge" -c:v copy'''
            outputOption = outputOption.replace("'", "''")
            cursor.execute('''
                            insert into %s
                            (name, outputOption)
                            values (
                            '%s', 
                            '%s'
                            );''' % (presetTableName, presetName, outputOption))

        else:
            print('存储"预设"的表单已存在')
        self.conn.commit()
        # 不在这里关数据库了()
        return True

    # 将数据库的预设填入列表（更新列表）
    def refreshList(self):
        ########改用主数据库
        cursor = self.conn.cursor()
        presetData = cursor.execute(
            'select id, name, inputOneOption, inputTwoOption, outputExt, outputOption, extraCode from %s order by id' % (
                self.presetTableName))
        self.预设列表.clear()
        for i in presetData:
            self.预设列表.addItem(i[1])
        # 不在这里关数据库了()
        pass

    # 选择一个预设时，将预设中的命令填入相应的框
    def presetItemSelected(self, Index):
        if self.commandOptionsChanged == True:
            result = QMessageBox.question(self, '覆盖命令选项', '命令选项已经被手工修改过，使用预设会覆盖掉已修改的选项，确认要继续吗？', QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.No:
                return
        global 当前已选择的条目
        当前已选择的条目 = self.预设列表.item(self.预设列表.row(Index)).text()
        # print(当前已选择的条目)
        presetData = conn.cursor().execute(
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
        self.commandOptionsChanged = False

    # 点击添加一个预设
    def addPresetButtonClicked(self):
        dialog = self.SetupPresetItemDialog()

    # 点击删除按钮后删除预设
    def delPresetButtonClicked(self):
        global 当前已选择的条目
        try:
            当前已选择的条目
            answer = QMessageBox.question(self, self.tr('删除预设'), self.tr('将要删除“%s”预设，是否确认？') % (当前已选择的条目))
            if answer == QMessageBox.Yes:
                id = conn.cursor().execute(
                    '''select id from %s where name = '%s'; ''' % (presetTableName, 当前已选择的条目)).fetchone()[0]
                conn.cursor().execute("delete from %s where id = '%s'; " % (presetTableName, id))
                conn.cursor().execute("update %s set id=id-1 where id > %s" % (presetTableName, id))
                conn.commit()
                self.refreshList()
        except:
            QMessageBox.information(self, self.tr('删除失败'), self.tr('还没有选择要删除的预设'))

    # 向上移动预设
    def upwardButtonClicked(self):
        currentRow = self.预设列表.currentRow()
        if currentRow > 0:
            currentText = self.预设列表.currentItem().text()
            currentText = currentText.replace("'", "''")
            id = conn.cursor().execute(
                "select id from %s where name = '%s'" % (presetTableName, currentText)).fetchone()[0]
            conn.cursor().execute("update %s set id=10000 where id=%s-1 " % (presetTableName, id))
            conn.cursor().execute("update %s set id = id - 1 where name = '%s'" % (presetTableName, currentText))
            conn.cursor().execute("update %s set id=%s where id=10000 " % (presetTableName, id))
            conn.commit()
            self.refreshList()
            self.预设列表.setCurrentRow(currentRow - 1)

    # 向下移动预设
    def downwardButtonClicked(self):
        currentRow = self.预设列表.currentRow()
        totalRow = self.预设列表.count()
        if currentRow > -1 and currentRow < totalRow - 1:
            currentText = self.预设列表.currentItem().text()
            currentText = currentText.replace("'", "''")
            id = conn.cursor().execute(
                "select id from %s where name = '%s'" % (presetTableName, currentText)).fetchone()[0]
            conn.cursor().execute("update %s set id=10000 where id=%s+1 " % (presetTableName, id))
            conn.cursor().execute("update %s set id = id + 1 where name = '%s'" % (presetTableName, currentText))
            conn.cursor().execute("update %s set id=%s where id=10000 " % (presetTableName, id))
            conn.commit()
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
            dialog.setWindowTitle(self.tr('预设描述'))
            dialog.resize(1000, 800)
            textEdit = QTextEdit()
            font = QFont()
            layout = QHBoxLayout()
            layout.addWidget(textEdit)
            dialog.setLayout(layout)
            content = conn.cursor().execute("select description from %s where name = '%s'" % (
                presetTableName, self.预设列表.currentItem().text())).fetchone()[0]
            textEdit.setHtml(content)
            font.setPointSize(13)
            textEdit.setFont(font)
            print(True)
            dialog.exec()

    # 添加预设对话框
    class SetupPresetItemDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.initUI()

        def initUI(self):
            self.setWindowTitle(self.tr('添加或更新预设'))
            ########改用主数据库

            # 预设名称
            if True:
                self.预设名称标签 = QLabel(self.tr('预设名称：'))
                self.预设名称输入框 = QLineEdit()
                self.预设名称输入框.textChanged.connect(self.presetNameEditChanged)

            # 输入1选项
            if True:
                self.输入1选项标签 = QLabel(self.tr('输入1选项：'))
                self.输入1选项输入框 = QLineEdit()

            # 输入2选项
            if True:
                self.输入2选项标签 = QLabel(self.tr('输入2选项：'))
                self.输入2选项输入框 = QLineEdit()

            # 输出选项
            if True:
                # 输出后缀名
                if True:
                    self.输出后缀标签 = QLabel(self.tr('输出后缀名：'))
                    self.输出后缀输入框 = QLineEdit()
                # 输出选项
                if True:
                    self.输出选项标签 = QLabel(self.tr('输出选项：'))
                    self.输出选项输入框 = QPlainTextEdit()
                    self.输出选项输入框.setMaximumHeight(70)

            # 额外代码
            if True:
                self.额外代码标签 = QLabel(self.tr('额外代码：'))
                self.额外代码输入框 = QPlainTextEdit()
                self.额外代码输入框.setMaximumHeight(70)
                self.额外代码输入框.setPlaceholderText(self.tr('这里是用于实现一些比较复杂的预设的，普通用户不用管这个框'))

            # 描述
            if True:
                self.描述标签 = QLabel(self.tr('描述：'))
                self.描述输入框 = QTextEdit()

            # 底部按钮
            if True:
                self.submitButton = QPushButton(self.tr('确定'))
                self.submitButton.clicked.connect(self.submitButtonClicked)
                self.cancelButton = QPushButton(self.tr('取消'))
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
                    presetData = conn.cursor().execute(
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

            result = conn.cursor().execute(
                'select name from %s where name = "%s";' % (presetTableName, self.新预设名称)).fetchone()
            if result == None:
                try:
                    maxIdItem = conn.cursor().execute(
                        'select id from %s order by id desc' % presetTableName).fetchone()
                    if maxIdItem != None:
                        maxId = maxIdItem[0]
                    else:
                        maxId = 0
                    conn.cursor().execute(
                        '''insert into %s (id, name, inputOneOption, inputTwoOption, outputExt, outputOption, extraCode, description) values (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s');''' % (
                            presetTableName, maxId + 1, self.新预设名称, self.新预设输入1选项, self.新预设输入2选项, self.新预设输出后缀,
                            self.新预设输出选项,
                            self.新预设额外代码, self.新预设描述))
                    conn.commit()
                    QMessageBox.information(self, self.tr('添加预设'), self.tr('新预设添加成功'))
                    self.close()
                except:
                    QMessageBox.warning(self, self.tr('添加预设'), self.tr('新预设添加失败，你可以把失败过程重新操作记录一遍，然后发给作者'))
            else:
                answer = QMessageBox.question(self, self.tr('覆盖预设'), self.tr('''已经存在名字相同的预设，你可以选择换一个预设名字或者覆盖旧的预设。是否要覆盖？'''))
                if answer == QMessageBox.Yes:  # 如果同意覆盖
                    try:
                        conn.cursor().execute(
                            '''update %s set name = '%s', inputOneOption = '%s', inputTwoOption = '%s', outputExt = '%s', outputOption = '%s', extraCode = '%s', description = '%s' where name = '%s';''' % (
                                presetTableName, self.新预设名称, self.新预设输入1选项, self.新预设输入2选项, self.新预设输出后缀, self.新预设输出选项,
                                self.新预设额外代码, self.新预设描述, self.新预设名称))
                        # print(
                        #     '''update %s set name = '%s', inputOneOption = '%s', inputTwoOption = '%s', outputExt = '%s', outputOption = '%s', extraCode = '%s', description = '%s' where name = '%s';''' % (
                        #         presetTableName, self.新预设名称, self.新预设输入1选项, self.新预设输入2选项, self.新预设输出后缀, self.新预设输出选项,
                        #         self.新预设额外代码, self.新预设描述, self.新预设名称))
                        conn.commit()
                        QMessageBox.information(self, self.tr('更新预设'), self.tr('预设更新成功'))
                        self.close()
                    except:
                        QMessageBox.warning(self, self.tr('更新预设'), self.tr('预设更新失败，你可以把失败过程重新操作记录一遍，然后发给作者'))

        def closeEvent(self, a0: QCloseEvent) -> None:
            try:
                # 不在这里关数据库了()
                mainWindow.ffmpegMainTab.refreshList()
            except:
                pass

    # 点击会变化“截取时长”、 “截止时刻”的label
    class ClickableEndTimeLable(QLabel):
        def __init__(self):
            super().__init__()
            self.setText(self.tr('截取时长：'))

        def enterEvent(self, *args, **kwargs):
            mainWindow.status.showMessage(self.tr('点击交换“截取时长”和“截止时刻”'))

        def leaveEvent(self, *args, **kwargs):
            mainWindow.status.showMessage('')

        def mousePressEvent(self, QMouseEvent):
            # print(self.text())
            if self.text() == self.tr('截取时长：'):
                self.setText(self.tr('截止时刻：'))
            else:
                self.setText(self.tr('截取时长：'))
            mainWindow.ffmpegMainTab.generateFinalCommand()

    # 点击会交换横竖分辨率的 label
    class ClickableResolutionTimesLable(QLabel):
        def __init__(self):
            # global main
            super().__init__()
            self.setText('×')
            self.setToolTip(self.tr('点击交换横纵分辨率'))
            # mainWindow.status.showMessage('1')

        def enterEvent(self, *args, **kwargs):
            mainWindow.status.showMessage(self.tr('点击交换横竖分辨率'))

        def leaveEvent(self, *args, **kwargs):
            mainWindow.status.showMessage('')

        def mousePressEvent(self, QMouseEvent):
            x = mainWindow.ffmpegMainTab.X轴分辨率输入框.text()
            mainWindow.ffmpegMainTab.X轴分辨率输入框.setText(mainWindow.ffmpegMainTab.Y轴分辨率输入框.text())
            mainWindow.ffmpegMainTab.Y轴分辨率输入框.setText(x)

    # 分辨率预设 dialog
    class ResolutionDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.resolutions = ['4096 x 2160 (Ultra HD 4k)', '2560 x 1440 (Quad HD 2k)', '1920 x 1080 (Full HD 1080p)',
                                '1280 x 720 (HD 720p)', '720 x 480 (480p)', '480 x 360 (360p)']
            self.setWindowTitle(self.tr('选择分辨率预设'))
            self.listWidget = QListWidget()
            self.listWidget.addItems(self.resolutions)
            self.listWidget.itemDoubleClicked.connect(self.setResolution)
            self.layout = QVBoxLayout()
            self.layout.addWidget(self.listWidget)
            self.setLayout(self.layout)
            self.exec()

        def setResolution(self):
            resolution = re.findall('\d+', self.listWidget.currentItem().text())
            mainWindow.ffmpegMainTab.X轴分辨率输入框.setText(resolution[0])
            mainWindow.ffmpegMainTab.Y轴分辨率输入框.setText(resolution[1])
            self.close()

    # 剪切时间的提示 QLineEdit
    class CutTimeEdit(QLineEdit):
        def __init__(self):
            super().__init__()
            self.setAlignment(Qt.AlignCenter)

        def enterEvent(self, *args, **kwargs):
            mainWindow.status.showMessage(self.tr('例如 “00:05.00”、“23.189”、“12:03:45”的形式都是有效的，注意冒号是英文冒号'))

        def leaveEvent(self, *args, **kwargs):
            mainWindow.status.showMessage('')

    # 分辨率的提示 QLineEdit
    class ResolutionEdit(QLineEdit):
        def __init__(self):
            super().__init__()
            self.setAlignment(Qt.AlignCenter)

        def enterEvent(self, *args, **kwargs):
            mainWindow.status.showMessage(self.tr('负数表示自适应。例如，“ 720 × -2 ” 表示横轴分辨率为 720，纵轴分辨率为自适应且能够整除 -2'))

        def leaveEvent(self, *args, **kwargs):
            mainWindow.status.showMessage('')