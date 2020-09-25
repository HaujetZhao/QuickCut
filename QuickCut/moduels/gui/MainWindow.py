# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *

# try:
from moduels.gui.FFmpegMainTab import FFmpegMainTab
from moduels.gui.FFmpegSplitVideoTab import FFmpegSplitVideoTab
from moduels.gui.FFmpegConcatTab import FFmpegConcatTab
from moduels.gui.DownLoadVideoTab import DownLoadVideoTab
from moduels.gui.ConfigTab import ConfigTab
from moduels.gui.FFmpegAutoEditTab import FFmpegAutoEditTab
from moduels.gui.FFmpegAutoSrtTab import FFmpegAutoSrtTab
from moduels.gui.CapsWriterTab import CapsWriterTab
from moduels.gui.HelpTab import HelpTab
from moduels.component.UpdateChecker import UpdateChecker
# except:
#     from QuickCut.

from moduels.component.NormalValue import 常量

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        常量.mainWindow = self
        self._update_checker = None
        self.initGui()
        self.loadStyleSheet()
        self.status = self.statusBar()
        self._start_checker()


        # self.setWindowState(Qt.WindowMaximized)
        # sys.stdout = Stream(newText=self.onUpdateText)

    def initGui(self):
        # 定义中心控件为多 tab 页面
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # 定义多个不同功能的 tab
        self.ffmpegMainTab = FFmpegMainTab()  # 主要功能的 tab
        self.ffmpegSplitVideoTab = FFmpegSplitVideoTab()  # 分割视频 tab
        # self.ffmpegCutVideoTab = FFmpegCutVideoTab()  # 剪切视频的 tab
        self.ffmpegConcatTab = FFmpegConcatTab()  # 合并视频的 tab
        # self.ffmpegBurnCaptionTab = FFmpegBurnCaptionTab()  # 烧字幕的 tab
        self.downloadVidwoTab = DownLoadVideoTab()  # 下载视频的 tab
        self.ConfigTab = ConfigTab()  # 配置 Api 的 tab 这个要放在前面儿初始化, 因为他要创建数据库
        self.ffmpegAutoEditTab = FFmpegAutoEditTab()  # 自动剪辑的 tab
        self.ffmpegAutoSrtTab = FFmpegAutoSrtTab()  # 自动转字幕的 tab
        self.capsWriterTab = CapsWriterTab()

         # 创建一个可以发送信号的对象，用于告知其他界面 api列表已经更新


        # self.consoleTab = ConsoleTab() # 新的控制台输出 tab
        self.helpTab = HelpTab()  # 帮助
        # self.aboutTab = AboutTab()  # 关于

        # 将不同功能的 tab 添加到主 tabWidget
        self.tabs.addTab(self.ffmpegMainTab, self.tr('FFmpeg'))

        self.tabs.addTab(self.ffmpegSplitVideoTab, self.tr('分割视频'))
        # self.tabs.addTab(self.ffmpegCutVideoTab, '截取片段')
        self.tabs.addTab(self.ffmpegConcatTab, self.tr('合并片段'))
        # self.downloadTabScroll = QScrollArea()
        # self.downloadTabScroll.setWidget(self.downloadVidwoTab)
        # self.downloadVidwoTab.setObjectName('widget')
        # self.downloadVidwoTab.setStyleSheet("QWidget#widget{background-color:transparent;}")
        # self.downloadTabScroll.setStyleSheet("QScrollArea{background-color:transparent;}")
        # self.tabs.addTab(self.downloadTabScroll, '下载视频')
        self.tabs.addTab(self.downloadVidwoTab, self.tr('下载视频'))
        # self.tabs.addTab(self.ffmpegBurnCaptionTab, '嵌入字幕')
        self.tabs.addTab(self.ffmpegAutoEditTab, self.tr('自动剪辑'))
        self.tabs.addTab(self.ffmpegAutoSrtTab, self.tr('自动字幕'))
        self.tabs.addTab(self.capsWriterTab, self.tr('语音输入'))
        self.tabs.addTab(self.ConfigTab, self.tr('设置'))
        # self.tabs.addTab(self.consoleTab, '控制台')
        self.tabs.addTab(self.helpTab, self.tr('帮助'))
        # self.tabs.addTab(self.aboutTab, '关于')

        self.adjustSize()
        if 常量.platfm == 'Darwin':
            self.setWindowIcon(QIcon('misc/icon.icns'))
        else:
            self.setWindowIcon(QIcon('misc/icon.ico'))
        self.setWindowTitle('Quick Cut')

        # self.setWindowFlag(Qt.WindowStaysOnTopHint) # 始终在前台

        self.show()

    def loadStyleSheet(self):
        try:
            try:
                with open(常量.styleFile, 'r', encoding='utf-8') as style:
                    self.setStyleSheet(style.read())
            except:
                with open(常量.styleFile, 'r', encoding='gbk') as style:
                    self.setStyleSheet(style.read())
        except:
            QMessageBox.warning(self, self.tr('主题载入错误'), self.tr('未能成功载入主题，请确保软件根目录有 "style.css" 文件存在。'))

    def keyPressEvent(self, event) -> None:
        # 在按下 F5 的时候重载 style.css 主题
        if (event.key() == Qt.Key_F5):
            self.loadStyleSheet()
            self.status.showMessage('已成功更新主题', 800)

    def onUpdateText(self, text):
        """Write console output to text widget."""

        cursor = self.consoleTab.consoleEditBox.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.consoleTab.consoleEditBox.setTextCursor(cursor)
        self.consoleTab.consoleEditBox.ensureCursorVisible()

    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        if 常量.mainWindow.ConfigTab.hideToSystemTraySwitch.isChecked():
            event.ignore()
            self.hide()
        else:
            sys.stdout = sys.__stdout__
            super().closeEvent(event)

    def _start_checker(self):
        self._update_checker = UpdateChecker()
        self._update_checker.check_for_update()
        self._update_checker.update_dialog.setParent(self)
        # Setting the dialog's parent resets its flags
        # See https://forum.qt.io/topic/10477
        self._update_checker.update_dialog.setWindowFlags(
            Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.Dialog)