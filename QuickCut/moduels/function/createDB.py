# -*- coding: UTF-8 -*-

from moduels.component.NormalValue import 常量

def createDB():
    conn = 常量.conn
    ossTableName = 常量.ossTableName
    apiTableName = 常量.apiTableName
    preferenceTableName = 常量.preferenceTableName
    cursor = conn.cursor()
    result = cursor.execute('select * from sqlite_master where name = "%s";' % (ossTableName)) # 检查 oss 表在不在数据库
    if result.fetchone() == None:
        cursor.execute('''create table %s (
                                    id integer primary key autoincrement,
                                    provider text, 
                                    endPoint text, 
                                    bucketName text, 
                                    bucketDomain text,
                                    accessKeyId text, 
                                    accessKeySecret text)''' % ossTableName)
    else:
        print('oss 表单已存在')

    result = cursor.execute('select * from sqlite_master where name = "%s";' % (apiTableName)) # 检查 api 表在不在数据库
    if result.fetchone() == None:
        cursor.execute('''create table %s (
                                    id integer primary key autoincrement,
                                    name text, 
                                    provider text, 
                                    appKey text, 
                                    language text, 
                                    accessKeyId text, 
                                    accessKeySecret text
                                    )''' % apiTableName)
    else:
        print('api 表单已存在')

    result = cursor.execute('select * from sqlite_master where name = "%s";' % (preferenceTableName)) # 检查初始偏好设置表在不在数据库
    if result.fetchone() == None:
        cursor.execute('''create table %s (
                                            id integer primary key autoincrement,
                                            item text,
                                            value text
                                            )''' % preferenceTableName)

        cursor.execute('''insert into %s (item, value) values ('%s', '%s');''' % (
        常量.preferenceTableName, 'hideToTrayWhenHitCloseButton', 'False'))
    else:
        print('偏好设置表单已存在')
    conn.commit() # 最后要提交更改
