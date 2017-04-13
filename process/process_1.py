# -*- coding: UTF-8 -*-
import json
import jieba
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
li = ['冠心病', '心脏病', '高血脂', '糖尿病足', '肾病', '营养不良', '头晕', '心慌', '白内障']
p = [100, 100, 200, 300, 100, 100, 300, 200, 200]
G.add_nodes_from(li, size=200)
G.add_node('糖尿病', size=200)

file = open('../data/diabetes.txt', 'r')

for j in file.readlines():
    dic = json.loads(j)

    # 同一个病人的提问，需要归并吗
    # if dic['patient'] != '匿名':
    #     if dic['patient'] not in patient:
    #         patient.append(dic['patient'])
    #     else:
    #         print(dic['patient'])

    ele = ['糖尿病']
    i = 0
    for sen in jieba.cut(dic['ques']):
        if sen in li and sen not in ele:
            ele.append(sen)
            i += 1
    if i >= 1:
        if G.get_edge_data(ele[0], ele[1]):
            G.add_weighted_edges_from([(ele[0], ele[1], G.get_edge_data(ele[0], ele[1])['weight']+1)])
        else:
            G.add_weighted_edges_from([(ele[0], ele[1], 1)])
        # print(ele[0], ele[1], G.get_edge_data(ele[0], ele[1])['weight'])

file.close()

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

G.add_node("a")
G.node["a"]['size'] = 800
a = [s['size'] for (n, s) in G.nodes(data=True)]


pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=[s['size'] for (n, s) in G.nodes(data=True)])
nx.draw_networkx_edges(G, pos, width=[float(d['weight']*0.2) for (u, v, d) in G.edges(data=True)])
nx.draw_networkx_labels(G, pos)
plt.axis('off')
plt.show()

