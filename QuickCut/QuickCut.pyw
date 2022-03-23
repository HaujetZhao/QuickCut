# -*- coding: UTF-8 -*-

'''
一点答疑：为什么要在这个软件中使用那么多中文变量，而不是使用英文变量？

1. 我英文太菜，看中文母语舒服
2. 我很享受用五笔打中文，精准、优雅
'''
from os import path

import os
import sys
import logging

try:
    os.chdir(path.dirname(path.abspath(__file__))) # 更改工作目录，指向正确的当前文件夹，才能读取 database.db
    sys.path.append(path.dirname(path.abspath(__file__))) # 将当前目录导入 python 寻找 package 和 moduel 的变量
except:
    print('更改使用路径失败，不过没关系')

import sqlite3
import platform
import subprocess

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from moduels.database.initDatabase import 初始化数据库
from moduels.function.checkDBLanguage import * # 引入检查和初始化语言设置的函数
from moduels.function.excepthook import *
from moduels.component.NormalValue import 常量
from moduels.gui.MainWindow import MainWindow
from moduels.gui.SystemTray import SystemTray



############# 程序入口 ################

def main():
    logging.disable() # chardet 的 debug logging 很烦人，关掉
    # sys.excepthook = 自定义异常勾子
    os.environ['PATH'] += os.pathsep + os.getcwd()

    # 高分屏相关，去掉下行注释，会放大软件界面（有点像老人模式）
    # QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)

    初始化数据库() # 如果数据库不存在，就新建

    语言 = 从DB获取语言()  # 得到已设置的语言
    if 语言 != '中文':
        print('language changed')
        翻译器 = QTranslator()
        翻译器.load('./languages/%s.qm' % 语言) # 没检查语文文件是否存在，这里可能脆弱
        app.installTranslator(翻译器)

    主窗口 = MainWindow()

    tray = SystemTray(QIcon(常量.图标路径), 主窗口)

    sys.exit(app.exec_())
    conn.close()

if __name__ == '__main__':
    main()
