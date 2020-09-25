import os, subprocess, time, json, srt, datetime
from moduels.component.NormalValue import 常量

from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

class AliTrans():
    def __init__(self):
        pass

    def setupApi(self, appKey, language, accessKeyId, accessKeySecret):
        self.appKey = appKey
        self.accessKeyId = accessKeyId
        self.accessKeySecret = accessKeySecret

    def fileTrans(self, output, accessKeyId, accessKeySecret, appKey, fileLink):
        # 地域ID，常量内容，请勿改变
        REGION_ID = "cn-shanghai"
        PRODUCT = "nls-filetrans"
        DOMAIN = "filetrans.cn-shanghai.aliyuncs.com"
        API_VERSION = "2018-08-17"
        POST_REQUEST_ACTION = "SubmitTask"
        GET_REQUEST_ACTION = "GetTaskResult"
        # 请求参数key
        KEY_APP_KEY = "appkey"
        KEY_FILE_LINK = "file_link"
        KEY_VERSION = "version"
        KEY_ENABLE_WORDS = "enable_words"
        # 是否开启智能分轨
        KEY_AUTO_SPLIT = "auto_split"
        # 响应参数key
        KEY_TASK = "Task"
        KEY_TASK_ID = "TaskId"
        KEY_STATUS_TEXT = "StatusText"
        KEY_RESULT = "Result"
        # 状态值
        STATUS_SUCCESS = "SUCCESS"
        STATUS_RUNNING = "RUNNING"
        STATUS_QUEUEING = "QUEUEING"
        # 创建AcsClient实例
        client = AcsClient(accessKeyId.replace(' ', '').replace('\n', ''), accessKeySecret.replace(' ', '').replace('\n', ''), REGION_ID)
        # 提交录音文件识别请求
        postRequest = CommonRequest()
        postRequest.set_domain(DOMAIN)
        postRequest.set_version(API_VERSION)
        postRequest.set_product(PRODUCT)
        postRequest.set_action_name(POST_REQUEST_ACTION)
        postRequest.set_method('POST')
        # 新接入请使用4.0版本，已接入(默认2.0)如需维持现状，请注释掉该参数设置
        # 设置是否输出词信息，默认为false，开启时需要设置version为4.0
        task = {KEY_APP_KEY: appKey.replace(' ', '').replace('\n', ''), KEY_FILE_LINK: fileLink, KEY_VERSION: "4.0", KEY_ENABLE_WORDS: False}
        # 开启智能分轨，如果开启智能分轨 task中设置KEY_AUTO_SPLIT : True
        # task = {KEY_APP_KEY : appKey, KEY_FILE_LINK : fileLink, KEY_VERSION : "4.0", KEY_ENABLE_WORDS : False, KEY_AUTO_SPLIT : True}
        task = json.dumps(task)
        # print(task)
        postRequest.add_body_params(KEY_TASK, task)
        taskId = ""
        try:
            postResponse = client.do_action_with_exception(postRequest)
            print(1)
            print(postResponse)
            postResponse = json.loads(postResponse)
            statusText = postResponse[KEY_STATUS_TEXT]
            print(statusText)
            print(accessKeyId)
            print(accessKeySecret)

            if statusText == STATUS_SUCCESS:
                output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('录音文件识别请求成功响应！\n'))
                taskId = postResponse[KEY_TASK_ID]
            elif statusText == 'USER_BIZDURATION_QUOTA_EXCEED':
                output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('你今天的阿里云识别额度已用完！\n'))
            else:
                output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('录音文件识别请求失败，失败原因是：%s，你可以将这个代码复制，到 “https://help.aliyun.com/document_detail/90727.html” 查询具体原因\n') % statusText)
                return
        except ServerException as e:
            output.print('阿里云返回了错误信息，你的 api 的 accessKeyId 、accessKeySecret 不正确，或者没有设置正确的权限\n')
            return
        except ClientException as e:
            output.print('客户端错误\n')
            return
        # 创建CommonRequest，设置任务ID
        getRequest = CommonRequest()
        getRequest.set_domain(DOMAIN)
        getRequest.set_version(API_VERSION)
        getRequest.set_product(PRODUCT)
        getRequest.set_action_name(GET_REQUEST_ACTION)
        getRequest.set_method('GET')
        getRequest.add_query_param(KEY_TASK_ID, taskId)
        # 提交录音文件识别结果查询请求
        # 以轮询的方式进行识别结果的查询，直到服务端返回的状态描述符为"SUCCESS"、"SUCCESS_WITH_NO_VALID_FRAGMENT"，
        # 或者为错误描述，则结束轮询。
        statusText = ""
        while True:
            try:
                self.getResponse = client.do_action_with_exception(getRequest)
                self.getResponse = json.loads(self.getResponse)
                statusText = self.getResponse[KEY_STATUS_TEXT]
                if statusText == STATUS_RUNNING or statusText == STATUS_QUEUEING:
                    # 继续轮询
                    if statusText == STATUS_QUEUEING:
                        output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('云端任务正在排队中，3 秒后重新查询\n'))
                    elif statusText == STATUS_RUNNING:
                        output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('音频转文字中，3 秒后重新查询\n'))
                    time.sleep(3)
                else:
                    # 退出轮询
                    break
            except ServerException as e:
                output.print(e)
                pass
            except ClientException as e:
                output.print(e)
                pass
        if statusText == STATUS_SUCCESS:
            output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('录音文件识别成功！\n'))
        else:
            output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('录音文件识别失败！\n'))
        return

    def subGen(self, output, oss, audioFile):

        # 确定本地音频文件名
        audioFileFullName = os.path.basename(audioFile)

        # 确定当前日期
        localTime = time.localtime(time.time())
        year = localTime.tm_year
        month = localTime.tm_mon
        day = localTime.tm_mday

        # 用当前日期给 oss 文件指定上传路径
        remoteFile = '%s/%s/%s/%s' % (year, month, day, audioFileFullName)
        # 目标链接要转换成 base64 的

        output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('上传 oss 目标路径：') + remoteFile + '\n')

        # 上传音频文件 upload audio to cloud
        output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('上传音频中\n'))
        remoteLink = oss.upload(audioFile, remoteFile)
        output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('音频上传完毕，路径是：%s\n') % remoteLink)

        # 识别文字 recognize
        output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('正在识别中\n'))
        self.fileTrans(output, self.accessKeyId, self.accessKeySecret, self.appKey, remoteLink)

        # 删除文件

        output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('识别完成，现在删除 oss 上的音频文件：') + remoteFile + '\n')
        oss.delete(remoteFile)

        # 新建一个列表，用于存放字幕
        subtitles = list()
        try:
            for i in range(len(self.getResponse['Result']['Sentences'])):
                startSeconds = self.getResponse['Result']['Sentences'][i]['BeginTime'] // 1000
                startMicroseconds = self.getResponse['Result']['Sentences'][i]['BeginTime'] % 1000 * 1000
                endSeconds = self.getResponse['Result']['Sentences'][i]['EndTime'] // 1000
                endMicroseconds = self.getResponse['Result']['Sentences'][i]['EndTime'] % 1000 * 1000

                # 设定字幕起始时间
                if startSeconds == 0:
                    startTime = datetime.timedelta(microseconds=startMicroseconds)
                else:
                    startTime = datetime.timedelta(seconds=startSeconds, microseconds=startMicroseconds)

                # 设定字幕终止时间
                if endSeconds == 0:
                    endTime = datetime.timedelta(microseconds=endMicroseconds)
                else:
                    endTime = datetime.timedelta(seconds=endSeconds, microseconds=endMicroseconds)

                # 设定字幕内容
                subContent = self.getResponse['Result']['Sentences'][i]['Text']

                # 字幕的内容还需要去掉未尾的标点
                subContent = re.sub('(.)$|(。)$|(. )$', '', subContent)

                # 合成 srt 类
                subtitle = srt.Subtitle(index=i, start=startTime, end=endTime, content=subContent)

                # 把合成的 srt 类字幕，附加到列表
                subtitles.append(subtitle)
        except:
            output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('云端数据转字幕的过程中出错了，可能是没有识别到文字\n'))
            subtitles = [srt.Subtitle(index=0, start=datetime.timedelta(0), end=datetime.timedelta(microseconds=480000),
                                      content=' ', proprietary='')]

        # 生成 srt 格式的字幕
        srtSub = srt.compose(subtitles, reindex=True, start_index=1, strict=True)

        # 得到输入文件除了除了扩展名外的名字
        pathPrefix = os.path.splitext(audioFile)[0]

        # 得到要写入的 srt 文件名
        srtPath = '%s.srt' % (pathPrefix)

        # 写入字幕
        with open(srtPath, 'w+', encoding='utf-8') as srtFile:
            srtFile.write(srtSub)

        return srtPath

    def wavGen(self, output, mediaFile):
        # 得到输入文件除了除了扩展名外的名字
        pathPrefix = os.path.splitext(mediaFile)[0]
        # ffmpeg 命令
        command = 'ffmpeg -hide_banner -y -i "%s" -ac 1 -ar 16000 "%s.wav"' % (mediaFile, pathPrefix)
        output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('现在开始生成单声道、 16000Hz 的 wav 音频：%s \n') % command)
        subprocess.call(command, shell=True)
        if not os.path.exists('%s.wav' % (pathPrefix)):
            output.print('生成 wav 文件失败，请检查文件所在路径是否有正常的读写权限，或 ffmpeg 是否能正常工作\n')
        else:
            output.print('wav 文件生成成功\n')
        return '%s.wav' % (pathPrefix)

    # 用媒体文件生成 srt
    def mediaToSrt(self, output, oss, mediaFile):
        # 先生成 wav 格式音频，并获得路径
        wavFile = self.wavGen(output, mediaFile)

        # 从 wav 音频文件生成 srt 字幕, 并得到生成字幕的路径
        srtFilePath = self.subGen(output, oss, wavFile)

        # 删除 wav 文件
        os.remove(wavFile)
        output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('已删除 oss 音频文件\n'))

        return srtFilePath
