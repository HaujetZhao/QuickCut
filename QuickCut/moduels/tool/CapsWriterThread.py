# -*- coding: UTF-8 -*-

from PySide2.QtCore import *
from PySide2.QtGui import *
import pyaudio, sqlite3, time, json, keyboard, threading

import ali_speech
from ali_speech.callbacks import SpeechRecognizerCallback
from ali_speech.constant import ASRFormat
from ali_speech.constant import ASRSampleRate

from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from moduels.component.NormalValue import 常量


# 语音输入
class CapsWriterThread(QThread):
    signal = Signal(str)


    outputBox = None  # 用于显示输出的控件，如一个 QEditBox，它需要有自定义的 print 方法。

    appKey = None

    accessKeyId = None

    accessKeySecret = None

    CHUNK = 1024  # 数据包或者数据片段
    FORMAT = pyaudio.paInt16  # pyaudio.paInt16表示我们使用量化位数 16位来进行录音
    CHANNELS = 1  # 声道，1为单声道，2为双声道
    RATE = 16000  # 采样率，每秒钟16000次

    count = 1  # 计数
    lastTime = 0
    pre = True  # 是否准备开始录音
    runRecognition = False  # 控制录音是否停止
    正在识别 = False

    def __init__(self, parent=None):
        super(CapsWriterThread, self).__init__(parent)
        ########改用主数据库

    def print(self, text):
        self.signal.emit(text)

    def run(self):
        try:
            self.client = ali_speech.NlsClient()
            self.client.set_log_level('ERROR')  # 设置 client 输出日志信息的级别：DEBUG、INFO、WARNING、ERROR

            self.识别器列表 = []
            self.补全识别器()
            self.识别器 = self.识别器列表.pop(0)
            self.p = pyaudio.PyAudio()

            self.outputBox.print(self.tr("""\r\n初始化完成，现在可以将本工具最小化，在需要输入的界面，按住 CapsLock 键 0.3 秒后开始说话，松开 CapsLock 键后识别结果会自动输入\r\n"""))

            keyboard.hook_key('caps lock', self.on_hotkey)
            self.outputBox.print(self.tr('{}:按住 CapsLock 键 0.3 秒后开始说话...').format(self.count))
            keyboard.wait()
        except:
            # QMessageBox.warning(main, '语音识别出错','语音识别出错，极有可能是 API 填写有误，请检查一下。')
            print('语音识别输入功能启动失败')
            try:
                keyboard.unhook_all()
            except:
                pass
            return

    class MyCallback(SpeechRecognizerCallback):
        """
        构造函数的参数没有要求，可根据需要设置添加
        示例中的name参数可作为待识别的音频文件名，用于在多线程中进行区分
        """
        def __init__(self, name='default'):
            self._name = name
            self.message = None
            self.outputBox = 常量.mainWindow.capsWriterTab.outputBox

        def on_started(self, message):
            # print('MyCallback.OnRecognitionStarted: %s' % message)
            pass

        def on_result_changed(self, message):
            self.outputBox.print(self.tr('任务信息: task_id: %s, result: %s') % (message['header']['task_id'], message['payload']['result']))

        def on_completed(self, message):
            if message != self.message:
                self.message = message
                # print(message)
                self.outputBox.print(常量.mainWindow.capsWriterTab.tr('结果: %s') % (message['payload']['result']))
                result = message['payload']['result']
                try:
                    if result[-1] == '。':  # 如果最后一个符号是句号，就去掉。
                        result = result[0:-1]
                except Exception as e:
                    pass

                keyboard.write(result)  # 输入识别结果

        def on_task_failed(self, message):
            print(self.tr('识别任务失败: %s') % message)

        def on_channel_closed(self):
            # print('MyCallback.OnRecognitionChannelClosed')
            pass

    def get_token(self):
        newConn = sqlite3.connect(常量.dbname)
        token = newConn.cursor().execute('select value from %s where item = "%s";' % (常量.preferenceTableName, 'CapsWriterTokenId')).fetchone()[0]
        expireTime = newConn.cursor().execute('select value from %s where item = "%s";' % (常量.preferenceTableName, 'CapsWriterTokenExpireTime')).fetchone()[0]
        # 要是 token 还有 5 秒过期，那就重新获得一个。
        if (int(expireTime) - time.time()) < 5:
            # 创建AcsClient实例
            client = AcsClient(
                self.accessKeyId,  # 填写 AccessID
                self.accessKeySecret,  # 填写 AccessKey
                "cn-shanghai"
            );
            # 创建request，并设置参数
            request = CommonRequest()
            request.set_method('POST')
            request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
            request.set_version('2019-02-28')
            request.set_action_name('CreateToken')
            response = json.loads(client.do_action_with_exception(request))
            token = response['Token']['Id']
            expireTime = str(response['Token']['ExpireTime'])
            newConn.cursor().execute(
                '''update %s set value = '%s'  where item = '%s'; ''' % (
                    常量.preferenceTableName, token, 'CapsWriterTokenId'))
            newConn.cursor().execute(
                '''update %s set value = '%s' where item = '%s'; ''' % (
                常量.preferenceTableName, expireTime, 'CapsWriterTokenExpireTime'))
            newConn.commit()
            newConn.close()
        return token

    def get_recognizer(self, client, appkey):
        token = self.get_token()
        audio_name = 'none'
        callback = self.MyCallback(audio_name)
        recognizer = client.create_recognizer(callback)
        recognizer.set_appkey(appkey)
        recognizer.set_token(token)
        recognizer.set_format(ASRFormat.PCM)
        recognizer.set_sample_rate(ASRSampleRate.SAMPLE_RATE_16K)
        recognizer.set_enable_intermediate_result(False)
        recognizer.set_enable_punctuation_prediction(True)
        recognizer.set_enable_inverse_text_normalization(True)
        return (recognizer)

    # 因为关闭 recognizer 有点慢，就须做成一个函数，用多线程关闭它。
    def 为下一次输入准备识别器(self):
        self.识别器 = self.识别器列表.pop(0)
        self.补全识别器()

    def close_recognizer(self, 识别器):
        识别器.close()
        print('识别器关掉了')

    # 处理热键响应
    def on_hotkey(self, event):
        if event.event_type == "down":
            if self.pre and (not self.runRecognition):
                self.pre = False
                self.runRecognition = True
                try:
                    threading.Thread(target=self.process).start()
                except:
                    print('process 启动失败')
            else:
                pass
        elif event.event_type == "up":
            self.pre, self.runRecognition = True, False
        else:
            # print(event.event_type)
            pass

    # 处理是否开始录音
    def process(self):
        self.data = []
        threading.Thread(target=self.recoding, args=[self.p]).start()  # 开始录音
        threading.Thread(target=self.recognizing, args=[self.p]).start()  # 开始识别
        self.count += 1

    def recoding(self, p):
        # try:
        self.正在录音 = True
        # print('准备录制')
        stream = p.open(channels=self.CHANNELS,
                        format=self.FORMAT,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        # print('录制器准备完毕')
        for i in range(5):
            if self.runRecognition:
                # print('准备录制第 %s 段' % i)
                self.data.append(stream.read(self.CHUNK))
                # print('录制了第 %s 段' % i)
            else:
                self.data = []
                return
        # 在这里录下5个小片段，大约录制了0.32秒，如果这个时候松开了大写锁定键，就不打开连接。如果还继续按着，那就开始识别。
        while self.runRecognition:
            self.data.append(stream.read(self.CHUNK))
        self.data.append(stream.read(self.CHUNK))
        self.正在录音 = False
        keyboard.press_and_release('caps lock')  # 再按下大写锁定键，还原大写锁定
        stream.stop_stream()# print('停止录制流')
        stream.close()

    # 这边开始上传识别
    def recognizing(self, p):
        识别器 = self.识别器
        # print('识别器开始等待')
        for i in range(5):
            time.sleep(0.06)
            if not self.runRecognition:
                return # 如果这个时候大写锁定键松开了  那就返回
        # print('识别器等待完闭')
        # try:
        self.outputBox.print(self.tr('\n{}:在听了，说完了请松开 CapsLock 键...').format(self.count))
        # 接下来设置一下托盘栏的听写图标
        # print('识别器开始设置新图标')
        if 常量.platfm == 'Darwin':
            常量.tray.setIcon(QIcon('misc/icon_listning.icns'))
        else:
            常量.tray.setIcon(QIcon('misc/icon_listning.ico'))
        # print('新图标设置完毕')
        threading.Thread(target=self.为下一次输入准备识别器).start()  # 用新线程为下一次识别准备识别器
        # print('准备新的识别器')
        self.正在识别 = True
        ret = 识别器.start() # 识别器开始识别
        # print('识别器开始识别')
        已发送音频片段数 = 0 # 对音频片段记数
        if ret < 0:
            if 常量.platfm == 'Darwin':
                常量.tray.setIcon(QIcon('misc/icon.icns'))
            else:
                常量.tray.setIcon(QIcon('misc/icon.ico'))
            return ret # 如果开始识别出错了，那就返回
        while self.正在录音:
            while 已发送音频片段数 < len(self.data):
                ret = 识别器.send(self.data[已发送音频片段数]) # 发送音频数据
                已发送音频片段数 += 1
            time.sleep(0.032)
        self.outputBox.print(self.tr('\n{}:按住 CapsLock 键 0.3 秒后开始说话...').format(self.count + 1))
        if 常量.platfm == 'Darwin':
            常量.tray.setIcon(QIcon('misc/icon.icns'))
        else:
            常量.tray.setIcon(QIcon('misc/icon.ico'))
        识别器.stop()
        识别器.close()
        self.data = []

        # print('识别器停止')
        # if 识别器被使用: # 不再关闭它，让 python 自动回收
        # threading.Thread(target=self.close_recognizer, args=[识别器]).start()  # 关闭 recognizer
        #     print('识别器关闭进程已启动')



        # print('重置数据为空')
        # print('')

    def clean(self):
        # 结束这个进程前的清理工作
        keyboard.unhook('caps lock')

    def 补全识别器(self):
        if len(self.识别器列表) < 2:
            for i in range(5):
                self.识别器列表.append(self.get_recognizer(self.client, self.appKey))


