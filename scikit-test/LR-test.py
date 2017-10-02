#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2017/10/2 下午1:39
# @Author      : Zoe
# @File        : LR-test.py
# @Description : linear regression test

from sklearn import datasets
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

loaded_data = datasets.load_boston()
data_X = loaded_data.data
data_y = loaded_data.target

model = LinearRegression(normalize=True)
model.fit(data_X, data_y)

# print(model.predict(data_X[:5]))
# print(data_y[:5])
# print(model.coef_)
# print(model.intercept_)
# print(model.get_params())
# print(model.score(data_X, data_y))

# X, y = datasets.make_regression(n_samples=100, n_features=1, n_targets=1, noise=10)
# plt.scatter(X, y)
# plt.show()
