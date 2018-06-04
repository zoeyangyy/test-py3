#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2018/5/24 下午7:43
# @Author      : Zoe
# @File        : RBM_mnist.py
# @Description :

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import cv2
import numpy as np

learning_rate = 1e-4
keep_prob_rate = 0.7
hidden_units = 500
max_epoch = 1000


def weight_variable(shape):
    # initial = tf.truncated_normal(shape, stddev=0.1)
    initial = tf.contrib.layers.xavier_initializer(shape)
    return tf.Variable(initial)


def bias_variable(shape):
    # initial = tf.constant(0.1, shape=shape)
    initial = tf.zeros_initializer(shape)
    return tf.Variable(initial)


# define placeholder for inputs to network
xs = tf.placeholder(tf.float32, [None, 784])
keep_prob = tf.placeholder(tf.float32)
x_image = tf.reshape(xs, [-1, 784])

# encoder连接层
# W_encoder = weight_variable([784, 256])
W_encoder = tf.get_variable('w', shape=[784, hidden_units], initializer=tf.contrib.layers.xavier_initializer())
b_encoder = tf.get_variable('b_e', shape=[hidden_units], initializer=tf.zeros_initializer())
h_encoder = tf.nn.sigmoid(tf.matmul(x_image, W_encoder) + b_encoder)
# h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# decoder连接层
b_decoder = tf.get_variable('b_d', shape=[784], initializer=tf.zeros_initializer())
# b_decoder = bias_variable([784])
x_decoder = tf.nn.sigmoid(tf.matmul(h_encoder, tf.transpose(W_encoder)) + b_decoder)

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=x_decoder, labels=x_image))
train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)

mnist = input_data.read_data_sets('/Users/zoe/Documents/复旦课程/神经网络与深度学习/pj2/MNIST_data', one_hot=True)
mnist_images = mnist.train.images

with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)

    BigIm = np.zeros((28, 280))
    index = 0
    for i in range(max_epoch):
        batch_xs, batch_ys = mnist.train.next_batch(100)
        sess.run(train_step, feed_dict={xs: batch_xs, keep_prob: keep_prob_rate})
        # 每训练十分之一的max_epoch，就输出一次结果
        if i % (max_epoch//10) == 0:
            index = i//(max_epoch//10)
            print(index)
            test_image = np.reshape(mnist.test.images[1], (-1, 784))
            result = sess.run(x_decoder, feed_dict={xs: test_image, keep_prob: 1})
            result_image = np.reshape(result, (28, 28))
            BigIm[0:28, 28 * index:28 * (index + 1)] = result_image
    cv2.imshow("demo", BigIm)
    cv2.waitKey(0)
