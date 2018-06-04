#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2018/4/10 下午6:18
# @Author      : Zoe Yang
# @File        : relu_approximate.py
# @Description : 实验证明，一个两层的ReLU网络可以模拟任何函数


import numpy as np
from numpy import *
import matplotlib.pyplot as plt


class TwoLayer_NeuralNetwork(object):
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        # Set number of nodes in input, hidden and output layers
        self.input_nodes = input_nodes
        self.hidden1_nodes = hidden_nodes
        self.hidden2_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Initialize weights, biases and learning rate
        self.weights_input_to_hidden1 = self.weights_initializer(self.hidden1_nodes, self.input_nodes)
        self.weights_hidden1_to_hidden2 = self.weights_initializer(self.hidden2_nodes, self.hidden1_nodes)
        self.weights_hidden2_to_output = self.weights_initializer(self.output_nodes, self.hidden2_nodes)

        self.bias_hidden1 = self.bias_initializer(self.hidden1_nodes)
        self.bias_hidden2 = self.bias_initializer(self.hidden2_nodes)
        self.bias_output = self.bias_initializer(self.output_nodes)

        self.lr = learning_rate

        # Activation function is the Relu function
        self.activation_function = (lambda x: np.maximum(0, x))

    # weights initialization function : same as tf.contrib.layers.xavier_initializer()
    def weights_initializer(self, input, output):
        return np.random.uniform(-sqrt(6 / (input+output)), sqrt(6/(input+output)), size=(input, output))

    # bias initialization function : same as tf.zeros_initializer()
    def bias_initializer(self, size):
        return np.zeros((size, 1))

    # construct train and test data
    def data_constructor(self, number):
        # input data
        x_data = np.linspace(-2.0, 2.0, num=number).astype('float32').reshape([number, 1])

        # output data
        # Different kinds of functions
        y_data = 0.2 + 0.4 * x_data ** 2 + 0.3 * x_data * sin(15 * x_data) + 0.05 * cos(50 * x_data)
        # y_data = 0.2+0.3*x_data+0.4*x_data**2
        # y_data = 3*x_data+1
        return x_data, y_data

    # shuffle x y
    def shuffle_xy(self, inputs_list, targets_list):
        zip_list = list(zip(inputs_list, targets_list))
        random.shuffle(zip_list)
        inputs_list[:], targets_list[:] = zip(*zip_list)
        return inputs_list, targets_list

    # training process
    def train(self, inputs_list, targets_list):
        # Convert inputs list to 2d array
        inputs = np.array(inputs_list, ndmin=2).T  # inputs shape is [feature_diemension, 1]
        targets = np.array(targets_list, ndmin=2).T

        ### Forward pass ###

        hidden1_inputs = np.dot(self.weights_input_to_hidden1, inputs) + self.bias_hidden1  # signals into hidden layer 1
        hidden1_outputs = self.activation_function(hidden1_inputs)  # signals from hidden layer 1

        hidden2_inputs = np.dot(self.weights_hidden1_to_hidden2, hidden1_outputs) + self.bias_hidden2  # signals into hidden layer 2
        hidden2_outputs = self.activation_function(hidden2_inputs)  # signals from hidden layer 2

        # Output Layer without activation function
        final_inputs = np.dot(self.weights_hidden2_to_output, hidden2_outputs) + self.bias_output  # signals into final output layer
        final_outputs = final_inputs  # signals from final output layer

        # loss is defined as the mean square of the difference
        loss = np.mean((targets_list - final_outputs)**2)/2

        ### Backward pass，Use Gradient Descent to update weights and bias ###

        # Output layer error is the difference between desired target and actual output
        output_errors = targets_list - final_outputs

        # Backpropagated error: errors propagated to the hidden layer
        hidden2_errors = np.dot(output_errors, self.weights_hidden2_to_output) * (1.0*(hidden2_outputs>0)).T
        hidden1_errors = np.dot(hidden2_errors, self.weights_hidden1_to_hidden2) * (1.0*(hidden1_outputs>0)).T

        # Update the weights
        # update hidden-to-output, hidden-to-hidden, hidden-to-input weights with gradient descent step
        self.weights_hidden2_to_output += np.dot(output_errors, hidden2_outputs.T) * self.lr
        self.weights_hidden1_to_hidden2 += np.dot(hidden2_errors.T, hidden1_outputs.T) * self.lr
        self.weights_input_to_hidden1 += np.dot(hidden1_errors.T, inputs.T) * self.lr

        # Update the biases
        self.bias_output += output_errors * self.lr
        self.bias_hidden2 += hidden2_errors.T * self.lr
        self.bias_hidden1 += hidden1_errors.T * self.lr

        return loss

    # testing process
    def test(self, inputs_list):
        # Run a forward pass through the network
        inputs = np.array(inputs_list, ndmin=2).T

        # Hidden layer
        hidden1_inputs = np.dot(self.weights_input_to_hidden1, inputs) + self.bias_hidden1  # signals into hidden layer 1
        hidden1_outputs = self.activation_function(hidden1_inputs)  # signals from hidden layer 1
        hidden2_inputs = np.dot(self.weights_hidden1_to_hidden2, hidden1_outputs)  + self.bias_hidden2 # signals into hidden layer 2
        hidden2_outputs = self.activation_function(hidden2_inputs)  # signals from hidden layer 2
        # Output layer
        final_inputs = np.dot(self.weights_hidden2_to_output, hidden2_outputs) +self.bias_output # signals into final output layer
        final_outputs = final_inputs  # signals from final output layer

        return final_outputs


if __name__ == '__main__':
    # Initialize parameters
    input_Size = 1
    hidden_Size = 100
    output_Size = 1
    learning_rate = 0.1
    Number = 100
    epoch = 20000
    training_iters = Number
    random.seed(5)

    # Instantiate NeuralNetwork object
    NN = TwoLayer_NeuralNetwork(input_Size, hidden_Size, output_Size, learning_rate)
    # Construct data
    x_data, y_data = NN.data_constructor(Number)

    # Training Model and collect average loss in each epoch
    epoch_i, loss_average = 0, []
    while epoch_i < epoch:
        step, loss = 0, 0
        # x_data, y_data = NN.shuffle_xy(x_data, y_data)
        while step < training_iters:
            loss += NN.train(x_data[step], y_data[step])
            step += 1
        epoch_i += 1
        if epoch_i % 1000 == 0:
            loss_average.append(loss / training_iters)
            print('Epoch:{}  Average_loss:{}'.format(epoch_i, loss_average[-1]))

    # Testing Model
    y_pred = NN.test(x_data)

    # Draw the approximation results （part of drawing codes）
    fig = plt.figure(1)
    ax = fig.add_subplot(211)
    ax.plot(loss_average, '#FF8C00', label='loss')
    ax.legend()
    bx = fig.add_subplot(212)
    bx.plot(y_data, 'blue', label='actual')
    bx.plot(y_pred[0], 'green', label='pred')
    xticks = np.arange(0, Number+1, 20)
    bx.set_xticks(xticks)
    bx.set_xticklabels(np.arange(-2, 2.1, 0.8))
    bx.legend()
    plt.xlabel('Function = 0.2+0.4*x**2+0.3*x*sin(15x)+0.05*cos(50x)')
    plt.show()
