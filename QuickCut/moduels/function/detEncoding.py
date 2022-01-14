import chardet
from os import path

def 检测文件编码(文件路径):
    if not path.exists(文件路径):
        return False
    with open(文件路径, 'rb') as f:
        内容 = f.read()
        编码 = chardet.detect(内容)
    if 编码['encoding']:
        return 编码['encoding']
    return 'utf-8'
