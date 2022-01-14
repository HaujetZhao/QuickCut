import sys


def 自定义异常勾子(异常类, 异常实例, 回溯对象):
    # 还不确定怎么处理异常
    # 有待学习

    # with open('traceback.log', 'w') as f:
    #     formatted_tb = format_exception(异常类, 异常实例, 回溯对象)
    #     print(*formatted_tb,
    #           '\n请将以上信息发给1292756898@qq.com，或提交到'
    #           'https://github.com/HaujetZhao/QuickCut/issues', file=f)
    # msg = ('程序发生致命错误，即将退出。\n'
    #        '请查看同目录下的traceback.log获取详细错误信息。')
    # try:
    #     QMessageBox.critical(main, mainWindow.tr('致命错误'), mainWindow.tr(msg))
    # except NameError:
    #     print('没有发现主窗口')
    # sys.exit(1)
    print(f'异常类：{异常类}\n异常实例：{异常实例}\n回溯对象：{回溯对象}\n')
    ...
