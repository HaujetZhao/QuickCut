# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import os
import re

# try:
from moduels.component.MyQLine import MyQLine
from moduels.component.MyQLine import MyQLine
from moduels.component.NormalValue import 常量
from moduels.component.SetupPresetItemDialog import SetupPresetItemDialog
from moduels.function.execute import execute
# except:
#     from QuickCut.


class FFmpegMainTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initGui()
        self.initValue()


    def initGui(self):
        self.输入输出vbox = QVBoxLayout()
        # 构造输入一、输入二和输出选项
        self.GUI输入输出()

        # 预设列表
        self.GUI预设列表()

        # 总命令编辑框
        self.GUI总命令编辑框()

        # 放置三个主要部件
        self.GUI总布局()


    def GUI输入输出(self):
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

    def GUI预设列表(self):
        self.预设列表提示标签 = QLabel(self.tr('选择预设：'))
        self.预设列表 = QListWidget()
        self.预设列表.itemClicked.connect(self.presetItemSelected)
        self.预设列表.itemDoubleClicked.connect(self.addPresetButtonClicked)

        self.添加预设按钮 = QPushButton('+')
        self.删除预设按钮 = QPushButton('-')
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
        self.预设vbox.addWidget(self.查看预设帮助按钮, 4, 0, 1, 2)
        self.预设vbox控件 = QWidget()
        self.预设vbox控件.setLayout(self.预设vbox)

        self.上移预设按钮.clicked.connect(self.upwardButtonClicked)
        self.下移预设按钮.clicked.connect(self.downwardButtonClicked)
        self.添加预设按钮.clicked.connect(self.addPresetButtonClicked)
        self.删除预设按钮.clicked.connect(self.delPresetButtonClicked)
        self.查看预设帮助按钮.clicked.connect(self.checkPresetHelpButtonClicked)

    def GUI总命令编辑框(self):
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

    def GUI总布局(self):
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

    # 将数据库的预设填入列表（更新列表）
    def refreshList(self):
        ########改用主数据库
        cursor = 常量.conn.cursor()
        presetData = cursor.execute(
            'select id, name, inputOneOption, inputTwoOption, outputExt, outputOption, extraCode from %s order by id' % (
                常量.ffmpeg预设的表名))
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
        
        常量.主Tab当前已选择的预设名称 = self.预设列表.item(self.预设列表.row(Index)).text()
        # print(常量.主Tab当前已选择的预设名称)
        presetData = 常量.conn.cursor().execute(
            'select id, name, inputOneOption, inputTwoOption, outputExt, outputOption, extraCode, description from %s where name = "%s"' % (
                常量.ffmpeg预设的表名, 常量.主Tab当前已选择的预设名称)).fetchone()
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
        dialog = SetupPresetItemDialog()

    # 点击删除按钮后删除预设
    def delPresetButtonClicked(self):
        
        try:
            常量.主Tab当前已选择的预设名称
            answer = QMessageBox.question(self, self.tr('删除预设'), self.tr('将要删除“%s”预设，是否确认？') % (常量.主Tab当前已选择的预设名称))
            if answer == QMessageBox.Yes:
                id = 常量.conn.cursor().execute(
                    '''select id from %s where name = '%s'; ''' % (常量.ffmpeg预设的表名, 常量.主Tab当前已选择的预设名称)).fetchone()[0]
                常量.conn.cursor().execute("delete from %s where id = '%s'; " % (常量.ffmpeg预设的表名, id))
                常量.conn.cursor().execute("update %s set id=id-1 where id > %s" % (常量.ffmpeg预设的表名, id))
                常量.conn.commit()
                self.refreshList()
        except:
            QMessageBox.information(self, self.tr('删除失败'), self.tr('还没有选择要删除的预设'))

    # 向上移动预设
    def upwardButtonClicked(self):
        currentRow = self.预设列表.currentRow()
        if currentRow > 0:
            currentText = self.预设列表.currentItem().text()
            currentText = currentText.replace("'", "''")
            id = 常量.conn.cursor().execute(
                "select id from %s where name = '%s'" % (常量.ffmpeg预设的表名, currentText)).fetchone()[0]
            常量.conn.cursor().execute("update %s set id=10000 where id=%s-1 " % (常量.ffmpeg预设的表名, id))
            常量.conn.cursor().execute("update %s set id = id - 1 where name = '%s'" % (常量.ffmpeg预设的表名, currentText))
            常量.conn.cursor().execute("update %s set id=%s where id=10000 " % (常量.ffmpeg预设的表名, id))
            常量.conn.commit()
            self.refreshList()
            self.预设列表.setCurrentRow(currentRow - 1)

    # 向下移动预设
    def downwardButtonClicked(self):
        currentRow = self.预设列表.currentRow()
        totalRow = self.预设列表.count()
        if currentRow > -1 and currentRow < totalRow - 1:
            currentText = self.预设列表.currentItem().text()
            currentText = currentText.replace("'", "''")
            id = 常量.conn.cursor().execute(
                "select id from %s where name = '%s'" % (常量.ffmpeg预设的表名, currentText)).fetchone()[0]
            常量.conn.cursor().execute("update %s set id=10000 where id=%s+1 " % (常量.ffmpeg预设的表名, id))
            常量.conn.cursor().execute("update %s set id = id + 1 where name = '%s'" % (常量.ffmpeg预设的表名, currentText))
            常量.conn.cursor().execute("update %s set id=%s where id=10000 " % (常量.ffmpeg预设的表名, id))
            常量.conn.commit()
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
            content = 常量.conn.cursor().execute("select description from %s where name = '%s'" % (
                常量.ffmpeg预设的表名, self.预设列表.currentItem().text())).fetchone()[0]
            textEdit.setHtml(content)
            font.setPointSize(13)
            textEdit.setFont(font)
            print(True)
            dialog.exec()

    # 点击会变化“截取时长”、 “截止时刻”的label
    class ClickableEndTimeLable(QLabel):
        def __init__(self):
            super().__init__()
            self.setText(self.tr('截取时长：'))

        def enterEvent(self, *args, **kwargs):
            常量.mainWindow.状态栏.showMessage(self.tr('点击交换“截取时长”和“截止时刻”'))

        def leaveEvent(self, *args, **kwargs):
            常量.mainWindow.状态栏.showMessage('')

        def mousePressEvent(self, QMouseEvent):
            # print(self.text())
            if self.text() == self.tr('截取时长：'):
                self.setText(self.tr('截止时刻：'))
            else:
                self.setText(self.tr('截取时长：'))
            常量.mainWindow.ffmpeg主功能Tab.生成最终命令()

    # 点击会交换横竖分辨率的 label
    class ClickableResolutionTimesLable(QLabel):
        def __init__(self):
            # global main
            super().__init__()
            self.setText('×')
            self.setToolTip(self.tr('点击交换横纵分辨率'))
            # mainWindow.status.showMessage('1')

        def enterEvent(self, *args, **kwargs):
            常量.mainWindow.状态栏.showMessage(self.tr('点击交换横竖分辨率'))

        def leaveEvent(self, *args, **kwargs):
            常量.mainWindow.状态栏.showMessage('')

        def mousePressEvent(self, QMouseEvent):
            x = 常量.mainWindow.ffmpeg主功能Tab.X轴分辨率输入框.text()
            常量.mainWindow.ffmpeg主功能Tab.X轴分辨率输入框.setText(常量.mainWindow.ffmpeg主功能Tab.Y轴分辨率输入框.text())
            常量.mainWindow.ffmpeg主功能Tab.Y轴分辨率输入框.setText(x)

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
            常量.mainWindow.ffmpeg主功能Tab.X轴分辨率输入框.setText(resolution[0])
            常量.mainWindow.ffmpeg主功能Tab.Y轴分辨率输入框.setText(resolution[1])
            self.close()

    # 剪切时间的提示 QLineEdit
    class CutTimeEdit(QLineEdit):
        def __init__(self):
            super().__init__()
            self.setAlignment(Qt.AlignCenter)

        def enterEvent(self, *args, **kwargs):
            常量.mainWindow.状态栏.showMessage(self.tr('例如 “00:05.00”、“23.189”、“12:03:45”的形式都是有效的，注意冒号是英文冒号'))

        def leaveEvent(self, *args, **kwargs):
            常量.mainWindow.状态栏.showMessage('')

    # 分辨率的提示 QLineEdit
    class ResolutionEdit(QLineEdit):
        def __init__(self):
            super().__init__()
            self.setAlignment(Qt.AlignCenter)

        def enterEvent(self, *args, **kwargs):
            常量.mainWindow.状态栏.showMessage(self.tr('负数表示自适应。例如，“ 720 × -2 ” 表示横轴分辨率为 720，纵轴分辨率为自适应且能够整除 -2'))

        def leaveEvent(self, *args, **kwargs):
            常量.mainWindow.状态栏.showMessage('')
