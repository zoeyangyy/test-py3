# encoding=utf-8
import os
import re
import json
import sys,getopt
import matplotlib.pyplot as plt
import numpy as np
from numpy import *
from functools import reduce
import tensorflow as tf
import time


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


def np_matmul():
    x = np.array([1,2,3,4,5,6]).reshape([2,3])
    y = np.array([1,2,3]).reshape([3,1])
    z = np.array([1,2]).reshape([2,1])

    print(np.dot(x,y))
    print(np.matmul(x,y))

    # z扩展成维度一样的
    print(x*z)
    print(np.multiply(x,z))


class LR:
    def __init__(self, dim):
        self.dim = dim
        # self.w = np.random.random(self.dim)
        self.w = np.zeros(self.dim)
        self.eta = 0.2

    def sigmoid(self, x):
        return 1.0/(1+np.exp(-x))

    def logistic_regression(self,x,y,eta):
        itr = 0
        self.eta = eta
        row, column = np.shape(x)

        while itr <= 5000:
            fx = np.dot(self.w, x.T)
            hx = self.sigmoid(fx)
            t = (hx-y)
            s = []
            for i in zip(t, x):
                s.append([i[0] * i[1][j] for j in range(self.dim)])
            gradient_w = np.sum(s, 0)/row * self.eta
            self.w -= gradient_w

            if itr % 500 == 0:
                accuracy = len(list(filter(lambda x: abs(x) < 0.5, t)))/row
                loss = -(np.dot(y, np.log(hx))+np.dot((1-y), np.log(1-hx)))/row
                print("Iter: {}  Training Accuracy: {:.4}  Loss : {:.4}".format(itr, accuracy, loss))

            # Break if gradient stop descenting
            if reduce(lambda x, y: x & y, map(lambda x: abs(x) < 0.0001, gradient_w)):
                break
            itr += 1

        return self.w

a = np.linspace(1,10,10).reshape(10,1)
b = np.linspace(50,59,10).reshape(10,1)
c = (1.0*(b>3))
# print(np.dot(a, b)*c.T)
print(a)
print(a+b)

