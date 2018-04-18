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


class TwoLayerNeuralNetwork(object):
    def __init__(self, input_nodes, hidden1_nodes, hidden2_nodes , output_nodes, learning_rate):
        # Set number of nodes in input, hidden and output layers
        self.input_nodes = input_nodes
        self.hidden1_nodes = hidden1_nodes
        self.hidden2_nodes = hidden2_nodes
        self.output_nodes = output_nodes

        # Initialize weights bias and learning rate
        self.weights_input_to_hidden1 = self.weights_initializer(self.hidden1_nodes, self.input_nodes)
        self.weights_hidden1_to_hidden2 = self.weights_initializer(self.hidden2_nodes, self.hidden1_nodes)
        self.weights_hidden2_to_output = self.weights_initializer(self.output_nodes, self.hidden2_nodes)

        self.bias_hidden1 = self.bias_initializer(self.hidden1_nodes)
        self.bias_hidden2 = self.bias_initializer(self.hidden2_nodes)
        self.bias_output = self.bias_initializer(self.output_nodes)

        self.lr = learning_rate

        # Activation function is the sigmoid function
        self.activation_function = (lambda x: np.maximum(0, x))


    # function : xavier_initializer
    def weights_initializer(self, input, output):
        return np.random.uniform(-sqrt(6 / (input+output)), sqrt(6/(input+output)), size=(input, output))

    def bias_initializer(self, size):
        return np.zeros((size,1))

    def train(self, inputs_list, targets_list):
        # Convert inputs list to 2d array
        inputs = np.array(inputs_list, ndmin=2).T  # 输入向量的shape为 [feature_diemension, 1]
        targets = np.array(targets_list, ndmin=2).T

        # 向前传播，Forward pass
        hidden1_inputs = np.dot(self.weights_input_to_hidden1, inputs) + self.bias_hidden1  # signals into hidden layer
        hidden1_outputs = self.activation_function(hidden1_inputs)  # signals from hidden layer
        # 100*1

        hidden2_inputs = np.dot(self.weights_hidden1_to_hidden2, hidden1_outputs) + self.bias_hidden2
        hidden2_outputs = self.activation_function(hidden2_inputs)

        # 输出层，输出层的激励函数就是 y = x
        final_inputs = np.dot(self.weights_hidden2_to_output, hidden2_outputs) + self.bias_output  # signals into final output layer
        final_outputs = final_inputs  # signals from final output layer

        ### 反向传播 Backward pass，使用梯度下降对权重进行更新 ###

        # 输出误差
        # Output layer error is the difference between desired target and actual output.
        loss = (targets_list - final_outputs)**2/2
        output_errors = targets_list - final_outputs

        # 反向传播误差 Backpropagated error
        # errors propagated to the hidden layer
        # 1*100
        hidden2_errors = np.dot(output_errors, self.weights_hidden2_to_output) * (1.0*(hidden2_outputs>0)).T
        hidden1_errors = np.dot(hidden2_errors, self.weights_hidden1_to_hidden2) * (1.0*(hidden1_outputs>0)).T

        # 更新权重 Update the weights
        # 更新隐藏层与输出层之间的权重 update hidden-to-output weights with gradient descent step
        self.weights_hidden2_to_output += np.dot(output_errors, hidden2_outputs.T) * self.lr
        self.weights_hidden1_to_hidden2 += np.dot(hidden2_errors.T, hidden1_outputs.T) * self.lr
        self.weights_input_to_hidden1 += np.dot(hidden1_errors.T, inputs.T) * self.lr

        self.bias_output += output_errors * self.lr
        self.bias_hidden2 += hidden2_errors.T * self.lr
        self.bias_hidden1 += hidden1_errors.T * self.lr

        return loss, self.weights_hidden2_to_output[0][0]

    # 进行预测
    def test(self, inputs_list):
        # Run a forward pass through the network
        inputs = np.array(inputs_list, ndmin=2).T

        #### 实现向前传播 Implement the forward pass here ####
        # 隐藏层 Hidden layer
        hidden1_inputs = np.dot(self.weights_input_to_hidden1, inputs) + self.bias_hidden1  # signals into hidden layer
        hidden1_outputs = self.activation_function(hidden1_inputs)  # signals from hidden layer
        hidden2_inputs = np.dot(self.weights_hidden1_to_hidden2, hidden1_outputs)  + self.bias_hidden2 # signals into hidden layer
        hidden2_outputs = self.activation_function(hidden2_inputs)  # signals from hidden layer
        # 输出层 Output layer
        final_inputs = np.dot(self.weights_hidden2_to_output, hidden2_outputs) +self.bias_output # signals into final output layer
        final_outputs = final_inputs  # signals from final output layer

        return final_outputs


if __name__ == '__main__':
    x_Number = 100
    input_Size = 1
    hidden1_Size = 100
    hidden2_Size = 100
    output_Size = 1
    learning_rate = 0.1
    training_iters = 50000
    random.seed(5)

    NN = TwoLayerNeuralNetwork(input_Size, hidden1_Size, hidden2_Size, output_Size, learning_rate)
    #构造输入数据
    x_data = np.linspace(0.0, 1.0, num=x_Number).astype('float32').reshape([x_Number, 1])
    #y可以是下述各种
    y_data = 0.2+0.4*x_data**2+0.3*x_data*sin(15*x_data)+0.05*cos(50*x_data)
    # y_data = 0.2+0.3*x_data+0.4*x_data**2
    # y_data = 3*x_data+1

    for step in range(training_iters):
        loss,w = NN.train(x_data[step%x_Number], y_data[step%x_Number])
        if step % 1000 == 0:
            print(loss,w)

    y_pred = NN.test(x_data)

    fig = plt.figure()
    bx = fig.add_subplot(111)
    bx.plot(y_data, 'blue', label='data')
    bx.plot(y_pred[0], 'green', label='pred')
    plt.legend()
    plt.show()
