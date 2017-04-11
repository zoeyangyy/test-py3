# encoding: utf-8
# 医生信息处理

import json

file = open('../data/diabates.txt', 'r')

dt = []
for line in file.readlines():
    dic = json.loads(line)
    if dic['dt_url'] not in dt:
        dt.append(dic['dt_url'])

print(len(dt))
