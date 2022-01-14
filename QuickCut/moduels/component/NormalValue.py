import sqlite3
import platform
import subprocess
from moduels.component.ApiUpdated import ApiUpdated

class NormalValue():
    数据库路径 = './database.db'  # 存储预设的数据库名字
    conn = sqlite3.connect(数据库路径)

    ffmpeg预设的表名 = 'commandPreset'
    首选项表名 = 'preference'
    oss表名 = 'oss'
    api表名 = 'api'

    默认ffmpeg预设备份 = './misc/sql/commandPreset.sql'
    默认首选项备份 = './misc/sql/preference.sql'
    默认oss备份 = './misc/sql/oss.sql'
    默认api备份 = './misc/sql/api.sql'

    样式文件 = './style.css'
    finalCommand = ''
    程序版本 = 'V1.7.0'

    platfm = platform.system()
    # 不同的系统，托盘图标的格式不同，Win 是 ico 格式，Mac 是 icns 格式
    图标路径 = 'misc/icon.icns' if platfm == 'Darwin' else 'misc/icon.ico'

    # 这一段我也忘记是干什么的了，大概是为了不出现黑窗口
    if platfm == 'Windows':
        subprocessStartUpInfo = subprocess.STARTUPINFO()
        subprocessStartUpInfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
        subprocessStartUpInfo.wShowWindow = subprocess.SW_HIDE
    else:
        pass

    apiUpdateBroadCaster = ApiUpdated()
    主Tab当前已选择的预设名称 = None
    mainWindow = None
    tray = None

常量 = NormalValue()
