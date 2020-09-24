from moduels.component.NormalValue import 常量

def checkDBLanguage():
    conn = 常量.conn
    preferenceTableName = 常量.preferenceTableName
    result = conn.cursor().execute('select value from %s where item = "language";' % (preferenceTableName))
    if result.fetchone() == None:
        conn.cursor().execute('''insert into %s (item, value) values ('%s', '%s');''' % (preferenceTableName, 'language', '中文'))
    else:
        print('oss 表单已存在')
    result = conn.cursor().execute('select value from %s where item = "language";' % (preferenceTableName))
    return result.fetchone()[0]

