# encoding=utf-8
import os
import re
import json
import sys,getopt
import matplotlib.pyplot as plt
import numpy as np


def count_len():
    count = 0
    for files in os.walk('./data_date/'):
        for i in files[2]:
            if re.match('0', i):
                file = open('./data_date/' + i, 'r')
                for line in file.readlines():
                    count += 1
    print(count)


def try_color():
    G = nx.Graph()
    # coli = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
    node = ['lightcoral', 'brown', '#81c2d6', 'r', 'firebrick', 'sienna', 'salmon', 'lightsalmon']
    coli = [i for i in range(0, 14)]
    G.add_nodes_from(node)

    # mod = community.modularity(part, G)
    # print("modularity:", mod)

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color=node)
    nx.draw_networkx_labels(G, pos, font_size=8)
    # print(G.neighbors('头痛'))
    plt.axis('off')
    plt.show()


def count_date():
    f = open('/Users/zoe/Documents/毕业论文/data/rawdata/2016-04.txt', 'r')
    contents = f.readlines()

    all_count = 0
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    i5 = 0
    i6 = 0
    i7 = 0
    i8 = 0
    i9 = 0
    i10 = 0
    i11 = 0
    i12 = 0
    i13 = 0
    i14 = 0
    i15 = 0
    i16 = 0
    i17 = 0
    i18 = 0
    i19 = 0
    i20 = 0
    i21 = 0
    i22 = 0
    i23 = 0
    i24 = 0
    i25 = 0
    i26 = 0
    i27 = 0
    i28 = 0
    i29 = 0
    i30 = 0
    for line in contents:
        all_count += 1
        dic = json.loads(line)
        time = dic['time'][0:10]
        if time == '2016-04-01':
            i1 += 1
        if time == '2016-04-02':
            i2 += 1
        if time == '2016-04-03':
            i3 += 1
        if time == '2016-04-04':
            i4 += 1
        if time == '2016-04-05':
            i5 += 1
        if time == '2016-04-06':
            i6 += 1
        if time == '2016-04-07':
            i7 += 1
        if time == '2016-04-08':
            i8 += 1
        if time == '2016-04-09':
            i9 += 1
        if time == '2016-04-10':
            i10 += 1
        if time == '2016-04-11':
            i11 += 1
        if time == '2016-04-12':
            i12 += 1
        if time == '2016-04-13':
            i13 += 1
        if time == '2016-04-14':
            i14 += 1
        if time == '2016-04-15':
            i15 += 1
        if time == '2016-04-16':
            i16 += 1
        if time == '2016-04-17':
            i17 += 1
        if time == '2016-04-18':
            i18 += 1
        if time == '2016-04-19':
            i19 += 1
        if time == '2016-04-20':
            i20 += 1
        if time == '2016-04-21':
            i21 += 1
        if time == '2016-04-22':
            i22 += 1
        if time == '2016-04-23':
            i23 += 1
        if time == '2016-04-24':
            i24 += 1
        if time == '2016-04-25':
            i25 += 1
        if time == '2016-04-26':
            i26 += 1
        if time == '2016-04-27':
            i27 += 1
        if time == '2016-04-28':
            i28 += 1
        if time == '2016-04-29':
            i29 += 1
        if time == '2016-04-30':
            i30 += 1

    print(i1)
    print(i2)
    print(i3)
    print(i4)
    print(i5)
    print(i6)
    print(i7)
    print(i8)
    print(i9)
    print(i10)
    print(i11)
    print(i12)
    print(i13)
    print(i14)
    print(i15)
    print(i16)
    print(i17)
    print(i18)
    print(i19)
    print(i20)
    print(i21)
    print(i22)
    print(i23)
    print(i24)
    print(i25)
    print(i26)
    print(i27)
    print(i28)
    print(i29)
    print(i30)
    f.close()


def chazhao():
    f = open('/Users/zoe/Documents/毕业论文/data/rawdata/2016-04.txt','r')

    for line in f.readlines():
        dic = json.loads(line)
        if re.findall("视网膜", dic['ques']):
            print(dic)

    f.close()


def draw():
    x = np.arange(0.01,1,0.01)
    y = -x*np.log2(x)
    plt.plot(x,y)
    plt.show()

draw()