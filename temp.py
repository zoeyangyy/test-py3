# encoding: utf-8
# 一个临时的文件
import json

fr = open('./data/gastritis.txt', 'r')
fw = open('./data/gas.txt', 'w')

time = []

for line in fr.readlines():
    dic = json.loads(line)
    dic['disease'] = '胃炎'
    fw.write(json.dumps(dic, ensure_ascii=False)+'\n')

fw.close()
fr.close()
