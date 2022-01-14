from moduels.component.NormalValue import 常量

def 从DB获取语言():
    conn = 常量.conn
    首选项表名 = 常量.首选项表名
    result = conn.cursor().execute('select value from %s where item = "language";' % (首选项表名))
    if result.fetchone() == None:
        conn.cursor().execute('''insert into %s (item, value) values ('%s', '%s');''' % (首选项表名, 'language', '中文'))
    else:
        ...
        # print('oss 表单已存在')
    result = conn.cursor().execute('select value from %s where item = "language";' % (首选项表名))
    return result.fetchone()[0]

