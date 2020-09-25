# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from moduels.component.OutputBox import OutputBox
from moduels.component.NormalValue import 常量
from moduels.tool.CapsWriterThread import CapsWriterThread


class CapsWriterTab(QWidget):
    def __init__(self):
        super().__init__()
        self.createDB()
        self.capsWriterThread = None
        self.initGui()


    def initGui(self):
        self.masterLayout = QVBoxLayout()
        self.widgetLayout = QGridLayout()
        self.setLayout(self.masterLayout)
        self.subtitleEngineLabel = QLabel(self.tr('字幕语音 API：'))
        self.subtitleEngineComboBox = QComboBox()
        apis = 常量.conn.cursor().execute('select name from %s where provider = "Alibaba"' % 常量.apiTableName).fetchall()
        if apis != None:
            for api in apis:
                self.subtitleEngineComboBox.addItem(api[0])
            self.subtitleEngineComboBox.setCurrentIndex(0)
            pass
        # 不在这里关数据库了

        常量.apiUpdateBroadCaster.signal.connect(self.updateEngineList)
        self.engineLayout = QFormLayout()
        self.masterLayout.addLayout(self.engineLayout)
        self.engineLayout.addRow(self.subtitleEngineLabel, self.subtitleEngineComboBox)
        # self.engineLayout.addWidget(self.subtitleEngineLabel)
        # self.engineLayout.addWidget(self.subtitleEngineComboBox)

        self.disableButton = QRadioButton(self.tr('停用 CapsWirter 语音输入'))
        self.enableButton = QRadioButton(self.tr('启用 CapsWirter 语音输入'))
        self.buttonLayout = QHBoxLayout()
        self.masterLayout.addSpacing(30)
        self.masterLayout.addLayout(self.buttonLayout)
        self.buttonLayout.addWidget(self.disableButton)
        self.buttonLayout.addWidget(self.enableButton)


        if self.subtitleEngineComboBox.currentText() == '':
            self.enableButton.setEnabled(False)
        self.subtitleEngineComboBox.currentTextChanged.connect(self.switchEnableButtonStatus)

        ########改用主数据库

        # 不在这里关数据库了


        self.introBox = QTextEdit()
        font = QFont()
        font.setPointSize(12)
        self.introBox.setFont(font)
        # self.introBox.setMaximumHeight(200)
        self.introBox.setPlainText(self.tr("选择阿里云 api 的引擎，启用 CapsWriter 语音输入后，只要在任意界面长按大写大写锁定键（Caps Lk）超过 0.3 秒，就会开始进行语音识别，说几句话，再松开大写锁定键，请别结果就会自动输入。你可以在这个输入框试试效果"))
        self.masterLayout.addSpacing(30)
        self.masterLayout.addWidget(self.introBox)

        self.outputBox = OutputBox()
        self.masterLayout.addSpacing(30)
        self.masterLayout.addWidget(self.outputBox)

        self.masterLayout.addStretch(0)

        self.enableButton.clicked.connect(self.capsWriterEnabled)
        self.disableButton.clicked.connect(self.capsWriterDisabled)

    def initCapsWriterStatus(self):
        cursor = 常量.conn.cursor()
        result = cursor.execute('select value from %s where item = "%s";' % (常量.preferenceTableName, 'CapsWriterEnabled'))
        if result.fetchone()[0] == 'False':
            self.disableButton.click()
        else:
            self.enableButton.click()

    def switchEnableButtonStatus(self):
        if self.subtitleEngineComboBox.currentText() == '':
            self.enableButton.setEnabled(False)
        else:
            self.enableButton.setEnabled(True)

    def createDB(self):
        ########改用主数据库
        cursor = 常量.conn.cursor()
        result = cursor.execute('select * from %s where item = "%s";' % (常量.preferenceTableName, 'CapsWriterEnabled'))
        if result.fetchone() == None:
            cursor.execute('''insert into %s (item, value) values ('%s', '%s');''' % (
                常量.preferenceTableName, 'CapsWriterEnabled', 'False'))
        else:
            print('CapsWriterEnabled 条目已存在')

        result = cursor.execute('select * from %s where item = "%s";' % (常量.preferenceTableName, 'CapsWriterTokenId'))
        if result.fetchone() == None:
            cursor.execute('''insert into %s (item, value) values ('%s', '%s');''' % (
                常量.preferenceTableName, 'CapsWriterTokenId', 'xxxxxxx'))
        else:
            print('CapsWriterEnabled Token ID 条目已存在')
            pass

        result = cursor.execute('select * from %s where item = "%s";' % (常量.preferenceTableName, 'CapsWriterTokenExpireTime'))
        if result.fetchone() == None:
            cursor.execute('''insert into %s (item, value) values ('%s', '%s');''' % (
                常量.preferenceTableName, 'CapsWriterTokenExpireTime', '0000000000'))
        else:
            print('CapsWriterEnabled Token ExpireTime 条目已存在')
            pass

        常量.conn.commit()
        # 不在这里关数据库了()

    def capsWriterEnabled(self):
        ########改用主数据库
        cursor = 常量.conn.cursor()
        result = cursor.execute('''update %s set value = 'True'  where item = '%s';''' % (常量.preferenceTableName, 'CapsWriterEnabled'))
        常量.conn.commit()
        api = cursor.execute('''select appkey, accessKeyId, accessKeySecret from %s where name = "%s"''' % (常量.apiTableName, self.subtitleEngineComboBox.currentText())).fetchone()
        # 不在这里关数据库了()
        self.capsWriterThread = CapsWriterThread()
        self.capsWriterThread.appKey = api[0]
        self.capsWriterThread.accessKeyId = api[1]
        self.capsWriterThread.accessKeySecret = api[2]
        self.capsWriterThread.outputBox = self.outputBox
        self.capsWriterThread.start()

    def capsWriterDisabled(self):
        try:
            self.capsWriterThread.clean()
            self.capsWriterThread.exit()
        except:
            print('语音输入进程退出失败')
        try:
            self.capsWriterThread.setTerminationEnabled(True)
            self.capsWriterThread.terminate()
        except:
            print('语音输入进程结束失败')
        cursor = 常量.conn.cursor()
        result = cursor.execute('''update  %s set value = 'False'  where item = '%s';''' % (常量.preferenceTableName, 'CapsWriterEnabled'))
        常量.conn.commit()


    def updateEngineList(self):
        apis = 常量.conn.cursor().execute('select name from %s where provider = "Alibaba"' % 常量.apiTableName).fetchall()
        self.subtitleEngineComboBox.clear()
        if apis != None:
            for api in apis:
                self.subtitleEngineComboBox.addItem(api[0])
            self.subtitleEngineComboBox.setCurrentIndex(0)
            pass
        # 不在这里关数据库了
