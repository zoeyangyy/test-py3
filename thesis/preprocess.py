#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2018/5/21 下午3:48
# @Author      : Zoe
# @File        : preprocess.py
# @Description :

file = open('/Users/zoe/Documents/复旦课程/毕业论文/开题/STK_MA_TRADINGMAIN.txt', 'r', encoding='GB18030' ,errors='ignore')
contents = file.readlines()
print(len(contents))
file.close()

print(contents[:5])