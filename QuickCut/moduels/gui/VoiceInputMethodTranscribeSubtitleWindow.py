# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from moduels.tool.FFmpegWavGenThread import FFmpegWavGenThread
from moduels.component.OutputBox import OutputBox
from moduels.component.OutputLineBox import OutputLineBox
import os, srt, time


class VoiceInputMethodTranscribeSubtitleWindow(QMainWindow):
    # 这是个子窗口，调用的时候要指定父窗口。例如：window = Console(mainWindow)
    # 里面包含一个 OutputBox, 可以将信号导到它的 print 方法。
    thread = None
    mode = 0  # 零代表半自动模式
    inputFiePath = None  # 输入路径
    timestampFile = None # 时间戳辅助文件
    outputFilePath = None  # 输出路径
    shortcutOfInputMethod = None  # 输入法的快捷键
    startTime = None  # 确定起始时间
    ffmpegWavGenThread = None
    continueToTrans = True # 默认在全自动模式下一句完成时继续下一轮
    transEngine = None

    def __init__(self, parent=None):
        super(VoiceInputMethodTranscribeSubtitleWindow, self).__init__(parent)
        self.ffmpegWavGenThread = FFmpegWavGenThread()
        self.initGui()

    def initGui(self):
        self.setWindowTitle(self.tr('语音输入法转写字幕工作窗口'))
        self.resize(1300, 700)
        self.hintConsoleBox = OutputBox() # 他就用于输出提示用户的信息
        self.finalResultBox = OutputBox()  # 输出总结果
        self.finalResultBox.setReadOnly(False)
        self.transInputBox = OutputLineBox()  # 临时听写框

        self.buttonLayout = QHBoxLayout()
        self.pauseButton = QPushButton(self.tr('暂停'))
        self.pauseButton.setEnabled(False)
        self.continueButton = QPushButton(self.tr('继续'))
        self.continueButton.setEnabled(False)
        self.pauseButton.clicked.connect(self.pauseThread)
        self.continueButton.clicked.connect(self.startThread)
        self.buttonLayout.addWidget(self.pauseButton)
        self.buttonLayout.addWidget(self.continueButton)



        # 设置父控件
        self.hintConsoleBox.setParent(self)
        self.finalResultBox.setParent(self)
        self.transInputBox.setParent(self)

        # 设置窗口布局
        self.masterWidget = QWidget()
        self.setCentralWidget(self.masterWidget)
        self.masterLayout = QVBoxLayout()
        self.masterLayout.setSpacing(30)
        self.masterWidget.setLayout(self.masterLayout)

        # 添加部件
        self.masterLayout.addWidget(self.hintConsoleBox, 2)
        self.masterLayout.addWidget(self.finalResultBox, 4)
        self.masterLayout.addWidget(self.transInputBox, 1)
        self.masterLayout.addLayout(self.buttonLayout, 1)

        self.show()

        self.hintConsoleBox.print(self.tr('正在生成 wav 文件\n'))

    def initParams(self):
        self.srtIndex = 0  # 初始化第一条字幕的序号
        if os.path.exists(self.outputFilePath):
            self.srtFile = open(os.path.splitext(self.outputFilePath)[0] + '.srt', 'r', encoding='utf-8')
            with self.srtFile:
                content = self.srtFile.read()
                if content != '':
                    self.finalResultBox.setText(content + '\n')  # 先读取已经存在的 srt
                    subtitleLists = list(srt.parse(content))  # 从已存在的文件中读取字幕
                    self.srtIndex += len(subtitleLists)  # 如果已经有，那就将字幕向前移
                    self.hintConsoleBox.print(self.tr('检测到已存在同名字幕文件，已有 %s 条字幕，将会自动载入到下面的编辑框\n') % self.srtIndex)
                    self.hintConsoleBox.print(self.tr('如果不希望接着已有内容做字幕，请手动删除已存在的字幕文件\n'))

            self.srtFile = open(os.path.splitext(self.outputFilePath)[0] + '.srt', 'w', encoding='utf-8')
        else:
            self.srtFile = open(os.path.splitext(self.outputFilePath)[0] + '.srt', 'w', encoding='utf-8')
        self.ffmpegWavGenThread.signal.connect(self.getFFmpegFinishSignal) #
        self.ffmpegWavGenThread.start()
        self.thread.offsetTime = self.startTime
        self.thread.srtIndex = self.srtIndex
        self.thread.resultTextBox = self.transInputBox  # 把语音识别结果的输入框给线程
        self.thread.shortcutKey = self.shortcutOfInputMethod  # 把快捷键
        self.thread.signal.connect(self.printSignalReceived)
        self.thread.signalOfSubtitle.connect(self.signalOfSubtitleReceived)

    def startThread(self):
        self.continueToTrans = True
        if self.mode == 1:
            self.pauseButton.setEnabled(True)
        self.thread.start()
        self.finalResultBox.setReadOnly(True)
        self.continueButton.setEnabled(False)

    def pauseThread(self):
        self.continueToTrans = False
        self.pauseButton.setEnabled(False)
        self.transInputBox.setFocus()

    def printSignalReceived(self, text):
        print(text)

    def signalOfSubtitleReceived(self, srtObject):
        self.finalResultBox.setReadOnly(False)
        subtitle = srt.compose([srtObject], start_index=srtObject.index + 1)
        self.finalResultBox.print(subtitle)
        self.hintConsoleBox.print(self.tr('第 %s 句识别完毕！\n') % self.thread.srtIndex)
        if srtObject.content == '':
            self.hintConsoleBox.print(self.tr('片段识别结果是空白，有可能音频设置有误，请查看视频教程：https://www.bilibili.com/video/BV1wT4y177kD/\n'))
        if self.mode == 0:  # 只有在半自动模式，才在收到结果时恢复继续按键
            self.continueButton.setEnabled(True)
        else:
            if self.continueToTrans == False: # 当在全自动模式，暂停后，收到了结果，让继续键变可用
                self.continueButton.setEnabled(True)
            if self.continueToTrans == True:
                self.startThread()

    def getFFmpegFinishSignal(self, wavFile): # 得到 wav 文件，
        self.regionsList = self.transEngine.getRegions(wavFile) # 得到片段
        if self.regionsList == False:
            self.hintConsoleBox.print('无法从输入文件转出 wav 文件，请先用“pip show auditok”检查下 auditok 的版本，如果低于 0.2，请使用 “pip install git+https://gitee.com/haujet/auditok” 或 “pip install git+https://github.com/amsehili/auditok” 安装最新版本的 auditok，如果 auditok 版本没有问题，那就可能是输入文件不是标准音视频文件。 ')
            return
        self.wavFile = wavFile
        self.regionsListLength = len(self.regionsList)
        self.thread.transEngine = self.transEngine
        self.thread.regionsList = self.regionsList
        self.thread.regionsListLength = self.regionsListLength
        print(self.regionsListLength)
        self.hintConsoleBox.print(self.tr('已得到 wav 文件，并分段，共有 %s 段\n') % self.regionsListLength)
        self.hintConsoleBox.print(self.tr('该功能需要设置电脑一番，所以请确保已看过视频教程：\n'))
        self.hintConsoleBox.print(self.tr('关闭本页面后，下方输入框的内容会自动保存到 %s 中\n') % self.outputFilePath)
        if self.mode == 0: #只有在半自动模式，才在收到结果时恢复继续按键
            self.hintConsoleBox.print(self.tr('现在按下 继续 键开始听写音频\n'))
            self.continueButton.setEnabled(True)
        if self.mode == 1: # 如果是自动模式，那就即刻发车！
            time.sleep(1)
            self.startThread()


    def closeEvent(self, a0: QCloseEvent) -> None:
        try: # 尝试将字幕格式化后写入输出文件。
            originalSubtitle = self.finalResultBox.toPlainText()
            processedSubtitle = srt.compose(list(srt.parse(originalSubtitle)), reindex=True, start_index=1, strict=True)
            with self.srtFile:
                self.srtFile.write(processedSubtitle)
        except:
            print('格式化字幕输入文本失败')
        try:
            os.remove(self.wavFile)
        except:
            print('删除 wav 文件失败')
        try:
            keyboard.release(self.shortcutOfInputMethod) # 这里是防止在关闭页面时，语音输入快捷键还按着
        except:
            pass
        try:
            self.thread.exit()
        except:
            pass
        try:
            self.thread.setTerminationEnabled(True)
            self.thread.terminate()
        except:
            pass
