#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2018/3/31 下午2:32
# @Author      : Yiying Yang
# @File        : LR-German.py
# @Description : UCI German 语料集练习 logistic regression


import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.cross_validation import KFold
from sklearn.decomposition import PCA
from functools import reduce
import matplotlib.pyplot as plt
import random
import pickle


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
        fig = plt.figure()
        lx = fig.add_subplot(111, ylabel='loss')
        loss = []

        while itr <= 3000:
            fx = np.dot(self.w, x.T)
            hx = self.sigmoid(fx)
            t = (hx-y)
            s = []
            for i in zip(t, x):
                s.append([i[0] * i[1][j] for j in range(self.dim)])
            gradient_w = np.sum(s, 0)/row * self.eta
            self.w -= gradient_w
            print(gradient_w)
            loss.append(-(np.dot(y, np.log(hx))+np.dot((1-y), np.log(1-hx)))/row)

            if itr % 500 == 0:
                accuracy = len(list(filter(lambda x: abs(x) < 0.5, t)))/row
                print("Iter: {}  Training Accuracy: {:.4}".format(itr, accuracy))

            if reduce(lambda x, y: x & y, map(lambda x: abs(x) < 0.0001, gradient_w)):
                break
            itr += 1

        print("Feature:{}   loss:{}\n".format(self.dim-1, loss[-1]))
        lx.plot(loss)
        plt.xlabel('iter_num')
        plt.show()
        return loss[-1]

    def test(self, x, y, threshold=0.5):
        fx = np.dot(self.w, x.T)
        hx = self.sigmoid(fx)
        t = (hx-y)
        TP, FP, TN, FN, sum = 0, 0, 0, 0, 0
        for y, pred in zip(y, hx):
            sum += 1
            if y == 0 and pred <= threshold:
                TP += 1
            if y == 0 and pred > threshold:
                FN += 1
            if y == 1 and pred <= threshold:
                FP += 1
            if y == 1 and pred > threshold:
                TN += 1

        recall = TP / (TP + FN)
        precision = TP / (TP + FP)
        accuracy = (TP + TN) / sum
        F1 = 2 * precision * recall / (precision + recall)
        print(sum, TP, FN, FP, TN)
        print('=====testing result=====')
        print("precision: ", round(precision, 4))
        print("recall: ", round(recall, 4))
        print("F1: ", round(F1, 4))
        print("accuracy: ", round(accuracy, 4))

        return precision,recall,F1,accuracy


def shuffle_xy(x_mat_list, y_tag_list):
    zip_list = list(zip(x_mat_list, y_tag_list))
    random.shuffle(zip_list)
    x_mat_list[:], y_tag_list[:] = zip(*zip_list)
    return x_mat_list, y_tag_list


if __name__ == '__main__':

    with open('german.data-numeric.txt', 'r') as file:
        contents = file.readlines()
    x, y = [], []
    for line in contents:
        line = line.split()
        x.append([int(one) for one in line][:-1])
        y.append([int(one)-1 for one in line][-1])

    x = np.array(x).astype(np.float32)
    y = np.array(y)
    x, y = shuffle_xy(x, y)

    # data normalization -- min-max normalizaion performs better
    for index in range(x.shape[1]):
        # x[:, index] = (x[:, index]-np.average(x[:, index]))/np.std(x[:, index])
        x[:, index] = (x[:, index] - x[:, index].min())/(x[:, index].max()-x[:, index].min())

    # feature importance
    pca = PCA(n_components=5)
    pca.fit(x)
    print(pca.explained_variance_ratio_)

    test_result = []
    train_loss = []
    precision, recall, F1, accuracy = [],[],[],[]

    # traverse different feature sets
    for Feature in range(1, x.shape[1]+1):
        selectFeature = SelectKBest(f_regression, k=Feature)
        x_new = selectFeature.fit_transform(x, y)
        print(Feature, selectFeature.get_support(indices=True).tolist())
        x_new = np.hstack([x_new, np.ones((len(x), 1))])

        # k-fold cross-validation
        kf = KFold(len(x_new), n_folds=4, shuffle=False)
        train_loss_kf, test_result_kf = 0, 0
        for iteration, data in enumerate(kf):
            x_train, x_test, y_train, y_test = x_new[data[0]], x_new[data[1]], y[data[0]], y[data[1]]
            # Logistic regression
            lr = LR(Feature+1)
            train_loss_kf += lr.logistic_regression(x_train, y_train, eta=0.1)
            test_result_kf += lr.test(x_test, y_test)

        # test process
        x_train, x_test, y_train, y_test = x_new[:750], x_new[750:], y[:750], y[750:]
        lr = LR(Feature + 1)
        train_loss = lr.logistic_regression(x_train, y_train, eta=0.1)

        # test with different threshold
        # for i in [i/10 for i in range(1, 10)]:
        #     p,r,f,a = lr.test(x_test, y_test, i)
        #     precision.append(p)
        #     recall.append(r)
        #     F1.append(f)
        #     accuracy.append(a)

    # save data
    # with open('temp.txt', 'wb') as file:
    #     pickle.dump(train_loss, file)
    #     pickle.dump(test_result, file)

    # draw the final result
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot(precision,'red', label='precision')
    # ax.plot(recall, 'blue', label='recall')
    # ax.plot(F1, 'green', label='F1')
    # ax.plot(accuracy, 'black', label='accuracy')
    # plt.xlabel('threshold')
    # plt.xticks([i for i in range(0,9)], (str(i/10) for i in range(1,10)))
    # plt.legend()
    # plt.show()

    # compare with sklearn package
    # model = LogisticRegression()
    # model.fit(x, y)
    # print(model.score(x, y))

