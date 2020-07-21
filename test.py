import datetime

print(datetime.datetime.now())  # 2019-01-28 11:09:01.529864
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))  # 2019-01-28 11:09:01.529864
print(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))  # 20190128110901529864
