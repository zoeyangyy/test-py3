# -*- coding: UTF-8 -*-
import json
import jieba
import os
import re
import networkx as nx
import matplotlib.pyplot as plt


# 总结类别
def generate_type():
    f2 = open('../data_date/type.txt', 'w')
    ele = []
    for files in os.walk('../data_date/'):
        for i in files[2]:
            if re.match('0', i):
                file = open('../data_date/'+i, 'r')
                for j in file.readlines():
                    dic = json.loads(j)
                    disease = dic['disease']
                    if disease not in ele:
                        ele.append(disease)
                        f2.write(disease+'\n')
                file.close()
    f2.close()


# 导入jieba词库，需要词频数据，暂时都写成1
def generate_dic():
    f1 = open('../data_date/type.txt', 'r')
    f2 = open('../data_date/dic.txt', 'w')
    for line in f1.readlines():
        new = line.strip() + ' 1'
        f2.write(new + '\n')
    f1.close()
    f2.close()


# 第一种画图方法
def create_graph():
    jieba.load_userdict('../data_date/dic.txt')
    G = nx.Graph()
    f2 = open('../data_date/type.txt', 'r')
    # 所有疾病列表
    li = []
    for line in f2.readlines():
        li.append(line.strip())
    G.add_nodes_from(li)
    f2.close()
    # 存在边的节点
    # exist = []

    for files in os.walk('../data_date/'):
        for i in files[2]:
            if re.match('0', i):
                f1 = open('../data_date/'+i, 'r')
                for line in f1.readlines():
                    dic = json.loads(line)
                    ele = []
                    i = 0
                    for sen in jieba.cut(dic['title']+dic['ques']):
                        if (sen in li) and (sen not in ele):
                            ele.append(sen)
                            i += 1
                    if i >= 2:
                        # if ele[0] not in exist:
                        #     exist.append(ele[0])
                        # if ele[1] not in exist:
                        #     exist.append(ele[1])
                        if G.get_edge_data(ele[0], ele[1]):
                            G.add_weighted_edges_from([(ele[0], ele[1], G.get_edge_data(ele[0], ele[1])['weight']+1)])
                        else:
                            G.add_weighted_edges_from([(ele[0], ele[1], 1)])
                        # print(ele[0], ele[1], G.get_edge_data(ele[0], ele[1])['weight'])
                f1.close()

    # - circular_layout：节点在一个圆环上均匀分布
    # - random_layout：节点随机分布
    # - shell_layout：节点在同心圆上分布
    # - spring_layout：用Fruchterman-Reingold算法排列节点

    exist = []
    pair = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 3]
    for one in pair:
        if one[0] not in exist:
            exist.append(one[0])
        if one[1] not in exist:
            exist.append(one[1])

    for ele in li:
        if ele not in exist:
            G.remove_node(ele)

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=100)
    nx.draw_networkx_edges(G, pos, width=[float(d['weight'] * 0.2) for (u, v, d) in G.edges(data=True)])
    nx.draw_networkx_labels(G, pos, font_size=8)
    # print(G.neighbors('头痛'))
    plt.axis('off')
    plt.show()


# 遍历文件，储存关系数据
def create_data():
    jieba.load_userdict('../data_date/dic.txt')
    f2 = open('../data_date/type.txt', 'r')
    # 所有疾病列表
    li = []
    for line in f2.readlines():
        li.append(line.strip())
    f2.close()

    f3 = open('../data_date/data.txt', 'w')

    edges = {}
    for files in os.walk('../data_date/'):
        for i in files[2]:
            if re.match('0', i):
                f1 = open('../data_date/' + i, 'r')
                for line in f1.readlines():
                    dic = json.loads(line)
                    ele = []
                    i = 0
                    for sen in jieba.cut(dic['title'] + dic['ques']):
                        if (sen in li) and (sen not in ele):
                            ele.append(sen)
                            i += 1
                    if i >= 2:
                        if (ele[0], ele[1]) in edges:
                            edges[(ele[0], ele[1])] += 1
                        else:
                            edges[(ele[0], ele[1])] = 1
                f1.close()

    for (u, v) in edges:
        f3.write(u+" "+v+" "+str(edges[(u, v)])+"\n")

    f3.close()


# 第二种画图，性能更好
def create_graph2():
    f1 = open('../data_date/data.txt', 'r')
    edges = {}
    for line in f1.readlines():
        li = line.split()
        if (li[1], li[0]) in edges:
            edges[(li[1], li[0])] += int(li[2])
        else:
            edges[(li[0], li[1])] = int(li[2])

    # - circular_layout：节点在一个圆环上均匀分布
    # - random_layout：节点随机分布
    # - shell_layout：节点在同心圆上分布
    # - spring_layout：用Fruchterman-Reingold算法排列节点

    exist = []
    pair = [(u, v, {"weight": edges[(u, v)]}) for (u, v) in edges if edges[(u, v)] > 3]
    for one in pair:
        for i in range(0, 2):
            if one[i] not in exist:
                exist.append(one[i])

    G = nx.Graph()
    G.add_nodes_from(exist)
    G.add_edges_from(pair)
    for node in exist:
        size = 0
        for neigh in G.neighbors(node):
            if (node, neigh) in edges:
                size += edges[(node, neigh)]
            else:
                size += edges[(neigh, node)]
        G.node[node]['size'] = size

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos,  node_size=[s['size']*10 for (n, s) in G.nodes(data=True)])
    nx.draw_networkx_edges(G, pos, width=[float(d['weight'] * 0.2) for (u, v, d) in G.edges(data=True)])
    nx.draw_networkx_labels(G, pos, font_size=8)
    # print(G.neighbors('头痛'))
    plt.axis('off')
    plt.show()


create_graph2()
