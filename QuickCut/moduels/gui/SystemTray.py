class SystemTray(QSystemTrayIcon):
    def __init__(self, icon, window):
        super(SystemTray, self).__init__()
        self.window = window
        self.setIcon(icon)
        self.setParent(window)
        self.activated.connect(self.trayEvent)  # 设置托盘点击事件处理函数
        self.tray_menu = QMenu(QApplication.desktop())  # 创建菜单
        # self.RestoreAction = QAction(u'还原 ', self, triggered=self.showWindow)  # 添加一级菜单动作选项(还原主窗口)
        self.QuitAction = QAction(self.tr('退出'), self, triggered=self.quit)  # 添加一级菜单动作选项(退出程序)
        # self.StyleAction = QAction(self.tr('更新主题'), self, triggered=mainWindow.loadStyleSheet)  # 添加一级菜单动作选项(更新 QSS)
        # self.tray_menu.addAction(self.RestoreAction)  # 为菜单添加动作
        self.tray_menu.addAction(self.QuitAction)
        # self.tray_menu.addAction(self.StyleAction)
        self.setContextMenu(self.tray_menu)  # 设置系统托盘菜单
        self.show()

    def showWindow(self):
        self.window.showNormal()
        self.window.activateWindow()
        self.window.setWindowFlags(Qt.Window)
        self.window.show()

    def quit(self):
        sys.stdout = sys.__stdout__
        self.hide()
        qApp.quit()

    def trayEvent(self, reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 or reason == 3:
            if mainWindow.isMinimized() or not mainWindow.isVisible():
                # 若是最小化或者最小化到托盘，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
                self.window.showNormal()
                self.window.activateWindow()
                self.window.setWindowFlags(Qt.Window)
                self.window.show()
            else:
                # 若不是最小化，则最小化
                # self.window.showMinimized()
                # self.window.show()
                pass