import os, subprocess, time, json, srt, datetime, re
from moduels.component.NormalValue import 常量

from tencentcloud.asr.v20190614 import asr_client, models
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile


# 相关文档 https://cloud.tencent.com/document/api/1093/37822#SDK

class TencentTrans():
    def __init__(self):
        pass

    def setupApi(self, appKey, language, accessKeyId, accessKeySecret):
        self.appKey = appKey
        self.accessKeyId = accessKeyId
        self.accessKeySecret = accessKeySecret
        # print(language)
        if language == '中文普通话':
            self.language = 'zh'
        elif language == '英语':
            self.language = 'en'
        elif language == '粤语':
            self.language = 'ca'

    def urlAudioToSrt(self, output, url, language):
        # 语言可以有：en, zh, ca
        # 16k_zh：16k 中文普通话通用；
        # 16k_en：16k 英语；
        # 16k_ca：16k 粤语。
        output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('即将识别：') + url)
        try:
            # 此处<Your SecretId><Your SecretKey>需要替换成客户自己的账号信息
            cred = credential.Credential(self.accessKeyId, self.accessKeySecret)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "asr.tencentcloudapi.com"
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            clientProfile.signMethod = "TC3-HMAC-SHA256"
            client = asr_client.AsrClient(cred, "ap-shanghai", clientProfile)
            req = models.CreateRecTaskRequest()
            # params = {"EngineModelType":"16k_" + language,"ChannelNum":1,"ResTextFormat":0,"SourceType":0,"Url":url}
            params = {"EngineModelType": "16k_" + language, "ChannelNum": 1, "ResTextFormat": 0, "SourceType": 0,
                      "Url": url}
            req._deserialize(params)
            resp = client.CreateRecTask(req)
            # print(resp.to_json_string())
            # windows 系统使用下面一行替换上面一行
            # print(resp.to_json_string().decode('UTF-8').encode('GBK') )
            resp = json.loads(resp.to_json_string())
            return resp['Data']['TaskId']

        except TencentCloudSDKException as err:
            output.print(err)

    def queryResult(self, output, taskid):
        # try:

        cred = credential.Credential(self.accessKeyId, self.accessKeySecret)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "asr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = asr_client.AsrClient(cred, "ap-shanghai", clientProfile)

        req = models.DescribeTaskStatusRequest()
        params = '{"TaskId":%s}' % (taskid)
        req.from_json_string(params)

        while True:
            try:
                resp = json.loads(client.DescribeTaskStatus(req).to_json_string())
                status = resp['Data']['Status'] # Status	Integer	任务状态码，0：任务等待，1：任务执行中，2：任务成功，3：任务失败。
                if status == 0:
                    output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('云端任务排队中，5秒之后再次查询\n'))
                    time.sleep(5)
                elif status == 1:
                    output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('任务进行中，3秒之后再次查询\n'))
                    time.sleep(3)
                elif status == 2:
                    output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('任务完成\n'))
                    break
                elif status == 3:# 出错了
                    output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('服务器有点错误,错误原因是：') + resp['Data']['ErrorMsg'])
                    time.sleep(3)
            except TencentCloudSDKException as e:
                print(e)
                break
        # 将返回的内容中的结果部分提取出来，转变成一个列表：['[0:0.940,0:3.250]  这是第一句话保留。', '[0:4.400,0:7.550]  这是第二句话咔嚓。', '[0:8.420,0:10.850]  这是第三句话保留。', '[0:11.980,0:14.730]  这是第四句话咔嚓。', '[0:15.480,0:18.250]  这是第五句话保留。']
        transResult = resp['Data']['Result'].splitlines()
        return transResult

        # except TencentCloudSDKException as err:
        #     print(err)

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
        output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('\n上传目标路径：') + remoteFile + '\n\n')

        # 上传音频文件 upload audio to cloud
        output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('上传音频中\n'))
        remoteLink = oss.upload(audioFile, remoteFile)
        output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('音频上传完毕，路径是：%s\n') % remoteLink)
        # 识别文字 recognize
        output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('正在识别中\n'))
        taskId = self.urlAudioToSrt(output, remoteLink, self.language)

        # 获取识别结果
        output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('正在读取结果中\n'))
        output.print('taskId: %s\n' % taskId)
        transResult = self.queryResult(output, taskId)

        # 删除文件
        oss.delete(remoteFile)

        # 新建一个列表，用于存放字幕
        subtitles = list()
        for i in range(len(transResult)):
            timestampAndSentence = transResult[i].split("  ")
            timestamp = timestampAndSentence[0].lstrip(r'[').rstrip(r']').split(',')
            startTimestamp = timestamp[0].split(':')
            startMinute = int(startTimestamp[0])
            startSecondsAndMicroseconds = startTimestamp[1].split('.')
            startSeconds = int(startSecondsAndMicroseconds[0]) + startMinute * 60
            startMicroseconds = int(startSecondsAndMicroseconds[1]) * 1000

            endTimestamp = timestamp[1].split(':')
            endMinute = int(endTimestamp[0])
            endSecondsAndMicroseconds = endTimestamp[1].split('.')
            endSeconds = int(endSecondsAndMicroseconds[0]) + endMinute * 60
            endMicroseconds = int(endSecondsAndMicroseconds[1]) * 1000

            sentence = timestampAndSentence[1]

            startTime = datetime.timedelta(seconds=startSeconds, microseconds=startMicroseconds)

            # 设定字幕终止时间
            if endSeconds == 0:
                endTime = datetime.timedelta(microseconds=endMicroseconds)
            else:
                endTime = datetime.timedelta(seconds=endSeconds, microseconds=endMicroseconds)

            # 字幕的内容还需要去掉未尾的标点
            subContent = re.sub('(.)$|(。)$|(. )$', '', sentence)

            # 合成 srt 类
            subtitle = srt.Subtitle(index=i, start=startTime, end=endTime, content=subContent)

            # 把合成的 srt 类字幕，附加到列表
            subtitles.append(subtitle)

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
        output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('现在开始生成单声道、 16000Hz 的 wav 音频：\n') + command)
        subprocess.call(command, shell=True)
        if not os.path.exists('%s.wav' % (pathPrefix)):
            output.print('生成 wav 文件失败，请检查文件所在路径是否有正常的读写权限，或 ffmpeg 是否能正常工作\n')
        else:
            output.print('wav 文件生成成功\n')
        return '%s.wav' % (pathPrefix)

    def mediaToSrt(self, output, oss, mediaFile):
        # 先生成 wav 格式音频，并获得路径
        wavFile = self.wavGen(output, mediaFile)

        # 从 wav 音频文件生成 srt 字幕, 并得到生成字幕的路径
        srtFilePath = self.subGen(output, oss, wavFile)

        # 删除 wav 文件
        os.remove(wavFile)
        output.print(常量.mainWindow.ffmpegAutoSrtTab.tr('已删除 oss 音频文件\n'))

        return srtFilePath
