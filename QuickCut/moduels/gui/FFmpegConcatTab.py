# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from moduels.component.FileListWidget import FileListWidget
from moduels.component.MyQLine import MyQLine
from moduels.component.NormalValue import 常量
from moduels.function.execute import execute

import os
from os import path

class FFmpegConcatTab(QWidget):
    def __init__(self):
        super().__init__()
        self.fileList = []
        self.initUI()


    def initUI(self):
        self.inputHintLabel = QLabel(self.tr('点击列表右下边的加号添加要合并的视频片段：'))
        self.fileListWidget = FileListWidget(self)  # 文件表控件
        self.fileListWidget.setAcceptDrops(True)

        self.fileListWidget.doubleClicked.connect(self.文件列表组件被双击)
        # self.fileListWidget.setLineWidth(1)

        self.masterVLayout = QVBoxLayout()
        self.masterVLayout.addWidget(self.inputHintLabel)
        self.masterVLayout.addWidget(self.fileListWidget)

        self.buttonHLayout = QHBoxLayout()
        self.upButton = QPushButton('↑')
        self.upButton.clicked.connect(self.向上按钮被单击)
        self.downButton = QPushButton('↓')
        self.downButton.clicked.connect(self.向下按钮被单击)
        self.reverseButton = QPushButton(self.tr('倒序'))
        self.reverseButton.clicked.connect(self.逆序按钮被单击)
        self.addButton = QPushButton('+')
        self.addButton.clicked.connect(self.添加按钮被单击)
        self.fileListWidget.signal.connect(self.文件拖入)
        self.delButton = QPushButton('-')
        self.delButton.clicked.connect(self.删除按钮被单击)
        self.buttonHLayout.addWidget(self.upButton)
        self.buttonHLayout.addWidget(self.downButton)
        self.buttonHLayout.addWidget(self.reverseButton)
        self.buttonHLayout.addWidget(self.addButton)
        self.buttonHLayout.addWidget(self.delButton)
        self.masterVLayout.addLayout(self.buttonHLayout)

        self.outputFileWidgetLayout = QHBoxLayout()
        self.outputHintLabel = QLabel(self.tr('输出：'))
        self.outputFileLineEdit = MyQLine()
        self.outputFileSelectButton = QPushButton(self.tr('选择保存位置'))
        self.outputFileSelectButton.clicked.connect(self.输出文件位置按钮被单击)
        self.outputFileWidgetLayout.addWidget(self.outputHintLabel)
        self.outputFileWidgetLayout.addWidget(self.outputFileLineEdit)
        self.outputFileWidgetLayout.addWidget(self.outputFileSelectButton)
        self.masterVLayout.addLayout(self.outputFileWidgetLayout)

        self.methodVLayout = QVBoxLayout()

        self.concatRadioButton = QRadioButton(self.tr('concat格式衔接，不重新解码、编码（快、无损、要求格式一致）'))
        self.tsRadioButton = QRadioButton(self.tr('先转成 ts 格式，再衔接，要解码、编码（用于合并不同格式）'))
        self.concatFilterVStream0RadioButton = QRadioButton(self.tr('concat滤镜衔接（视频为Stream0），要解码、编码'))
        self.concatFilterAStream0RadioButton = QRadioButton(self.tr('concat滤镜衔接（音频为Stream0），要解码、编码'))
        self.methodVLayout.addWidget(self.concatRadioButton)
        self.methodVLayout.addWidget(self.tsRadioButton)
        self.methodVLayout.addWidget(self.concatFilterVStream0RadioButton)
        self.methodVLayout.addWidget(self.concatFilterAStream0RadioButton)

        self.finalCommandBoxLayout = QVBoxLayout()
        self.finalCommandEditBox = QPlainTextEdit()
        self.finalCommandEditBox.setPlaceholderText(self.tr('这里是自动生成的总命令'))
        self.runCommandButton = QPushButton(self.tr('运行'))
        self.runCommandButton.clicked.connect(self.执行按钮被单击)
        self.finalCommandBoxLayout.addWidget(self.finalCommandEditBox)
        self.finalCommandBoxLayout.addWidget(self.runCommandButton)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.addLayout(self.methodVLayout)
        self.bottomLayout.addLayout(self.finalCommandBoxLayout)

        self.masterVLayout.addLayout(self.bottomLayout)
        self.setLayout(self.masterVLayout)

        self.刷新文件列表()

        self.concatRadioButton.clicked.connect(lambda: self.concat方式项被单击('concatFormat'))
        self.concatFilterVStream0RadioButton.clicked.connect(
            lambda: self.concat方式项被单击('concatFilterVStreamFirst'))
        self.tsRadioButton.clicked.connect(lambda: self.concat方式项被单击('tsConcat'))
        self.concatFilterAStream0RadioButton.clicked.connect(
            lambda: self.concat方式项被单击('concatFilterAStreamFirst'))
        self.outputFileLineEdit.textChanged.connect(self.生成最终命令)
        self.concatRadioButton.setChecked(True)
        self.concatMethod = 'concatFormat'

    def 文件拖入(self, list):
        self.fileList += list
        self.刷新文件列表()
        if len(self.fileList) == len(list):
            目录 = path.dirname(list[0])
            文件名 = '输出'
            后缀 = path.splitext(list[0])[1]
            self.outputFileLineEdit.setText('/'.join([目录, 文件名 + 后缀]))

    def 刷新文件列表(self):
        self.fileListWidget.clear()
        self.fileListWidget.addItems(self.fileList)
        self.生成最终命令()

    def concat方式项被单击(self, method):
        self.concatMethod = method
        self.生成最终命令()

    def 文件列表组件被双击(self):
        # print(True)
        result = QMessageBox.warning(self, self.tr('清空列表'), self.tr('是否确认清空列表？'), QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if result == QMessageBox.Yes:
            self.fileList.clear()
            self.刷新文件列表()

    def 向上按钮被单击(self):
        itemCurrentPosition = self.fileListWidget.currentRow()
        if itemCurrentPosition > 0:
            temp = self.fileList[itemCurrentPosition]
            self.fileList.insert(itemCurrentPosition - 1, temp)
            self.fileList.pop(itemCurrentPosition + 1)
            self.刷新文件列表()
            self.fileListWidget.setCurrentRow(itemCurrentPosition - 1)

    def 向下按钮被单击(self):
        itemCurrentPosition = self.fileListWidget.currentRow()
        if itemCurrentPosition > -1 and itemCurrentPosition < len(self.fileList) - 1:
            temp = self.fileList[itemCurrentPosition]
            self.fileList.insert(itemCurrentPosition + 2, temp)
            self.fileList.pop(itemCurrentPosition)
            self.刷新文件列表()
            self.fileListWidget.setCurrentRow(itemCurrentPosition + 1)

    def 逆序按钮被单击(self):
        self.fileList.reverse()
        self.刷新文件列表()

    def 添加按钮被单击(self):
        list, _ = QFileDialog().getOpenFileNames(self, self.tr('添加音视频文件'), None)
        self.fileList += list
        self.刷新文件列表()
        if len(self.fileList) == len(list):
            目录 = path.dirname(list[0])
            文件名 = '输出'
            后缀 = path.splitext(list[0])[1]
            self.outputFileLineEdit.setText('/'.join([目录, 文件名 + 后缀]))



    def 删除按钮被单击(self):
        currentPosition = self.fileListWidget.currentRow()
        if currentPosition > -1:
            self.fileList.pop(currentPosition)
            self.刷新文件列表()
            if len(self.fileList) > 0:
                self.fileListWidget.setCurrentRow(currentPosition)

    def 输出文件位置按钮被单击(self):
        file, _ = QFileDialog.getSaveFileName(self, self.tr('选择保存位置'), 'out.mp4')
        if file != '':
            self.outputFileLineEdit.setText(file)

    def 生成最终命令(self):
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
                    tsOutPath = path.splitext(i)[0] + '.ts'
                    finalCommand = finalCommand + '''ffmpeg -y -hide_banner -i "%s" -c copy -bsf:v h264_mp4toannexb -f mpegts "%s" && ''' % (
                        i, tsOutPath)
                    inputTsFiles = inputTsFiles + tsOutPath + '|'
                if inputTsFiles[-1] == '|':
                    inputTsFiles = inputTsFiles[0:-1]
                # print(inputTsFiles)
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

    def 执行按钮被单击(self):
        execute(self.finalCommandEditBox.toPlainText())
