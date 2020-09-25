# -*- coding: UTF-8 -*-

from moduels.tool.CommandThread import CommandThread
from moduels.gui.Console import Console
from moduels.component.NormalValue import 常量

# 执行命令
def execute(command):
    # 判断一下系统，如果是windows系统，就直接将命令在命令行窗口中运行，避免在程序中运行时候的卡顿。
    # 主要是因为手上没有图形化的linux系统和mac os系统，不知道怎么打开他们的终端执行某个个命令，所以就将命令在程序中运行，输出到一个新窗口的文本编辑框。
    # system = platform.system()
    # if system == 'Windows':
    #     os.system('start cmd /k ' + command)
    # else:
    #     console = Console(常量.mainWindow)
    #     console.runCommand(command)

    # 新方法，执行子进程，在新窗口输出
    thread = CommandThread()  # 新建一个子进程
    thread.command = command  # 将要执行的命令赋予子进程
    window = Console(常量.mainWindow)  # 显示一个新窗口，用于显示子进程的输出
    output = window.consoleBox  # 获得新窗口中的输出控件
    outputForFFmpeg = window.consoleBoxForFFmpeg
    thread.signal.connect(output.print)  # 将 子进程中的输出信号 连接到 新窗口输出控件的输出槽
    thread.signalForFFmpeg.connect(outputForFFmpeg.print)  # 将 子进程中的输出信号 连接到 新窗口输出控件的输出槽
    window.thread = thread  # 把这里的剪辑子进程赋值给新窗口，这样新窗口就可以在关闭的时候也把进程退出
    thread.start()
