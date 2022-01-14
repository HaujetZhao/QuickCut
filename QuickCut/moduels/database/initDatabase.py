from moduels.component.NormalValue import 常量
import sqlite3

def SQLite导入SQL(SQLite路径, SQL路径):
    '''
    SQLite路径: db 文件路径
    SQL路径：SQL 文本文件的路径
    '''
    conn = sqlite3.connect(SQLite路径)
    with open(SQL路径, encoding='utf-8') as f:
        conn.executescript(f.read())

def 初始化预设命令表单():
    SQLite导入SQL(常量.数据库路径, 常量.默认ffmpeg预设备份)

def 初始化首选项表单():
    SQLite导入SQL(常量.数据库路径, 常量.默认首选项备份)

def 初始化oss表单():
    SQLite导入SQL(常量.数据库路径, 常量.默认oss备份)

def 初始化api表单():
    SQLite导入SQL(常量.数据库路径, 常量.默认api备份)

def 初始化数据库():
    oss表名 = 常量.oss表名
    api表名 = 常量.api表名
    首选项表名 = 常量.首选项表名
    预设命令表名 = 常量.ffmpeg预设的表名

    result = 常量.conn.execute('select name from sqlite_master')
    表名列表 = [x[0] for x in result.fetchall()]

    if oss表名 not in 表名列表:
        初始化oss表单()

    if api表名 not in 表名列表:
        初始化api表单()

    if 首选项表名 not in 表名列表:
        初始化首选项表单()

    if 预设命令表名 not in 表名列表:
        初始化预设命令表单()

def 重置预设命令表单():
    预设命令表名 = 常量.ffmpeg预设的表名
    常量.conn.execute(f'drop table {预设命令表名}')
    初始化预设命令表单()