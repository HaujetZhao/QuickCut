
def strTimeToSecondsTime(inputTime):
    if re.match(r'.+\.\d+', inputTime):
        pass
    else:  # 如果没有小数点，就加上小数点
        inputTime = inputTime + '.0'

    if re.match(r'\d+:\d+:\d+\.\d+', inputTime):
        temp = re.findall('\d+', inputTime)
        return float(temp[0]) * 3600 + float(temp[1]) * 60 + float(temp[2]) + float('0.' + temp[3])
    elif re.match(r'\d+:\d+\.\d+', inputTime):
        temp = re.findall('\d+', inputTime)
        return float(temp[0]) * 60 + float(temp[1]) + float('0.' + temp[2])
    elif re.match(r'\d+\.\d+', inputTime):
        temp = re.findall('\d+', inputTime)
        return float(temp[0]) + float('0.' + temp[1])
    elif re.match(r'\d+', inputTime):
        temp = re.findall('\d+', inputTime)
        return float(temp[0])
    else:
        return float(0)
