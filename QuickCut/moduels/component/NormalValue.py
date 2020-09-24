import sqlite3
import platform
import subprocess
from moduels.component.ApiUpdated import ApiUpdated

class NormalValue():
    dbname = './database.db'  # 存储预设的数据库名字
    conn = sqlite3.connect(dbname)
    presetTableName = 'commandPreset'
    preferenceTableName = 'preference'
    ossTableName = 'oss'
    apiTableName = 'api'
    styleFile = './style.css'
    finalCommand = ''
    version = 'V1.6.10'
    apiUpdateBroadCaster = ApiUpdated()
    platfm = platform.system()
    if platfm == 'Windows':
        subprocessStartUpInfo = subprocess.STARTUPINFO()
        subprocessStartUpInfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
        subprocessStartUpInfo.wShowWindow = subprocess.SW_HIDE
    else:
        pass

常量 = NormalValue()
