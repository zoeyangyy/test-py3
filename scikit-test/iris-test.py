#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2017/10/2 下午12:31
# @Author      : Zoe
# @File        : iris-test.py
# @Description :

import numpy as np
import tensorflow as tf
from sklearn import datasets
from sklearn.model_selection import learning_curve
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import matplotlib.pyplot as plt

iris = datasets.load_iris()
digits = datasets.load_digits()
X = digits.data
y = digits.target
iris_X = iris.data
iris_y = iris.target

# print(iris_X[:2])

# # function 1
# X_train, X_test, y_train, y_test = train_test_split(iris_X, iris_y, test_size=0.3)
#
# knn = KNeighborsClassifier(n_neighbors=5)
# knn.fit(X_train, y_train)
#
# print(knn.predict(X_test))
# print(y_test)
# print(knn.score(X_test, y_test))

# # function 2
# knn = KNeighborsClassifier(n_neighbors=5)
# scores = cross_val_score(knn, iris_X, iris_y, cv=5, scoring='accuracy')
# print(scores.mean())

# function 3
# k_range = range(1,31)
# k_scores = []
# for k in k_range:
#     knn = KNeighborsClassifier(n_neighbors=k)
#     scores = cross_val_score(knn, iris_X, iris_y, cv=10, scoring='accuracy')
#     # when regression
#     # loss = -cross_val_score(knn, iris_X, iris_y, cv=10, scoring='mean_squared_error')
#     k_scores.append(scores.mean())
#
# plt.plot(k_range, k_scores)
# plt.xlabel('value of k')
# plt.show()

# with tf.Session() as sess:
#     correct_prediction = tf.equal(knn.predict(X_test), y_test)
#     accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
#     print(sess.run(accuracy))


def overfit():
    global X, y
    train_sizes, train_loss, test_loss = learning_curve(
        SVC(gamma=0.001), X, y, cv=10, scoring='neg_mean_squared_error',
        train_sizes=[0.1,0.25,0.5,0.75,1]
    )
    train_loss_mean = -np.mean(train_loss, axis=1)
    test_loss_mean = -np.mean(test_loss, axis=1)

    plt.plot(train_sizes, train_loss_mean, 'o-', color='r', label='training')
    plt.plot(train_sizes, test_loss_mean, 'o-', color='g', label='cross-validation')
    plt.legend(loc='best')
    plt.show()

overfit()