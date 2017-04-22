# encoding=utf8
import json
import jieba
import time
import re
import networkx as nx
import matplotlib.pyplot as plt
import community


# 去重
def quchong():
    start = time.clock()
    f = open('/Users/zoe/Documents/毕业论文/data/rawdata/2016-06.txt', 'r', encoding='gbk')
    contents = f.readlines()
    f.close()

    f = open('/Users/zoe/Documents/毕业论文/data/rawdata/2016-06.txt', 'w')
    s = {'0'}
    all_count = 0
    avail_count = 0
    for line in contents:
        all_count += 1
        dic = json.loads(line)
        ques = dic['ques']
        if ques not in s:
            avail_count += 1
            s.add(ques)
            f.write(line)

    print(all_count)
    print(avail_count)
    f.close()

    end = time.clock()
    print("cost: %f s" % (end - start))

# quchong()


# 提取出现的科室及疾病
def depart_disease():
    f = open('/Users/zoe/Documents/毕业论文/data/rawdata/2016-07.txt', 'r', encoding='gbk')
    f2 = open('../data_date/depart.txt', 'w')
    f3 = open('../data_date/disease.txt', 'w')
    depart = []
    disease = []

    for line in f.readlines():
        dic = json.loads(line)
        if dic['depart'] and dic['depart'] not in depart:
            depart.append(dic['depart'])
            f2.write(dic['depart'] + '\n')
        if dic['disease'] and dic['disease'] not in disease:
            disease.append(dic['disease'])
            f3.write(dic['disease'] + '\n')

    f.close()
    f2.close()
    f3.close()

# depart_disease()


# 集合收集的疾病库，生成自定义词库
def self_dic():
    f1 = open('../data_date/dic.txt', 'w')
    f2 = open('../data_date/疾病.txt', 'r')

    disease = []

    for line in f2.readlines():
        if line.strip() not in disease:
            disease.append(line.strip())
            f1.write(line.strip() + ' 1\n')

    f1.close()
    f2.close()


# self_dic()


# 加入自定义词库，分词，5分钟
def fenci():
    start = time.clock()
    jieba.load_userdict('../data_date/dic.txt')

    f = open('/Users/zoe/Documents/毕业论文/data/rawdata/2016-07.txt', 'r', encoding='gbk')
    contents = f.readlines()
    f.close()

    f2 = open('../data_date/disease.txt', 'r')
    # 所有疾病列表
    li = []
    for line in f2.readlines():
        li.append(line.strip())
    f2.close()

    li = set(li)

    mid = time.clock()
    print('%f' % (mid-start))
    f = open('../data/2016-07.txt', 'w')
    i = 0
    for line in contents:
        dic = json.loads(line)
        ele = []
        for sen in jieba.cut(dic['disease']+dic['ques']+dic['answer']):
            if (sen in li) and (sen not in ele):
                ele.append(sen)

        if len(ele) > 1:
            dic_new = {}
            dic_new['depart'] = dic['depart']
            dic_new['gender'] = dic['gender']
            dic_new['age'] = dic['age']
            dic_new['time'] = dic['time']
            dic_new['ques'] = ele
            f.write(json.dumps(dic_new, ensure_ascii=False)+'\n')
            i += 1

    print(i)
    f.close()
    end = time.clock()
    print('%f' % (end-start))
# fenci()


# 添加边
def add_edge(edges, ele1, ele2):
    if (ele1, ele2) in edges:
        edges[(ele1, ele2)] += 1
    elif (ele2, ele1) in edges:
        edges[(ele2, ele1)] += 1
    else:
        edges[(ele1, ele2)] = 1
    return edges


# 生成需要的数据
def create_data():
    f = open('../data/2016-07.txt', 'r')

    i2 = 0
    i3 = 0
    i4 = 0
    i5 = 0
    i6 = 0
    i7 = 0
    edges = {}
    for line in f.readlines():
        dic = json.loads(line)
        # if dic['disease']:
        #     ele = [dic['disease']]+dic['ques']
        # else:

        # if dic['age']:
        #     age = dic['age']
        #     try:
        #         s = re.findall('\d+', age)[0]
        #     except:
        #         s = 0
        #     finally:
        #         if 66 < int(s):

        if dic['depart'] == '皮肤科':
            ele = dic['ques']
            if len(ele) == 2:
                edges = add_edge(edges, ele[0], ele[1])
                i2 += 1
            if len(ele) == 3:
                edges = add_edge(edges, ele[0], ele[1])
                edges = add_edge(edges, ele[1], ele[2])
                edges = add_edge(edges, ele[2], ele[0])
                i3 += 1
            if len(ele) == 4:
                i4 += 1
            if len(ele) == 5:
                i5 += 1
            if len(ele) == 6:
                i6 += 1
            if len(ele) >= 7:
                i7 += 1

    f.close()
    print(i2)
    print(i3)
    print(i4)
    print(i5)
    print(i6)
    print(i7)

    f3 = open('../data_date/data.txt', 'w')
    for (u, v) in edges:
        f3.write(u + " " + v + " " + str(edges[(u, v)]) + "\n")

    f3.close()

create_data()


# 第二种画图，性能更，用data.txt
def create_graph_2():
    f1 = open('../data_date/data.txt', 'r')
    edges = {}
    for line in f1.readlines():
        li = line.split()
        edges[(li[0], li[1])] = int(li[2])

    exist = []

    min = 20

    pair = [(u, v, {"weight": edges[(u, v)]}) for (u, v) in edges if edges[(u, v)] > min]
    for one in pair:
        for i in range(0, 2):
            if one[i] not in exist:
                exist.append(one[i])

    G = nx.Graph()
    G.add_nodes_from(exist)
    G.add_edges_from(pair)

    max = 0
    for (u, v) in edges:
        if edges[(u, v)] > max:
            max = edges[(u, v)]

    for (u, v) in edges:
        edges[(u, v)] = min + (100-min)*(edges[(u, v)]-min)/(max-min)

    for node in exist:
        size = 0
        for neigh in G.neighbors(node):
            if (node, neigh) in edges:
                size += edges[(node, neigh)]
            else:
                size += edges[(neigh, node)]
        G.node[node]['size'] = size

    part = community.best_partition(G)

    # 有多少社群
    # print(len(set(part.values())))

    cname = ['#FF6600', '#FFCC33', '#009966', '#0099CC', '#FF6666', '#666699']
    color = [cname[part.get(node) % 6] for node in G.nodes()]

    # mod = community.modularity(part, G)
    # print("modularity:", mod)

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color=color,  node_size=[s['size'] for (n, s) in G.nodes(data=True)])
    nx.draw_networkx_edges(G, pos, width=[float(d['weight'] * 0.05) for (u, v, d) in G.edges(data=True)])
    nx.draw_networkx_labels(G, pos, font_size=8)
    # print(G.neighbors('头痛'))
    plt.axis('off')
    plt.show()

create_graph_2()


# 为gephi提供数据用
def create_graph_3():
    print()
