
def checkDBLanguage():
    result = conn.cursor().execute('select value from %s where item = "language";' % (preferenceTableName))
    if result.fetchone() == None:
        conn.cursor().execute('''insert into %s (item, value) values ('%s', '%s');''' % (preferenceTableName, 'language', '中文'))
    else:
        print('oss 表单已存在')
    result = conn.cursor().execute('select value from %s where item = "language";' % (preferenceTableName))
    return result.fetchone()[0]

