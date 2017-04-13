# encoding=utf-8
import os
import re


def count_len():
    count = 0
    for files in os.walk('./data_date/'):
        for i in files[2]:
            if re.match('0', i):
                file = open('./data_date/' + i, 'r')
                for line in file.readlines():
                    count += 1
    print(count)

count_len()
