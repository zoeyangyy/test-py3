#!/bin/bash/env python
#-*- coding: utf-8
# https://blog.csdn.net/zjsghww/article/details/55211530

import numpy as np
from sklearn.datasets import make_moons
from functools import reduce

class LR:
    def __init__(self):
        self.dim = 3
        self.w = np.random.random(self.dim)
        # self.b = 0
        self.eta = 0.2

    def sigmoid(self, x):
        return 1.0/(1+np.exp(-x))

    def logistic_regression(self,x,y,eta):
        itr = 0
        self.eta = eta
        row, column = np.shape(x)
        xpts = np.linspace(-1.5, 2.5)
        while itr <= 1000:
            # fx = np.dot(self.w, x.T) + self.b
            fx = np.dot(self.w, x.T)
            hx = self.sigmoid(fx)
            t = (hx-y)
            s = [[i[0]*i[1][0], i[0]*i[1][1], i[0]*i[1][2]] for i in zip(t, x)]
            gradient_w = np.sum(s, 0)/row * self.eta
            # gradient_b = np.sum(t, 0)/row * self.eta
            self.w -= gradient_w
            # self.b -= gradient_b

            # **********self********
            if itr % 20 == 0:
                # print(self.w, '______', self.b)
                print(self.w)

            # **********self********

            # ypts = (lr.w[0] * xpts + lr.b) / (-lr.w[1])
            ypts = (lr.w[0] * xpts) / (-lr.w[1])
            if itr % 50 == 0:
                plt.figure()
                for i in range(250):
                    plt.plot(x[i, 0], x[i, 1], col[y[i]] + 'o')
                plt.ylim([-1.5,1.5])
                plt.plot(xpts,ypts, 'g-', lw = 2)
                plt.title('eta = %s, Iteration = %s\n' % (str(eta), str(itr)))
                plt.show()
                # plt.savefig('p_N%s_it%s' % (str(row), str(itr)), dpi=200, bbox_inches='tight')

            # if abs(gradient_b) < 0.001 and reduce(lambda x,y:x&y, map(lambda x:abs(x)<0.001, gradient_w)):
            if reduce(lambda x, y: x & y, map(lambda x: abs(x) < 0.001, gradient_w)):
                break
            itr += 1


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    x, y = make_moons(250, noise=0.25)
    x_new = []
    for i in x:
        p = i.tolist()
        p.append(1)
        p = np.array(p)
        x_new.append(p)
    x_new = np.array(x_new)
    col = {0:'r',1:'b'}
    lr = LR()
    lr.logistic_regression(x_new,y,eta=1.2)
