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



def cal_rho(phi1,phi2,k):
    rho = list()
    rho.append(phi1/(1-phi2))
    rho.append((phi2*(1-phi2)+phi1*phi1)/(1-phi2))
    for i in range(2,k-1):
        rho.append(phi1*rho[i-1]+phi2*rho[i-2])
    return rho

# print(cal_rho(0.6,0.3,21))
# for i in range(len(rho_list)):
#     print(i,": ", rho_list[i])

def cal_rho3(phi1,phi2,k):
    rho = dict()
    rho['rho0'] = phi1/(1-phi2)
    rho['rho1'] = (phi2*(1-phi2)+phi1*phi1)/(1-phi2)
    for i in range(2, k-1):
        rho['rho'+str(i)] = phi1*rho['rho'+str(i-1)]+phi2*rho['rho'+str(i-2)]
    return rho

# rho_dict = cal_rho3(0.6,0.3,21)
# print(rho_dict)


def change_name():
    for dir, dirnames, filenames in os.walk('test/'):
        print(dir,dirnames,filenames)
        for name in dirnames:
            week = re.search('\d',name).group()
            os.rename(dir+name,dir+'week'+week)

# change_name()

def decor(func):
  def wrap():
    print("============")
    func()
    print("============")
  return wrap

def print_text():
  print("Hello world!")

# decorated = decor(print_text)
# decorated()

f = open('test.txt', 'r')
a = f.read()
f.close()

s = ''.join(a.split()).replace(',','，')
print(s)
