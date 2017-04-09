# encoding: utf-8
# 一个临时的文件
import json

fr = open('hypertension.txt', 'r')

time = []

for line in fr.readlines():
    dic = json.loads(line)
    if dic['time'] not in time:
        time.append(dic['time'])
    else:
        print(dic['time'])

fr.close()
