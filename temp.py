# encoding=utf-8
import os
import re
import json
import time
import networkx as nx
import matplotlib.pyplot as plt


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

f = open('/Users/zoe/Documents/毕业论文/data/rawdata/2017-03-29.txt', 'r')

a = open('/Users/zoe/Documents/毕业论文/data/rawdata/2017-03.txt', 'a')

for line in f.readlines():
    a.write(line)

f.close()
a.close()