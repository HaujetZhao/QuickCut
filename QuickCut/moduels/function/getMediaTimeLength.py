
# 得到视频长度
def getMediaTimeLength(inputFile):
    # 用于获取一个视频或者音频文件的长度
    # try:
    print('start getting info')
    info = pymediainfo.MediaInfo.parse(inputFile)
    print('info' + str(info))
    duration = 0
    print('info.tracks' + str(info.tracks))
    for track in info.tracks:
        print('track.duration' + str(track.duration))
        if float(track.duration) > duration:
            duration = track.duration
    return float(duration / 1000)
