# encoding=utf8
import json
import jieba
import time
import re
import os
import networkx as nx
import matplotlib.pyplot as plt
import community


# 去重
def redundancy():
    start = time.clock()
    f = open('/Users/zoe/Documents/毕业论文/data/rawdata/2016-04-26.txt', 'r')
    contents = f.readlines()
    f.close()

    f = open('/Users/zoe/Documents/毕业论文/data/rawdata/2016-04-26.txt', 'w')
    s = set()
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
    f.close()

    end = time.clock()
    print(str(all_count)+" "+str(avail_count)+" cost:%fs" % (end - start))

# redundancy()


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


# 集合收集的疾病库，生成自定义词库，共582种疾病
def self_dic():
    # f2 = open('../data_date/疾病.txt', 'a+')
    # f3 = open('../data_date/disease.txt', 'r')
    #
    # disease = []
    # for line in f2.readlines():
    #     if line.strip() not in disease:
    #         disease.append(line.strip())
    #
    # for line in f3.readlines():
    #     if line.strip() not in disease:
    #         f2.write(line)
    #         disease.append(line.strip())
    # f3.close()
    # f2.close()

    f1 = open('../data_date/dic.txt', 'w')
    f2 = open('../data_date/疾病.txt', 'r')
    for line in f2.readlines():
        f1.write(line.strip() + ' 1\n')

    f1.close()
    f2.close()


# self_dic()


# 加入自定义词库，分词，去除停用词，提取疾病
def fenci():
    jieba.load_userdict('../data_date/dic.txt')
    stopwords = set([line.strip() for line in open('../data_date/stopwords.txt').readlines()])

    f2 = open('../data_date/疾病.txt', 'r')
    # 所有疾病列表
    li = set()
    for line in f2.readlines():
        li.add(line.strip())
    f2.close()

    for files in os.walk('/Users/zoe/Documents/毕业论文/data/rawdata/'):
        for i in files[2]:
            if re.match('2016', i):
                start = time.clock()
                f = open('/Users/zoe/Documents/毕业论文/data/rawdata/'+i, 'r')
                contents = f.readlines()
                f.close()

                f = open('/Users/zoe/Documents/毕业论文/data/simdata2/'+i, 'w')
                count = 0
                for line in contents:
                    dic = json.loads(line)
                    ele = []
                    words = set(jieba.cut(dic['ques']))
                    for sen in words-stopwords:
                        if (sen in li) and (sen not in ele):
                            ele.append(sen)

                    if len(ele) > 1:
                        dic_new = dict()
                        dic_new['depart'] = dic['depart']
                        dic_new['gender'] = dic['gender']
                        dic_new['age'] = dic['age']
                        dic_new['time'] = dic['time']
                        dic_new['dis'] = ele
                        f.write(json.dumps(dic_new, ensure_ascii=False)+'\n')
                        count += 1

                f.close()
                end = time.clock()
                print(str(count)+' %f' % (end-start))

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


# 数据提取
def create_data(attr):
    edges = {}
    i2 = 0
    i3 = 0
    i4 = 0
    for files in os.walk('/Users/zoe/Documents/毕业论文/data/simdata2/'):
        for i in files[2]:
            if re.match('201', i):
                f = open('/Users/zoe/Documents/毕业论文/data/simdata2/'+i, 'r')
                contents = f.readlines()
                f.close()
                for line in contents:
                    dic = json.loads(line)
                    # if dic['gender'] == '女':
                    try:
                        s = re.findall('\d+', dic['age'])[0]
                    except:
                        s = 0
                    finally:
                        if 0 < int(s) <= 10:
                            ele = dic['dis']
                            if len(ele) == 2:
                                edges = add_edge(edges, ele[0], ele[1])
                                i2 += 1
                            if len(ele) == 3:
                                edges = add_edge(edges, ele[0], ele[1])
                                edges = add_edge(edges, ele[1], ele[2])
                                edges = add_edge(edges, ele[2], ele[0])
                                i3 += 1
                            if len(ele) >= 4:
                                i4 += 1
                            # if len(ele) >= 7:
                                # print(line)
    print(i2)
    print(i3)
    print(i4)
    f3 = open('/Users/zoe/Documents/毕业论文/data/gephidata/'+attr+'.txt', 'w')
    for (u, v) in edges:
        f3.write(u + " " + v + " " + str(edges[(u, v)]) + "\n")
    f3.close()

create_data('age0-10')


def modify_data(attr, number):
    f1 = open('/Users/zoe/Documents/毕业论文/data/gephidata/total.txt', 'r')
    edges = {}
    contents = f1.readlines()
    for line in contents:
        li = line.split()
        edges[(li[0], li[1])] = int(li[2])
    f1.close()

    f2 = open('/Users/zoe/Documents/毕业论文/data/gephidata/'+attr+'.txt', 'r')
    edges2 = {}
    contents2 = f2.readlines()
    for line in contents2:
        li = line.split()
        if (li[0], li[1]) in edges:
            edges2[(li[0], li[1])] = int(li[2]) - number/179831 * edges[(li[0], li[1])]
        elif (li[1], li[0]) in edges:
            edges2[(li[1], li[0])] = int(li[2]) - number/179831 * edges[(li[1], li[0])]
        else:
            edges2[(li[0], li[1])] = int(li[2])
    f2.close()

    f3 = open('/Users/zoe/Documents/毕业论文/data/gephidata/' + attr + '.txt', 'w')
    for (u, v) in edges2:
        if edges2[(u, v)] > 0:
            f3.write(u + " " + v + " " + str(edges2[(u, v)]) + "\n")
    f3.close()


# modify_data('spring', 37461)
# modify_data('summer', 53963)
# modify_data('autumn', 68804)
# modify_data('winter', 55165)


# 运用networkx生成复杂网络
def create_graph_2(attr):
    f1 = open('/Users/zoe/Documents/毕业论文/data/gephidata/'+attr+'.txt', 'r')
    edges = {}
    min_edge = 30   # 提取权值在50以上的边
    for line in f1.readlines():
        li = line.split()
        if float(li[2]) > min_edge:
            edges[(li[0], li[1])] = float(li[2])
    exist = []
    for one in edges:
        for i in range(0, 2):
            if one[i] not in exist:
                exist.append(one[i])

    G = nx.Graph()
    G.add_nodes_from(exist)  # 添加节点和边
    G.add_edges_from([(u, v, {"weight": edges[(u, v)]}) for (u, v) in edges])
    max_edge = max([edges[(u, v)] for (u, v) in edges])
    for (u, v) in edges:
        edges[(u, v)] = min_edge + (100-min_edge)*(edges[(u, v)]-min_edge)/(max_edge-min_edge)
    for node in exist:
        size = 0
        for neigh in G.neighbors(node):
            if (node, neigh) in edges:
                size += edges[(node, neigh)]
            else:
                size += edges[(neigh, node)]
        G.node[node]['size'] = size

    part = community.best_partition(G)
    cname = ['#FF6600', '#FFCC33', '#009966', '#0099CC', '#FF6666', '#666699']
    color = [cname[part.get(node) % 6] for node in G.nodes()]
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color=color,  node_size=[s['size'] for (n, s) in G.nodes(data=True)])
    nx.draw_networkx_edges(G, pos, width=[float(d['weight'] * 0.05) for (u, v, d) in G.edges(data=True)])
    nx.draw_networkx_labels(G, pos, font_size=8)
    nx.write_gexf(G, '/Users/zoe/Documents/毕业论文/data/gephidata/'+attr+'.gexf')
    plt.axis('off')
    plt.show()

create_graph_2('age0-10')
# create_graph_2('age7-17')
# create_graph_2('age41-65')
# create_graph_2('age60-')
#
# create_graph_2('female')
# create_graph_2('male')
#
# create_graph_2('spring')
# create_graph_2('summer')
# create_graph_2('autumn')
# create_graph_2('winter')

# create_graph_2('total')
# create_graph_2('2017-new')
