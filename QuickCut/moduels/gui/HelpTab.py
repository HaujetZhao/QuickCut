
class HelpTab(QWidget):
    def __init__(self):
        super().__init__()
        self.openHelpFileButton = QPushButton(self.tr('打开帮助文档'))
        self.ffmpegMannualNoteButton = QPushButton(self.tr('查看作者的 FFmpeg 笔记'))
        self.openVideoHelpButtone = QPushButton(self.tr('查看视频教程'))
        self.openGiteePage = QPushButton(self.tr('当前版本是 %s，到 Gitee 检查新版本') % version)
        self.openGithubPage = QPushButton(self.tr('当前版本是 %s，到 Github 检查新版本') % version)
        self.linkToDiscussPage = QPushButton(self.tr('加入 QQ 群'))
        self.tipButton = QPushButton(self.tr('打赏作者'))

        self.openHelpFileButton.setMaximumHeight(100)
        self.ffmpegMannualNoteButton.setMaximumHeight(100)
        self.openVideoHelpButtone.setMaximumHeight(100)
        self.openGiteePage.setMaximumHeight(100)
        self.openGithubPage.setMaximumHeight(100)
        self.linkToDiscussPage.setMaximumHeight(100)
        self.tipButton.setMaximumHeight(100)

        self.openHelpFileButton.clicked.connect(self.openHelpDocument)
        self.ffmpegMannualNoteButton.clicked.connect(lambda: webbrowser.open(self.tr(r'https://hacpai.com/article/1595480295489')))
        self.openVideoHelpButtone.clicked.connect(lambda: webbrowser.open(self.tr(r'https://www.bilibili.com/video/BV18T4y1E7FF/')))
        self.openGiteePage.clicked.connect(lambda: webbrowser.open(self.tr(r'https://gitee.com/haujet/QuickCut/releases')))
        self.openGithubPage.clicked.connect(lambda: webbrowser.open(self.tr(r'https://github.com/HaujetZhao/QuickCut/releases')))
        self.linkToDiscussPage.clicked.connect(lambda: webbrowser.open(
            self.tr(r'https://qm.qq.com/cgi-bin/qm/qr?k=DgiFh5cclAElnELH4mOxqWUBxReyEVpm&jump_from=webapi')))
        self.tipButton.clicked.connect(lambda: SponsorDialog())

        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)
        self.masterLayout.addWidget(self.openHelpFileButton)
        self.masterLayout.addWidget(self.ffmpegMannualNoteButton)
        self.masterLayout.addWidget(self.openVideoHelpButtone)
        self.masterLayout.addWidget(self.openGiteePage)
        self.masterLayout.addWidget(self.openGithubPage)
        self.masterLayout.addWidget(self.linkToDiscussPage)
        self.masterLayout.addWidget(self.tipButton)

    def openHelpDocument(self):
        try:
            if platfm == 'Darwin':
                import shlex
                os.system("open " + shlex.quote(self.tr("./README_zh.html")))
            elif platfm == 'Windows':
                os.startfile(os.path.realpath(self.tr('./README_zh.html')))
        except:
            pass
