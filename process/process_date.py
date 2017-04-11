# -*- coding: UTF-8 -*-
import json
import jieba
import networkx as nx
import matplotlib.pyplot as plt


# 总结类别
def generate_type():
    file = open('../data_date/0409.txt', 'r')
    f2 = open('../data_date/type.txt', 'w')

    ele = []
    for j in file.readlines():
        dic = json.loads(j)
        disease = dic['disease']
        if disease not in ele:
            ele.append(disease)
            f2.write(disease+'\n')

    file.close()
    f2.close()


def create_graph():

    G = nx.Graph()
    f2 = open('../data_date/type.txt', 'r')
    li = []
    for line in f2.readlines():
        li.append(line)
    G.add_nodes_from(li)

    f1 = open('../data_date/0409.txt', 'r')

    for line in f1.readlines():
        dic = json.loads(line)
        ele = []
        i = 0
        for sen in jieba.cut(dic['title']+dic['ques']):
            if sen in li and sen not in ele:
                ele.append(sen)
                i += 1
        if i>= 1:
            if G.get_edge_data(ele[0], ele[1]):
                G.add_weighted_edges_from([(ele[0], ele[1], G.get_edge_data(ele[0], ele[1])['weight']+1)])
            else:
                G.add_weighted_edges_from([(ele[0], ele[1], 1)])
            print(ele[0], ele[1], G.get_edge_data(ele[0], ele[1])['weight'])

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos, width=[float(d['weight']) for (u,v,d) in G.edges(data=True)])
    nx.draw_networkx_labels(G, pos)
    plt.axis('off')
    plt.show()

create_graph()