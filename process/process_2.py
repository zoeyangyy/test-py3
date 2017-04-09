# -*- coding: UTF-8 -*-
import json
import jieba
import networkx as nx
import matplotlib.pyplot as plt

# G = nx.Graph()
# li = ['冠心病', '心脏病', '高血脂', '糖尿病足', '肾病', '营养不良', '头晕', '心慌', '白内障']
# G.add_nodes_from(li)

file = open('../diabates.txt', 'r')

patient = []

for j in file.readlines():
    dic = json.loads(j)
    if dic['patient'] != '匿名':
        if dic['patient'] not in patient:
            patient.append(dic['patient'])
        else:
            print(dic['patient'])
    # ele = ['糖尿病']
    # i = 0
    # for sen in jieba.cut(dic['ques']+dic['answer']):
    #     if sen in li and sen not in ele:
    #         ele.append(sen)
    #         i += 1
    # if i >= 1:
    #     if G.get_edge_data(ele[0], ele[1]):
    #         G.add_weighted_edges_from([(ele[0], ele[1], G.get_edge_data(ele[0], ele[1])['weight']+0.1)])
    #     else:
    #         G.add_weighted_edges_from([(ele[0], ele[1], 0.1)])
    #
    # # 提到三个关键词的情况
    # if i >= 2:
    #     if G.get_edge_data(ele[0], ele[2]):
    #         G.add_weighted_edges_from([(ele[0], ele[2], G.get_edge_data(ele[0], ele[2])['weight'] + 0.1)])
    #     else:
    #         G.add_weighted_edges_from([(ele[0], ele[2], 0.1)])
    #     if G.get_edge_data(ele[1], ele[2]):
    #         G.add_weighted_edges_from([(ele[1], ele[2], G.get_edge_data(ele[1], ele[2])['weight'] + 0.1)])
    #     else:
    #         G.add_weighted_edges_from([(ele[1], ele[2], 0.1)])
    # if i>=3:
    #     print(i)

file.close()

# pos=nx.spring_layout(G)
# nx.draw_networkx_nodes(G, pos)
# nx.draw_networkx_edges(G, pos, width=[float(d['weight']*0.2) for (u, v, d) in G.edges(data=True)])
# nx.draw_networkx_labels(G, pos)
# plt.axis('off')
# plt.show()

