
class Console(QMainWindow):
    # 这个 console 是个子窗口，调用的时候要指定父窗口。例如：window = Console(mainWindow)
    # 里面包含一个 OutputBox, 可以将信号导到它的 print 方法。
    thread = None

    def __init__(self, parent=None):
        super(Console, self).__init__(parent)
        self.initGui()

    def initGui(self):
        self.setWindowTitle(self.tr('命令运行输出窗口'))
        self.resize(1300, 700)
        self.consoleBox = OutputBox() # 他就用于输出用户定义的打印信息
        self.consoleBoxForFFmpeg = OutputBox()  # 把ffmpeg的输出信息用它输出
        self.consoleBox.setParent(self)
        self.consoleBoxForFFmpeg.setParent(self)
        # self.masterLayout = QVBoxLayout()
        # self.masterLayout.addWidget(self.consoleBox)
        # self.masterLayout.addWidget(QPushButton())
        # self.setLayout(self.masterLayout)
        # self.masterWidget = QWidget()
        # self.masterWidget.setLayout(self.masterLayout)
        self.split = QSplitter(Qt.Vertical)
        self.split.addWidget(self.consoleBox)
        self.split.addWidget(self.consoleBoxForFFmpeg)
        self.setCentralWidget(self.split)
        self.show()

    def closeEvent(self, a0: QCloseEvent) -> None:
        try:
            try:
                if platfm == 'Windows':
                    # 这个方法可以杀死 subprocess 用了 shell=True 开启的子进程，新测好用！
                    # https://stackoverflow.com/questions/13243807/popen-waiting-for-child-process-even-when-the-immediate-child-has-terminated/13256908#13256908
                    subprocess.call("TASKKILL /F /PID {pid} /T".format(pid=self.thread.process.pid), startupinfo=subprocessStartUpInfo)
                else:
                    # 这个没新测，但是 Windows 用不了，只能用于 unix 类的系统
                    os.killpg(os.getpgid(self.thread.process.pid), signal.SIGTERM)
            except:
                pass
            try: # 用于自动剪辑线程，结束前清除其临时文件夹
                self.thread.removeTempFolder()
            except:
                pass

            try:
                self.thread.process.terminate()
            except:
                pass
            self.thread.exit()
            self.thread.setTerminationEnabled(True)
            self.thread.terminate()
        except:
            pass
