# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from moduels.component.NormalValue import 常量

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
            if 常量.主Tab当前已选择的预设名称 != None:
                presetData = 常量.conn.cursor().execute(
                    'select id, name, inputOneOption, inputTwoOption, outputExt, outputOption, extraCode, description from %s where name = "%s"' % (
                        常量.presetTableName, 常量.主Tab当前已选择的预设名称)).fetchone()
                if presetData != None:
                    self.inputOneOption = presetData[2]
                    self.inputTwoOption = presetData[3]
                    self.outputExt = presetData[4]
                    self.outputOption = presetData[5]
                    self.extraCode = presetData[6]
                    self.description = presetData[7]

                    self.预设名称输入框.setText(常量.主Tab当前已选择的预设名称)
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

        result = 常量.conn.cursor().execute(
            'select name from %s where name = "%s";' % (常量.presetTableName, self.新预设名称)).fetchone()
        if result == None:
            try:
                maxIdItem = 常量.conn.cursor().execute(
                    'select id from %s order by id desc' % 常量.presetTableName).fetchone()
                if maxIdItem != None:
                    maxId = maxIdItem[0]
                else:
                    maxId = 0
                常量.conn.cursor().execute(
                    '''insert into %s (id, name, inputOneOption, inputTwoOption, outputExt, outputOption, extraCode, description) values (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s');''' % (
                        常量.presetTableName, maxId + 1, self.新预设名称, self.新预设输入1选项, self.新预设输入2选项, self.新预设输出后缀,
                        self.新预设输出选项,
                        self.新预设额外代码, self.新预设描述))
                常量.conn.commit()
                QMessageBox.information(self, self.tr('添加预设'), self.tr('新预设添加成功'))
                self.close()
            except:
                QMessageBox.warning(self, self.tr('添加预设'), self.tr('新预设添加失败，你可以把失败过程重新操作记录一遍，然后发给作者'))
        else:
            answer = QMessageBox.question(self, self.tr('覆盖预设'), self.tr('''已经存在名字相同的预设，你可以选择换一个预设名字或者覆盖旧的预设。是否要覆盖？'''))
            if answer == QMessageBox.Yes:  # 如果同意覆盖
                try:
                    常量.conn.cursor().execute(
                        '''update %s set name = '%s', inputOneOption = '%s', inputTwoOption = '%s', outputExt = '%s', outputOption = '%s', extraCode = '%s', description = '%s' where name = '%s';''' % (
                            常量.presetTableName, self.新预设名称, self.新预设输入1选项, self.新预设输入2选项, self.新预设输出后缀, self.新预设输出选项,
                            self.新预设额外代码, self.新预设描述, self.新预设名称))
                    # print(
                    #     '''update %s set name = '%s', inputOneOption = '%s', inputTwoOption = '%s', outputExt = '%s', outputOption = '%s', extraCode = '%s', description = '%s' where name = '%s';''' % (
                    #         常量.presetTableName, self.新预设名称, self.新预设输入1选项, self.新预设输入2选项, self.新预设输出后缀, self.新预设输出选项,
                    #         self.新预设额外代码, self.新预设描述, self.新预设名称))
                    常量.conn.commit()
                    QMessageBox.information(self, self.tr('更新预设'), self.tr('预设更新成功'))
                    self.close()
                except:
                    QMessageBox.warning(self, self.tr('更新预设'), self.tr('预设更新失败，你可以把失败过程重新操作记录一遍，然后发给作者'))

    def closeEvent(self, a0: QCloseEvent) -> None:
        try:
            常量.mainWindow.ffmpegMainTab.refreshList()
        except:
            print('FFmpeg 主 Tab 预设列表刷新失败')
