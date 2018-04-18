#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2018/4/3 下午3:15
# @Author      : Zoe
# @File        : temp.py
# @Description :

import numpy as np
import pandas as pd
import pickle

txt = np.loadtxt('german.data-numeric.txt')
txtDF = pd.DataFrame(txt)
txtDF.to_csv('data.csv', index=False)

import csv

with open('data2.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, dialect='excel')
    with open('german.data.txt', 'r') as filein:
        for line in filein:
            line_list = line.strip().split()
            spamwriter.writerow(line_list)
