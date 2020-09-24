
def excepthook(exec_type, exec_val, exec_tb):
    with open('traceback.log', 'w') as f:
        formatted_tb = format_exception(exec_type, exec_val, exec_tb)
        print(*formatted_tb,
              '\n请将以上信息发给1292756898@qq.com，或提交到'
              'https://github.com/HaujetZhao/QuickCut/issues', file=f)
    msg = ('程序发生致命错误，即将退出。\n'
           '请查看同目录下的traceback.log获取详细错误信息。')
    try:
        QMessageBox.critical(main, mainWindow.tr('致命错误'), mainWindow.tr(msg))
    except NameError:
        print('没有发现主窗口')
    sys.exit(1)
