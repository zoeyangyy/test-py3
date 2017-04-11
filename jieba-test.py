# encoding=utf-8
import jieba
import json
import os
# demo
# seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# print("Full Mode:", "/ ".join(seg_list))  # 全模式
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# print("Default Mode:", "/ ".join(seg_list))  # 精确模式
#
# seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
# print(", ".join(seg_list))
#
# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
# print(", ".join(seg_list))

# rfile = open('/Users/zoe/Documents/remotefile2/readyforWV.txt', 'r')
# wfile = open('/Users/zoe/Documents/remotefile2/disease-cut.txt', 'w')

wfile = open('jieba-cut.txt', 'w')
f_list = []

for files in os.walk('./data/'):
    for i in files[2]:
        f_list.append(i)

for i in range(len(f_list)):
    rfile = open('./data/'+str(f_list[i]), 'r')
    for line in rfile.readlines():
        dic = json.loads(line)
        wfile.write(" ".join(jieba.cut(dic['ques']+dic['answer']))+'\n')
    rfile.close()

wfile.close()
