# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *

from moduels.gui.FFmpegMainTab import FFmpegMainTab
from moduels.gui.FFmpegSplitVideoTab import FFmpegSplitVideoTab
from moduels.gui.FFmpegConcatTab import FFmpegConcatTab
from moduels.gui.DownLoadVideoTab import DownLoadVideoTab
from moduels.gui.ConfigTab import ConfigTab
from moduels.gui.FFmpegAutoEditTab import FFmpegAutoEditTab
from moduels.gui.FFmpegAutoSrtTab import FFmpegAutoSrtTab
# from moduels.gui.CapsWriterTab import CapsWriterTab
from moduels.gui.HelpTab import HelpTab
from moduels.component.UpdateChecker import UpdateChecker
from moduels.function.readText import 读取文本
from moduels.function.checkExecutable import 查找可执行程序

from moduels.component.NormalValue import 常量

import sys, os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        常量.mainWindow = self
        self._update_checker = None
        self.initGui()
        self.载入样式表()
        self.状态栏 = self.statusBar()
        self.检查可执行文件()

        # 更新检查器，暂且停用
        # self._start_checker()

        # self.setWindowState(Qt.WindowMaximized)
        # sys.stdout = Stream(newText=self.onUpdateText)

    def initGui(self):
        # 定义中心控件为多 tab 页面
        self.tab总控件 = QTabWidget()
        self.setCentralWidget(self.tab总控件)

        # 定义多个不同功能的 tab
        self.ffmpeg主功能Tab = FFmpegMainTab()  # 主要功能的 tab
        self.ffmpeg分割视频Tab = FFmpegSplitVideoTab()  # 分割视频 tab
        self.ffmpeg连接视频Tab = FFmpegConcatTab()  # 合并视频的 tab
        self.下载视频Tab = DownLoadVideoTab()  # 下载视频的 tab
        self.设置页Tab = ConfigTab()  # 配置 Api 的 tab 这个要放在前面儿初始化, 因为他要创建数据库
        self.自动剪辑Tab = FFmpegAutoEditTab()  # 自动剪辑的 tab
        self.音频转字幕Tab = FFmpegAutoSrtTab()  # 自动转字幕的 tab
        self.帮助Tab = HelpTab()  # 帮助

        # 将不同功能的 tab 添加到主 tabWidget
        self.tab总控件.addTab(self.ffmpeg主功能Tab, self.tr('FFmpeg'))
        self.tab总控件.addTab(self.ffmpeg分割视频Tab, self.tr('分割'))
        self.tab总控件.addTab(self.ffmpeg连接视频Tab, self.tr('合并'))
        self.tab总控件.addTab(self.下载视频Tab, self.tr('下载'))
        self.tab总控件.addTab(self.自动剪辑Tab, self.tr('自动剪辑'))
        self.tab总控件.addTab(self.音频转字幕Tab, self.tr('字幕'))
        self.tab总控件.addTab(self.设置页Tab, self.tr('设置'))
        self.tab总控件.addTab(self.帮助Tab, self.tr('帮助'))

        # 想做个将 ass 字幕文件烧入画面中的功能来着，精力所限，先不做了
        # self.tabs.addTab(self.ffmpegBurnCaptionTab, '嵌入字幕')

        # 窗口大小、图标、标题
        self.adjustSize()
        self.setWindowIcon(QIcon(常量.图标路径))
        self.setWindowTitle('Quick Cut')

        # 解除下行注释，可以使窗口始终在前台
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.show()

    def 载入样式表(self):
        try:
            self.setStyleSheet(读取文本(常量.样式文件))
        except:
            QMessageBox.warning(self, self.tr('主题载入错误'),
                                self.tr('未能成功载入主题，请确保软件根目录有 "style.css" 文件存在。'))

    def 检查可执行文件(self):

        if not 查找可执行程序('ffmpeg') or not 查找可执行程序('ffprobe'):
            QMessageBox.information(self, '缺少依赖程序', f'''很报歉，在环境变量中找不到「FFmpeg」和「FFprobe」这两个依赖程序。

其中，FFmpeg 用于处理音视频文件，FFprobe 用于读取音视频的详细信息。

解决方法：

先到官网 https://ffmpeg.org/download.html 下载最新的 FFmpeg，解压后可以得到 FFmpeg 和 FFprobe，然后，

1. 如果你不懂什么是「环境变量」，那就将 FFmpeg 和 FFprobe 复制到 QuickCut 程序所在目录
2. 如果你懂什么是「环境变量」，那就将 FFmpeg 和 FFprobe 所在目录添加到系统环境变量 
   （也可以百度一下「Windows如何添加环境变量」）
''')

    def keyPressEvent(self, event) -> None:
        # 在按下 F5 的时候重载 style.css 主题
        if (event.key() == Qt.Key_F5):
            self.载入样式表()
            self.状态栏.showMessage('已成功更新主题', 800)

    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        if 常量.mainWindow.设置页Tab.隐藏到托盘栏开关.isChecked():
            event.ignore()
            self.hide()
        else:
            sys.stdout = sys.__stdout__
            super().closeEvent(event)

# -----------------------------------------------------------------------------------------

    # def onUpdateText(self, text):
    #     """Write console output to text widget."""
    #     cursor = self.consoleTab.consoleEditBox.textCursor()
    #     cursor.movePosition(QTextCursor.End)
    #     cursor.insertText(text)
    #     self.consoleTab.consoleEditBox.setTextCursor(cursor)
    #     self.consoleTab.consoleEditBox.ensureCursorVisible()

    # 更新检查器，暂且停用
    # def _start_checker(self):
    #     self._update_checker = UpdateChecker()
    #     self._update_checker.check_for_update()
    #     self._update_checker.update_dialog.setParent(self)
    #     # Setting the dialog's parent resets its flags
    #     # See https://forum.qt.io/topic/10477
    #     self._update_checker.update_dialog.setWindowFlags(
    #         Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.Dialog)