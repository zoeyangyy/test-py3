#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import collections
from itertools import combinations
import networkx as nx
import community
import matplotlib as plt
import pickle
###########
#生成(点，点)二元组
#data输入格式为(编号，名字，属性)
#输出为(名字，属性，另一个名字)
# def to_edge(data):
    # edge_dict = collections.defaultdict(list)#defaultdict 如果这个key有值就返回list 没有就返回空list
    # for index,d in enumerate(data):
    #     li=d[2].split('#')
    #     for i in li:
    #         edge_dict[i].append(d[1])
    # edge_list = set()
    # for key, li in edge_dict.items():
    #     for l in li:
    #         if l in edge_dict.keys():
    #             if key in edge_dict[l]:
    #                 if (l,key)not in edge_list:
    #                     edge_list.add((key,l))
    #
    # return list(edge_list)
    # edge_dict = collections.defaultdict(list)  # defaultdict 如果这个key有值就返回list 没有就返回空list
    # edge_list = []
    # name_list=[]

    # for d in data:
    #     name_list.append(d[1])
    #
    # for index, d in enumerate(data):
    #     li = d[2].split('#')
    #     edge_dict[d[1]]=set(d[2])
    #     # for i in li:
    #     #     if i in name_list:
    #     #     #if l in edge_dict.keys():
    #     #         #if key in edge_dict[l]:
    #     #             #if (l, key) not in edge_list:
    #     #                 edge_list.append(( name_list.index(d[1]),name_list.index(i)))
    #
    # for key1, li1 in range(len(data)):
    #     for key2, li2 in data.items():
    #         if len(list(set(li1).intersection(set(li2))))>5:
    #             if (key1,key2) not in name_list and (key2,key1) not in name_list:
    #                 edge_list.append((name_list.index(key1), name_list.index(key2)))


def to_edge(data):
    edge_list = []
    for i in range(len(data)):
        for j in range(i, len(data)):
            set_i = set(data[i][2].split('#'))
            set_j = set(data[j][2].split('#'))
            if len(list(set_i.intersection(set_j))) > 5:
                edge_list.append((data[i][1],data[j][1]))

    return edge_list


def to_matrix(edges):
    exist = []
    for one in edges:
        for i in range(0, 2):
            if one[i] not in exist:
                exist.append(one[i])
    G = nx.Graph()
    G.add_nodes_from(exist)  # 添加节点和边
    G.add_edges_from([(u, v, {"weight": 1}) for (u, v) in edges])
    part = community.best_partition(G)
    cname = ['#FF6600', '#FFCC33', '#009966', '#0099CC', '#FF6666', '#666699']
    color = [cname[part.get(node) % 6] for node in G.nodes()]
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color=color,  node_size=[s['size'] for (n, s) in G.nodes(data=True)])
    nx.draw_networkx_edges(G, pos, width=[float(d['weight'] * 0.05) for (u, v, d) in G.edges(data=True)])
    nx.draw_networkx_labels(G, pos, font_size=8)
    nx.write_gexf(G, '111.gexf')
    plt.axis('off')


def data_from_mysql(table_name,number,name,attr):
    # 打开数据库连接
    #db = pymysql.connect("localhost", "root", "666666", "rcmd")
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Sql2056',db='rcmd',charset='utf8')
    cursor = db.cursor()# 使用 cursor() 方法创建一个游标对象 cursor
    # 使用 execute()  方法执行 SQL 查询
    sql="SELECT "+number+","+name+","+attr +" from "+table_name+" order by "+number
    print(sql)
    cursor.execute(sql )
    #data = cursor.fetchone() #使用 fetchone() 方法获取单条数据.
    # row_2 = cursor.fetchmany(3)# 获取剩余结果前3行数据
    row_3 = cursor.fetchall()# 获取剩余结果所有数据
    db.close()# 关闭数据库连接
    return row_3

table_name='user'
number='user_id'
name='name'
attr='following_id'
data=data_from_mysql(table_name,number,name,attr)
edge=to_edge(data)
# dbfile = open('user_list_following_id3', 'wb')    #必须以2进制打开文件，否则pickle无法将对象序列化只文件
# pickle.dump(edge, dbfile)
# dbfile.close()
#to_matrix(edge)
#print (type(data))
#print (node)

