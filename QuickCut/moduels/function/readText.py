"""
为了避免文本文件的编码问题，在读取小文本文件时
先用二进制读取，再检测下编码
解码后反回文本
"""

import chardet
from os import path

def 读取文本(文件路径):
    if not path.exists(文件路径):
        return False
    with open(文件路径, 'rb') as f:
        内容 = f.read()
    编码 = chardet.detect(内容)
    编码 = 编码['encoding'] if 编码['encoding'] else 'utf-8'
    return 内容.decode(编码)
