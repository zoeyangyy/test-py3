#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2018/5/25 下午1:43
# @Author      : Zoe
# @File        : paparazi.py
# @Description :
import csv
import json
import collections
import numpy as np

def star():
    csv_reader = csv.reader(open('/Users/zoe/Documents/复旦课程/数据挖掘/大数据狗仔/position.csv', encoding='utf-8'))
    dic = collections.defaultdict(list)
    for row in csv_reader:
        if csv_reader.line_num == 1: continue
        dic[row[5]].append([round(float(row[3]), 2),round(float(row[4]), 2),row[2]])
    json.dump(dic, open('/Users/zoe/Library/Mobile Documents/com~apple~CloudDocs/nginx-fin/Public/data/data.json', 'w', encoding='utf8'))

def cv():
    csv_reader = csv.reader(open('/Users/zoe/Documents/复旦课程/数据挖掘/大数据狗仔/components.csv', encoding='utf-8'))
    dic = collections.defaultdict(list)
    for row in csv_reader:
        if csv_reader.line_num == 1: continue
        dic[row[2]] = list(map(lambda x:round(float(x), 2), row[3:9]))
    json.dump(dic, open('/Users/zoe/Library/Mobile Documents/com~apple~CloudDocs/nginx-fin/Application/Home/Controller/six_com.json', 'w',
                        encoding='utf8'))

def basic():
    csv_reader = csv.reader(open('/Users/zoe/Documents/复旦课程/数据挖掘/大数据狗仔/new_basic.csv', encoding='utf-8'))
    dic = collections.defaultdict(list)
    for row in csv_reader:
        if csv_reader.line_num == 1: continue
        dic[row[1]] = list(row[2:])
    json.dump(dic, open('/Users/zoe/Library/Mobile Documents/com~apple~CloudDocs/nginx-fin/Application/Home/Controller/new_basic.json', 'w',
                        encoding='utf8'))

# basic()


def color():
    with open('/Users/zoe/Documents/event_extraction/majorEventDump/1.txt', 'r') as f:
        col = f.readlines()
    colo = [i[1:8] for i in col]
    a = [colo[i] for i in np.random.randint(524, size=25)]
    print(a)