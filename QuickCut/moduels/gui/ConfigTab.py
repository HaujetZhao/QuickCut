# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtSql import *
from moduels.component.NormalValue import 常量
import os


class ConfigTab(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = 常量.conn
        self.dbname = 常量.dbname
        self.ossTableName = 常量.ossTableName
        self.apiTableName = 常量.apiTableName
        self.preferenceTableName = 常量.preferenceTableName
        self.initGui()

    def initGui(self):

        self.masterLayout = QVBoxLayout()
        # self.masterLayout.addSpacing(10)

        # 对象存储部分
        if True:
            self.ossGroup = QGroupBox(self.tr('OSS对象存储设置'))
            self.masterLayout.addWidget(self.ossGroup)
            self.ossConfigBoxLayout = QVBoxLayout()
            self.ossGroup.setLayout(self.ossConfigBoxLayout)

            # self.masterLayout.addStretch(0)
            self.ossProviderBoxLayout = QHBoxLayout()
            self.ossConfigBoxLayout.addLayout(self.ossProviderBoxLayout)
            self.ossAliProviderRadioButton = QRadioButton(self.tr('阿里OSS'))
            self.ossTencentProviderRadioButton = QRadioButton(self.tr('腾讯OSS'))
            self.ossProviderBoxLayout.addWidget(self.ossAliProviderRadioButton)
            self.ossProviderBoxLayout.addWidget(self.ossTencentProviderRadioButton)

            self.ossConfigFormLayout = QFormLayout()
            self.endPointLineEdit = QLineEdit()
            self.bucketNameLineEdit = QLineEdit()
            self.accessKeyIdLineEdit = QLineEdit()
            self.accessKeyIdLineEdit.setEchoMode(QLineEdit.Password)
            self.accessKeySecretLineEdit = QLineEdit()
            self.accessKeySecretLineEdit.setEchoMode(QLineEdit.Password)
            self.ossConfigFormLayout.addRow('EndPoint：', self.endPointLineEdit)
            self.ossConfigFormLayout.addRow('BucketName：', self.bucketNameLineEdit)
            self.ossConfigFormLayout.addRow('AccessKeyID：', self.accessKeyIdLineEdit)
            self.ossConfigFormLayout.addRow('AccessKeySecret：', self.accessKeySecretLineEdit)
            self.ossConfigBoxLayout.addLayout(self.ossConfigFormLayout)

            self.getOssData()

            self.saveOssConfigButton = QPushButton(self.tr('保存OSS配置'))
            self.saveOssConfigButton.clicked.connect(self.saveOssData)
            self.cancelOssConfigButton = QPushButton(self.tr('取消'))
            self.cancelOssConfigButton.clicked.connect(self.getOssData)
            self.ossConfigButtonLayout = QHBoxLayout()
            self.ossConfigButtonLayout.addWidget(self.saveOssConfigButton)
            self.ossConfigButtonLayout.addWidget(self.cancelOssConfigButton)
            self.ossConfigBoxLayout.addLayout(self.ossConfigButtonLayout)

        # self.masterLayout.addSpacing(10)

        # 语音api部分
        if True:
            self.apiGroup = QGroupBox(self.tr('语音 Api'))
            self.masterLayout.addWidget(self.apiGroup)
            self.apiBoxLayout = QVBoxLayout()
            self.apiGroup.setLayout(self.apiBoxLayout)
            # self.apiBoxLayout.addStretch(0)

            self.db = QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(self.dbname)
            self.model = QSqlTableModel()  # api 表的模型
            self.delrow = -1
            self.model.setTable(self.apiTableName)
            self.model.setEditStrategy(QSqlTableModel.OnRowChange)
            self.model.select()
            self.model.setHeaderData(0, Qt.Horizontal, 'id')
            self.model.setHeaderData(1, Qt.Horizontal, self.tr('引擎名称'))

            self.model.setHeaderData(2, Qt.Horizontal, self.tr('服务商'))

            self.model.setHeaderData(3, Qt.Horizontal, 'AppKey')

            self.model.setHeaderData(4, Qt.Horizontal, self.tr('语言'))

            self.model.setHeaderData(5, Qt.Horizontal, 'AccessKeyId')

            self.model.setHeaderData(6, Qt.Horizontal, 'AccessKeySecret')

            self.apiTableView = QTableView()

            self.apiTableView.setModel(self.model)

            self.apiTableView.hideColumn(0)

            self.apiTableView.hideColumn(5)

            self.apiTableView.hideColumn(6)

            self.apiTableView.setColumnWidth(1, 150)

            self.apiTableView.setColumnWidth(2, 100)

            self.apiTableView.setColumnWidth(3, 150)

            self.apiTableView.setColumnWidth(4, 200)

            self.apiTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

            self.apiTableView.setSelectionBehavior(QAbstractItemView.SelectRows)

            # self.apiTableView.setsize(600)
            self.apiBoxLayout.addWidget(self.apiTableView)

            # self.apiBoxLayout.addStretch(0)

            self.appKeyControlButtonLayout = QHBoxLayout()
            self.upApiButton = QPushButton('↑')
            self.upApiButton.clicked.connect(self.upApiButtonClicked)
            self.downApiButton = QPushButton('↓')
            self.downApiButton.clicked.connect(self.downApiButtonClicked)
            self.addApiButton = QPushButton('+')
            self.addApiButton.clicked.connect(self.addApiButtonClicked)
            self.delApiButton = QPushButton('-')
            self.delApiButton.clicked.connect(self.delApiButtonClicked)
            self.appKeyControlButtonLayout.addWidget(self.upApiButton)
            self.appKeyControlButtonLayout.addWidget(self.downApiButton)
            self.appKeyControlButtonLayout.addWidget(self.addApiButton)
            self.appKeyControlButtonLayout.addWidget(self.delApiButton)
            self.apiBoxLayout.addLayout(self.appKeyControlButtonLayout)
            # self.apiBoxLayout.addStretch(0)

        # self.masterLayout.addSpacing(10)

        # 偏好设置
        if True:
            self.preferenceGroup = QGroupBox(self.tr('偏好设置'))
            self.masterLayout.addWidget(self.preferenceGroup)
            self.preferenceGroupLayout = QHBoxLayout()
            self.preferenceGroup.setLayout(self.preferenceGroupLayout)

            self.hideToSystemTraySwitch = QCheckBox(self.tr('点击关闭按钮时隐藏到托盘'))
            self.preferenceGroupLayout.addWidget(self.hideToSystemTraySwitch)


            self.resetFFmpegTemplateButton = QPushButton(self.tr('重置 FFmpeg 预设'))
            self.resetFFmpegTemplateButton.clicked.connect(self.resetFFmpegTemplateButtonClicked)
            self.preferenceGroupLayout.addWidget(self.resetFFmpegTemplateButton)
            self.preferenceGroupLayout.addSpacing(30)

            self.chooseLanguageHint = QLabel(self.tr('语言：'))
            self.chooseLanguageHint.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.preferenceGroupLayout.addWidget(self.chooseLanguageHint)



            self.chooseLanguageBox = QComboBox()
            self.preferenceGroupLayout.addWidget(self.chooseLanguageBox)
            self.initChooseLanguageBox()
            self.chooseLanguageBox.currentTextChanged.connect(self.chooseLanguageBoxTextChanged)

            # self.masterLayout.addSpacing(10)

            self.linkButtonGroup = QGroupBox(self.tr('链接按钮'))
            self.masterLayout.addWidget(self.linkButtonGroup)
            self.linkButtonGroupLayout = QHBoxLayout()
            self.linkButtonGroup.setLayout(self.linkButtonGroupLayout)

            self.buttonRowOneLayout = QHBoxLayout()
            self.openPythonWebsiteButton = QPushButton(self.tr('打开 Python 下载页面'))
            self.openFfmpegWebsiteButton = QPushButton(self.tr('打开 FFmpeg 下载页面'))
            self.installPipToolsButton = QPushButton(self.tr('安装 you-get 和 youtube-dl'))
            self.linkButtonGroupLayout.addWidget(self.openPythonWebsiteButton)
            self.linkButtonGroupLayout.addWidget(self.openFfmpegWebsiteButton)
            self.linkButtonGroupLayout.addWidget(self.installPipToolsButton)
            self.linkButtonGroupLayout.addLayout(self.buttonRowOneLayout)

            self.openPythonWebsiteButton.clicked.connect(lambda: webbrowser.open(r'https://www.python.org/downloads/'))
            self.openFfmpegWebsiteButton.clicked.connect(lambda: webbrowser.open(r'http://ffmpeg.org/download.html'))
            self.installPipToolsButton.clicked.connect(self.installYouGetAndYouTubeDl)

            # self.addEnvRowLayout = QHBoxLayout()
            # self.addEnvPathHint = QLabel('一键添加环境变量：')
            # self.addEnvPathBox = QLineEdit()
            # self.addEnvPathBox.setPlaceholderText('将要添加环境变量的路径复制到这里')
            # self.addEnvPathButton = QPushButton('添加输入的环境变量(win)')
            # self.addEnvRowLayout.addWidget(self.addEnvPathHint)
            # self.addEnvRowLayout.addWidget(self.addEnvPathBox)
            # self.addEnvRowLayout.addWidget(self.addEnvPathButton)
            # self.preferenceGroupLayout.addLayout(self.addEnvRowLayout)
            # self.addEnvPathButton.clicked.connect(self.setEnvironmentPath)

            ########改用主数据库
            hideToSystemTrayValue = self.conn.cursor().execute('''select value from %s where item = '%s';''' % (
            self.preferenceTableName, 'hideToTrayWhenHitCloseButton')).fetchone()[0]
            # 不在这里关数据库了()
            if hideToSystemTrayValue != 'False':
                self.hideToSystemTraySwitch.setChecked(True)
            self.hideToSystemTraySwitch.clicked.connect(self.hideToSystemTraySwitchClicked)
            # 不在这里关数据库了()

        self.setLayout(self.masterLayout)

    def resetFFmpegTemplateButtonClicked(self):
        answer = QMessageBox.question(self, self.tr('重置 FFmpeg 预设'), self.tr('''将要重置 FFmpeg Tab 的预设列表，是否确认？'''))
        if answer == QMessageBox.Yes:  # 如果同意重置
            try:
                conn.cursor().execute('''drop table %s;''' % presetTableName)
                conn.commit()
                mainWindow.ffmpegMainTab.createDB()
                mainWindow.ffmpegMainTab.refreshList()
                QMessageBox.information(main, self.tr('重置 FFmpeg 预设'), self.tr('重置 FFmpeg 预设成功'))
            except:
                QMessageBox.information(main, self.tr('重置 FFmpeg 预设'), self.tr('重置 FFmpeg 预设失败'))



    def installYouGetAndYouTubeDl(self):
        command = 'pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple you-get youtube-dl'
        thread = YouGetYoutubeDlInstallThread()
        thread.command = command
        window = Console(mainWindow)
        window.thread = thread
        thread.signal.connect(window.consoleBox.print)
        thread.signalForFFmpeg.connect(window.consoleBoxForFFmpeg.print)
        thread.start()


    def hideToSystemTraySwitchClicked(self):
        ########改用主数据库
        cursor = conn.cursor()
        cursor.execute('''update %s set %s='%s' where item = '%s';''' % (
        preferenceTableName, 'value', self.hideToSystemTraySwitch.isChecked(), 'hideToTrayWhenHitCloseButton'))
        conn.commit()
        # 不在这里关数据库了()

    def sendApiUpdatedBroadCast(self):
        apiUpdateBroadCaster.broadCastUpdates()

    def findRow(self, i):
        self.delrow = i.row()


        # 不在这里关数据库了()

    def initChooseLanguageBox(self):
        result = self.conn.cursor().execute('select value from %s where item = "language";' % (self.preferenceTableName))
        language = result.fetchone()[0]
        languageList = ['中文']
        for file in os.listdir('./languages'):
            pathSplited = os.path.splitext(file)
            if pathSplited[1] == '.qm':
                languageList.append(pathSplited[0]) # 将 qm 文件添加到语言列表
        self.chooseLanguageBox.addItems(languageList)
        self.chooseLanguageBox.setCurrentText(language)

    def chooseLanguageBoxTextChanged(self):
        conn.cursor().execute('''update %s set value = '%s' where item = 'language';''' % (preferenceTableName, self.chooseLanguageBox.currentText()))
        conn.commit()
        result = QMessageBox.information(self, self.tr('更改语言'), self.tr('更改的语言会在重启软件后生效'), QMessageBox.Ok)

    def getOssData(self):
        ########改用主数据库
        ossData = self.conn.cursor().execute(
            '''select provider, endPoint, bucketName, accessKeyId, accessKeySecret from %s''' % self.ossTableName).fetchone()
        if ossData != None:
            if ossData[0] == 'Alibaba':
                self.ossAliProviderRadioButton.setChecked(True)
            elif ossData[0] == 'Tencent':
                self.ossTencentProviderRadioButton.setChecked(True)
            self.endPointLineEdit.setText(ossData[1])
            self.bucketNameLineEdit.setText(ossData[2])
            self.accessKeyIdLineEdit.setText(ossData[3])
            self.accessKeySecretLineEdit.setText(ossData[4])
        # 不在这里关数据库了()

    def saveOssData(self):
        ########改用主数据库
        ossData = conn.cursor().execute(
            '''select provider, endPoint, bucketName, bucketDomain, accessKeyId, accessKeySecret from %s''' % ossTableName).fetchone()
        provider = ''
        if self.ossAliProviderRadioButton.isChecked():
            provider = 'Alibaba'
        elif self.ossTencentProviderRadioButton.isChecked():
            provider = 'Tencent'
        if ossData == None:
            # print('新建oss item')
            conn.cursor().execute(
                '''insert into %s (provider, endPoint, bucketName, accessKeyId, accessKeySecret) values ( '%s', '%s', '%s', '%s', '%s')''' % (
                    ossTableName, provider, self.endPointLineEdit.text(), self.bucketNameLineEdit.text(),
                    self.accessKeyIdLineEdit.text(),
                    self.accessKeySecretLineEdit.text()))
        else:
            # print('更新oss item')
            conn.cursor().execute(
                '''update %s set provider='%s', endPoint='%s', bucketName='%s', accessKeyId='%s', accessKeySecret='%s' where id=1 ''' % (
                    ossTableName, provider, self.endPointLineEdit.text(), self.bucketNameLineEdit.text(),
                    self.accessKeyIdLineEdit.text(),
                    self.accessKeySecretLineEdit.text()))
        conn.commit()
        # 不在这里关数据库了()

    def addApiButtonClicked(self):
        dialog = self.AddApiDialog()

    def delApiButtonClicked(self):
        ########改用主数据库
        currentRow = mainWindow.ConfigTab.apiTableView.currentIndex().row()
        # print(currentRow)
        if currentRow > -1:
            try:
                answer = QMessageBox.question(self, self.tr('删除 Api'), self.tr('将要删除选中的 Api，是否确认？'))
                if answer == QMessageBox.Yes:
                    conn.cursor().execute("delete from %s where id = %s; " % (apiTableName, currentRow + 1))
                    conn.cursor().execute("update %s set id=id-1 where id > %s" % (apiTableName, currentRow + 1))
                    conn.commit()
            except:
                QMessageBox.information(self, self.tr('删除失败'), self.tr('删除失败'))
            self.model.select()
        self.sendApiUpdatedBroadCast()

    def upApiButtonClicked(self):
        ########改用主数据库
        currentRow = self.apiTableView.currentIndex().row()
        if currentRow > 0:
            conn.cursor().execute("update %s set id=10000 where id=%s-1 " % (apiTableName, currentRow + 1))
            conn.cursor().execute("update %s set id = id - 1 where id = %s" % (apiTableName, currentRow + 1))
            conn.cursor().execute("update %s set id=%s where id=10000 " % (apiTableName, currentRow + 1))
            conn.commit()
            self.model.select()
            self.apiTableView.selectRow(currentRow - 1)
        # 不在这里关数据库了()
        self.sendApiUpdatedBroadCast()

    def downApiButtonClicked(self):
        ########改用主数据库
        currentRow = self.apiTableView.currentIndex().row()
        rowCount = self.model.rowCount()
        # print(currentRow)
        if currentRow > -1 and currentRow < rowCount - 1:
            # print(True)
            conn.cursor().execute("update %s set id=10000 where id=%s+1 " % (apiTableName, currentRow + 1))
            conn.cursor().execute("update %s set id = id + 1 where id = %s" % (apiTableName, currentRow + 1))
            conn.cursor().execute("update %s set id=%s where id=10000 " % (apiTableName, currentRow + 1))
            conn.commit()
            self.model.select()
            self.apiTableView.selectRow(currentRow + 1)
        # 不在这里关数据库了()
        self.sendApiUpdatedBroadCast()

    class AddApiDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.initUI()

        def initUI(self):
            self.setWindowTitle(self.tr('添加或更新 Api'))
            ########改用主数据库

            # 各个输入框
            if True:
                if True:
                    self.引擎名称标签 = QLabel(self.tr('引擎名字：'))
                    self.引擎名称编辑框 = QLineEdit()
                    self.引擎名称编辑框.setPlaceholderText(self.tr('例如：阿里-中文'))

                if True:
                    self.服务商标签 = QLabel(self.tr('服务商：'))
                    self.服务商选择框 = QComboBox()
                    self.服务商选择框.addItems(['Alibaba', 'Tencent'])
                    self.服务商选择框.setCurrentText('Alibaba')

                if True:
                    self.appKey标签 = QLabel('AppKey：')
                    self.appKey输入框 = QLineEdit()

                if True:
                    self.语言标签 = QLabel(self.tr('语言：'))
                    self.语言Combobox = QComboBox()

                if True:
                    self.accessKeyId标签 = QLabel('AccessKeyId：')
                    self.accessKeyId输入框 = QLineEdit()
                    self.accessKeyId输入框.setEchoMode(QLineEdit.Password)

                if True:
                    self.AccessKeySecret标签 = QLabel('AccessKeySecret：')
                    self.AccessKeySecret输入框 = QLineEdit()
                    self.AccessKeySecret输入框.setEchoMode(QLineEdit.Password)

                currentRow = mainWindow.ConfigTab.apiTableView.currentIndex().row()
                if currentRow > -1:
                    currentApiItem = conn.cursor().execute(
                        '''select name, provider, appKey, language, accessKeyId, accessKeySecret from %s where id = %s''' % (
                        apiTableName, currentRow + 1)).fetchone()
                    if currentApiItem != None:
                        self.引擎名称编辑框.setText(currentApiItem[0])
                        self.服务商选择框.setCurrentText(currentApiItem[1])
                        self.appKey输入框.setText(currentApiItem[2])
                        self.语言Combobox.setCurrentText(currentApiItem[3])
                        self.accessKeyId输入框.setText(currentApiItem[4])
                        self.AccessKeySecret输入框.setText(currentApiItem[5])
                        pass
                self.服务商选择框.currentTextChanged.connect(self.configLanguageCombobox)
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
                self.表格布局控件.setLayout(self.表格布局)
                self.表格布局.addRow(self.引擎名称标签, self.引擎名称编辑框)
                self.表格布局.addRow(self.服务商标签, self.服务商选择框)
                self.表格布局.addRow(self.appKey标签, self.appKey输入框)
                self.表格布局.addRow(self.语言标签, self.语言Combobox)
                self.表格布局.addRow(self.accessKeyId标签, self.accessKeyId输入框)
                self.表格布局.addRow(self.AccessKeySecret标签, self.AccessKeySecret输入框)

                self.按钮布局控件 = QWidget()
                self.按钮布局 = QHBoxLayout()

                self.按钮布局.addWidget(self.submitButton)
                self.按钮布局.addWidget(self.cancelButton)
                self.按钮布局控件.setLayout(self.按钮布局)

                self.主布局vbox = QVBoxLayout()
                self.主布局vbox.addWidget(self.表格布局控件)
                self.主布局vbox.addWidget(self.按钮布局控件)

            self.setLayout(self.主布局vbox)

            # 根据是否有名字决定是否将确定按钮取消可用
            self.引擎名称编辑框.textChanged.connect(self.engineNameChanged)
            self.configLanguageCombobox()
            self.engineNameChanged()

            self.exec()

        def configLanguageCombobox(self):
            if self.服务商选择框.currentText() == 'Alibaba':
                self.语言Combobox.clear()
                self.语言Combobox.addItem(self.tr('由 Api 的云端配置决定'))
                self.语言Combobox.setCurrentText(self.tr('由 Api 的云端配置决定'))
                self.语言Combobox.setEnabled(False)
                self.appKey输入框.setEnabled(True)
                self.accessKeyId标签.setText('AccessKeyId：')
                self.AccessKeySecret标签.setText('AccessKeySecret：')
            elif self.服务商选择框.currentText() == 'Tencent':
                self.语言Combobox.clear()
                self.语言Combobox.addItems(['中文普通话', '英语', '粤语'])
                self.语言Combobox.setCurrentText('中文普通话')
                self.语言Combobox.setEnabled(True)
                self.appKey输入框.setEnabled(False)
                self.accessKeyId标签.setText('AccessSecretId：')
                self.AccessKeySecret标签.setText('AccessSecretKey：')

        # 根据引擎名称是否为空，设置确定键可否使用
        def engineNameChanged(self):
            self.引擎名称 = self.引擎名称编辑框.text()
            if self.引擎名称 == '':
                if self.submitButton.isEnabled():
                    self.submitButton.setEnabled(False)
            else:
                if not self.submitButton.isEnabled():
                    self.submitButton.setEnabled(True)

        # 点击提交按钮后, 添加预设
        def submitButtonClicked(self):
            self.引擎名称 = self.引擎名称编辑框.text()
            self.引擎名称 = self.引擎名称.replace("'", "''")

            self.服务商 = self.服务商选择框.currentText()
            self.服务商 = self.服务商.replace("'", "''")

            self.appKey = self.appKey输入框.text()
            self.appKey = self.appKey.replace("'", "''")

            self.language = self.语言Combobox.currentText()
            self.language = self.language.replace("'", "''")

            self.accessKeyId = self.accessKeyId输入框.text()
            self.accessKeyId = self.accessKeyId.replace("'", "''")

            self.AccessKeySecret = self.AccessKeySecret输入框.text()
            self.AccessKeySecret = self.AccessKeySecret.replace("'", "''")



            # currentApiItem = conn.cursor().execute(
            #     '''select name, provider, appKey, accessKeyId, accessKeySecret from %s where id = %s''' % (
            #     apiTableName, currentRow + 1)).fetchone()
            # if currentApiItem != None:

            result = conn.cursor().execute(
                '''select name, provider, appKey, language, accessKeyId, accessKeySecret from %s where name = '%s' ''' % (
                apiTableName, self.引擎名称.replace("'", "''"))).fetchone()
            if result == None:
                try:
                    maxIdRow = conn.cursor().execute(
                        '''select id from %s order by id desc;''' % apiTableName).fetchone()
                    if maxIdRow != None:
                        maxId = maxIdRow[0]
                        conn.cursor().execute(
                            '''insert into %s (id, name, provider, appKey, language, accessKeyId, accessKeySecret) values (%s, '%s', '%s', '%s', '%s', '%s', '%s');''' % (
                                apiTableName, maxId + 1, self.引擎名称.replace("'", "''"), self.服务商.replace("'", "''"),
                                self.appKey.replace("'", "''"), self.language.replace("'", "''"),
                                self.accessKeyId.replace("'", "''"), self.AccessKeySecret.replace("'", "''")))
                    else:
                        maxId = 0
                        # print(
                        #     '''insert into %s (id, name, provider, appKey, language, accessKeyId, accessKeySecret) values (%s, '%s', '%s', '%s', '%s', '%s', '%s');''' % (
                        #         apiTableName, maxId + 1, self.引擎名称.replace("'", "''"), self.服务商.replace("'", "''"),
                        #         self.appKey.replace("'", "''"), self.language.replace("'", "''"), self.accessKeyId.replace("'", "''"),
                        #         self.AccessKeySecret.replace("'", "''")))
                        conn.cursor().execute(
                            '''insert into %s (id, name, provider, appKey, language, accessKeyId, accessKeySecret) values (%s, '%s', '%s', '%s', '%s', '%s', '%s');''' % (
                                apiTableName, maxId + 1, self.引擎名称.replace("'", "''"), self.服务商.replace("'", "''"),
                                self.appKey.replace("'", "''"), self.language.replace("'", "''"),
                                self.accessKeyId.replace("'", "''"),
                                self.AccessKeySecret.replace("'", "''")))
                    conn.commit()
                    self.close()
                except:
                    QMessageBox.warning(self, self.tr('添加Api'), self.tr('新Api添加失败，你可以把失败过程重新操作记录一遍，然后发给作者'))
            else:
                answer = QMessageBox.question(self, self.tr('覆盖Api'), self.tr('''已经存在名字相同的Api，你可以选择换一个Api名称或者覆盖旧的Api。是否要覆盖？'''))
                if answer == QMessageBox.Yes:  # 如果同意覆盖
                    try:
                        conn.cursor().execute(
                            '''update %s set name = '%s', provider = '%s', appKey = '%s', language = '%s', accessKeyId = '%s', accessKeySecret = '%s' where name = '%s';''' % (
                                apiTableName, self.引擎名称.replace("'", "''"), self.服务商.replace("'", "''"),
                                self.appKey.replace("'", "''"), self.language.replace("'", "''"),
                                self.accessKeyId.replace("'", "''"), self.AccessKeySecret.replace("'", "''"),
                                self.引擎名称.replace("'", "''")))
                        conn.commit()
                        QMessageBox.information(self, self.tr('更新Api'), self.tr('Api更新成功'))
                        self.close()
                    except:
                        QMessageBox.warning(self, self.tr('更新Api'), self.tr('Api更新失败，你可以把失败过程重新操作记录一遍，然后发给作者'))
            mainWindow.ConfigTab.model.select()

            self.sendApiUpdatedBroadCast()

        def closeEvent(self, a0: QCloseEvent) -> None:
            try:
                pass
                # 不在这里关数据库了()
                # mainWindow.ffmpegMainTab.refreshList()
            except:
                pass

        def sendApiUpdatedBroadCast(self):
            apiUpdateBroadCaster.broadCastUpdates()
