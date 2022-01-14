# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from moduels.component.NormalValue import 常量
from moduels.tool.AliOss import AliOss
from moduels.tool.TencentOss import TencentOss
from moduels.tool.AliTrans import AliTrans
from moduels.tool.TencentTrans import TencentTrans

import sqlite3


# 自动字幕，其实是基于音频转写文本引擎的自动字幕
class FileTranscribeAutoSrtThread(QThread):
    signal = Signal(str)
    signalForFFmpeg = Signal(str)

    output = None  # 用于显示输出的控件，如一个 QEditBox，它需要有自定义的 print 方法。

    apiEngine = ''

    inputFile = None

    def __init__(self, parent=None):
        super(FileTranscribeAutoSrtThread, self).__init__(parent)

    def print(self, text):
        self.signal.emit(text)

    def run(self):
        newConn = sqlite3.connect(常量.数据库路径)
        ossData = newConn.cursor().execute(
            '''select provider, bucketName, endPoint, accessKeyId,  accessKeySecret from %s ;''' % (
                常量.oss表名)).fetchone()
        try:
            ossProvider, ossBucketName, ossEndPoint, ossAccessKeyId, ossAccessKeySecret = ossData[0], ossData[1], \
                                                                                      ossData[2], ossData[3], \
                                                                                      ossData[4]
        except:
            self.output.print(self.tr('API 填写有误，请核实。无法继续转字幕，任务取消。'))
            return
        if ossProvider == 'Alibaba':
            oss = AliOss()
            oss.auth(ossBucketName, ossEndPoint, ossAccessKeyId, ossAccessKeySecret)
        elif ossProvider == 'Tencent':
            oss = TencentOss()
            oss.auth(ossBucketName, ossEndPoint, ossAccessKeyId, ossAccessKeySecret)

        apiData = newConn.cursor().execute(
            '''select provider, appKey, language, accessKeyId, accessKeySecret from %s where name = '%s';''' % (
                常量.api表名, self.apiEngine)).fetchone()
        newConn.close()
        # 不在这里关数据库了()

        apiProvider, apiappKey, apiLanguage, apiAccessKeyId, apiAccessKeySecret = apiData[0].replace('\n', ''), apiData[1].replace('\n', ''), apiData[
            2].replace('\n', ''), apiData[3].replace('\n', ''), apiData[4].replace('\n', '')
        if apiProvider == 'Alibaba':
            transEngine = AliTrans()
        elif apiProvider == 'Tencent':
            transEngine = TencentTrans()
        # try:
        transEngine.setupApi(apiappKey, apiLanguage, apiAccessKeyId, apiAccessKeySecret)

        srtSubtitleFile = transEngine.mediaToSrt(self.output, oss, self.inputFile)
        # except:
        #     self.print(self.tr('转字幕出问题了，有可能是 oss 填写错误，或者语音引擎出错误，总之，请检查你的 api 和 KeyAccess 的权限\n\n这次用到的 oss AccessKeyId 是：%s,       \n这次用到的 oss AccessKeySecret 是：%s\n\n这次用到的语音引擎 AppKey 是：%s，     \n这次用到的语音引擎 AccessKeyId 是：%s，     \n这次用到的语音引擎 AccessKeySecret 是：%s，    ') % (ossAccessKeyId, ossAccessKeySecret, apiappKey, apiAccessKeyId, apiAccessKeySecret))
        #     return

        self.print(self.tr('\n\n转字幕完成\n\n'))
        # except:
        #     self.print('转字幕过程出错了')
