#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2017/10/22 下午6:52
# @Author      : Zoe
# @File        : gender_classification.py
# @Description : 性别分类测试

import nltk
from nltk.corpus import names
import random

# print([name for name in names.words('male.txt')])

# 特征提取器函数
def gender_features(word):
    return  {'last_letter':word[-1]}

# 准备数据
labeled_names = ([(name,'male') for name in names.words('male.txt')]+
                 [(name, 'female') for name in names.words('female.txt')])
random.shuffle(labeled_names)

# 调用特征提取器函数，得到数据特征集
featuresets = [(gender_features(n), gender) for (n, gender) in labeled_names]

# 将数据划分训练集与测试集，训练朴素贝叶斯分类器
train_set, test_set = featuresets[500:], featuresets[:500]
classifier = nltk.NaiveBayesClassifier.train(train_set)

# 测试"Neo"为男名还是女名
print(classifier.classify(gender_features('Neo')))
# 计算分类准确率
print(nltk.classify.accuracy(classifier, test_set))
# 显示信息量最大的前五个特征
print(classifier.show_most_informative_features(5))
