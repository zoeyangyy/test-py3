#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2018/4/1 下午6:18
# @Author      : Zoe
# @File        : relu.py
# @Description : http://neuralnetworksanddeeplearning.com/chap4.html
#
# 理论和实验证明，一个两层的ReLU网络可以模拟任何函数[1~5]。请自行定义一个函数​, 并使用基于ReLU的神经网络来拟合此函数。
#
# 请自行在函数上采样生成训练集和测试集，使用训练集来训练神经网络，使用测试集来验证拟合效果。
#
# 可以使用深度学习框架来编写模型，如tensorflow、pytorch、keras等。如果不使用上述框架，直接用NumPy实现可以最高加5分的附加分。
#
# 提交时请一并提交代码和报告。代码建议注释清楚（5分）报告至少应包含以下部分：（5分）函数定义、数据采集、模型描述、拟合效果。
#
# [1] G. Cybenko. 1989. Approximation by superpositions of a sigmoidal function.
# [2] K. Hornik, M. Stinchcombe, and H. White. 1989. Multilayer feedforward networks are universal approximators.
# [3] Moshe Leshno, et al. 1993. Multilayer feedforward networks with a nonpolynomial activation function can approximate any function
# [4] Vinod Nair and Geoffrey E. Hinton. 2010. Rectified linear units improve restricted boltzmann machines.
# [5] Xavier Glorot, Antoine Bordes, Yoshua Bengio. 2011. Deep Sparse Rectifier Neural Networks. PMLR 15:315-323.

import tensorflow as tf
import numpy as np
from numpy import *
import matplotlib.pyplot as plt


def approximate_relu():
    x_Number = 100
    hidden_Size = 100
    learning_rate = 0.1
    training_iters = 50000
    random.seed(5)

    #构造输入数据
    x_data = np.linspace(0.0, 1.0, num=x_Number).astype('float32').reshape([x_Number, 1])
    #y可以是下述各种
    y_data = 0.2+0.4*x_data**2+0.3*x_data*sin(15*x_data)+0.05*cos(50*x_data)
    # y_data = 0.2+0.3*x_data+0.4*x_data**2
    # y_data = 3*x_data+1

    #隐层
    W1 = tf.Variable(tf.random_uniform((1, hidden_Size), minval=-sqrt(6/(1+hidden_Size)), maxval=sqrt(6/(1+hidden_Size))))
    # W1 = tf.get_variable(name="weights1", shape=[1, hidden_Size], initializer=tf.contrib.layers.xavier_initializer())
    b1 = tf.get_variable(name='biases1', shape=[hidden_Size], initializer=tf.zeros_initializer())
    Wx_plus_b1 = tf.matmul(x_data, W1) + b1  #矩阵x和W1相乘，然后加上偏置b1
    output1 = tf.nn.relu(Wx_plus_b1) #激活函数使用tf.nn.relu

    W2 = tf.get_variable(name="weights2", shape=[hidden_Size, hidden_Size], initializer=tf.contrib.layers.xavier_initializer())
    b2 = tf.get_variable(name='biases2', shape=[hidden_Size], initializer=tf.zeros_initializer())
    Wx_plus_b2 = tf.matmul(output1, W2) + b2  # 矩阵output1和W2相乘，然后加上偏置b2
    output2 = tf.nn.relu(Wx_plus_b2)  # 激活函数使用tf.nn.relu

    #输出层
    W3 = tf.get_variable(name="weights3", shape=[hidden_Size, 1], initializer=tf.contrib.layers.xavier_initializer())
    b3 = tf.get_variable(name='biases3', shape=[1], initializer=tf.zeros_initializer())
    Wx_plus_b3 = tf.matmul(output2, W3)+b3
    output3 = Wx_plus_b3

    # 用内置fully_connected方法
    # output1 = tf.contrib.layers.fully_connected(x_data, 100, activation_fn=tf.nn.relu)
    # output2 = tf.contrib.layers.fully_connected(output1, 100, activation_fn=tf.nn.relu)
    # output3 = tf.contrib.layers.fully_connected(output2, 1, activation_fn=None)

    #损失
    loss = tf.reduce_mean(tf.reduce_sum(tf.square(y_data-output3), reduction_indices=[1])) #在第一维上，偏差平方后求和，再求平均值，来计算损失
    #梯度下降
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss) # 使用梯度下降法，设置步长0.1，来最小化损失
    #初始化变量
    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)
        loss_all = []
        for i in range(training_iters):
            sess.run(train_step)
            s = sess.run(loss)
            loss_all.append(s)
            if i%(training_iters/10) == 0:
                print("step={} loss={}".format(i, s))
                y_pred = sess.run(output3)

        fig = plt.figure()
        ax = fig.add_subplot(211)
        ax.set_ylim(0, 1)
        ax.plot(loss_all, 'red', label='loss')
        bx = fig.add_subplot(212)
        bx.plot(y_data, 'blue', label='data')
        bx.plot(y_pred, 'green', label='pred')
        plt.xlabel('step')
        plt.show()


if __name__ == '__main__':
    approximate_relu()
