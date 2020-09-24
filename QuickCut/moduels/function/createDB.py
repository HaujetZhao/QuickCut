
def createDB():
    ########改用主数据库
    cursor = conn.cursor()
    result = cursor.execute('select * from sqlite_master where name = "%s";' % (ossTableName))
    # 将oss初始预设写入数据库
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
    result = cursor.execute('select * from sqlite_master where name = "%s";' % (apiTableName))
    # 将api初始预设写入数据库
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
    result = cursor.execute('select * from sqlite_master where name = "%s";' % (preferenceTableName))
    # 将初始偏好设置写入数据库
    if result.fetchone() == None:
        cursor.execute('''create table %s (
                                            id integer primary key autoincrement,
                                            item text,
                                            value text
                                            )''' % preferenceTableName)

        cursor.execute('''insert into %s (item, value) values ('%s', '%s');''' % (
        preferenceTableName, 'hideToTrayWhenHitCloseButton', 'False'))
    else:
        print('偏好设置表单已存在')
    conn.commit()
