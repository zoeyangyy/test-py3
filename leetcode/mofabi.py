#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2018/3/26 上午9:27
# @Author      : Zoe
# @File        : mofabi.py
# @Description :


def one():
    N = int(input().strip())

    li = []
    while N != 0:
        yu = N % 2
        if yu == 1:
            li.append(1)
            N = N // 2
        else:
            li.append(2)
            N = N // 2 -1

    s = ''
    for one in li[::-1]:
        s += str(one)
    print(s)

def two():
    N = input().strip()

    s = []
    for i in range(0, len(N)):
        s.append(N[i])

    N_new = ''
    s = s[::-1]
    for i in range(0, len(s)):
        N_new += s[i]

    print(int(N)+int(N_new))


def three():
    N = input().strip()
    count = 1
    lenth = 1
    for i in range(1, len(N)):
        if N[i] != N[i-1]:
            count += 1
            lenth = 1
        else:
            lenth += 1

    print('%.2f' % (len(N)/count))


def four():

    class Node():
        def __init__(self, state):
            self.state = ''
            self.child = []
        def add_child(self, c):
            self.child.append(c)

    inp = input().strip().split()
    N = int(inp[0])
    L = int(inp[1])
    line = [int(i) for i in input().strip().split()]

    li = []
    for i in range(0, N):
        li.append(Node(i))
    for i in range(0, N-2):
        li[line[i]].add_child(line[i+1])

    start = li[0]
    lenth = 0
    queer = []
    while start:
        lenth += 1
        start = start.child[1]


def five():
    N = int(input().strip())
    for _ in range(0, N):
        _ = input()
        A,B,C = 0,0,0
        Num = [int(i) for i in input().strip().split()]
        for i in range(0, len(Num)):
            if Num[i] % 4 == 0:
                A += 1
            elif Num[i] % 2 == 0:
                B += 1
            else:
                C += 1
        if B and A >= C:
            print('Yes')
        elif (not B) and A-1 >= C:
            print('Yes')
        else:
            print('No')

# five()


def ifvalid(li):
    score = 0
    for i in li:
        if i == '(':
            score += 1
        if i == ')':
            score -= 1
        if score < 0:
            return 0
    return 1


def six():
    origin = input().strip()
    count = 0
    li = [origin]
    for i in range(1, len(origin)):
        for j in range(1, len(origin)):
            changed = list(origin)
            changed.insert(j, changed[i])
            if j < i:
                del changed[i+1]
            else:
                del changed[i]
            if ''.join(changed) not in li:
                li.append(''.join(changed))
                # print(changed)
                count += ifvalid(changed)
    print(count)

# six()

# 可先设 dp[i][j] 表示当前小Q唱到第 i 个音调，牛博士唱到第 j 个音调的难度和；
# 不妨设当前 i > j ：
# 若 i - 1 == j 则发生换人，由于不知道上一次 i 唱到哪里，状态由 min{ dp[k][j] + abs(v[i] - v[k]) }, k < j 转移来；
# 若 i - 1 > j 则表示当前是从 i - 1 唱到 i 的，没有换人，状态由 dp[i-1][j] + abs(v[i] - v[i-1]) 累加；

# 初始情况是若当前有 i 个音调，可以让一个人只唱第一个或最后一个音调，剩下的音调都由另一个人唱：
# dp[i][0] = dp[i-1][0] + abs(v[i] - v[i-1]), i ≥ 2
# dp[i][i-1] = dp[i-1][i-2] + abs(v[i-1] - v[i-2]), i ≥ 2

import collections


def seven():
    N = input().strip()
    li = [int(i) for i in input().strip().split()]

    dp = collections.defaultdict(dict)

    dp[0][0] = 0
    dp[1][0] = 0
    for i in range(2, len(li)):
        dp[i][0] = abs(li[i]-li[i-1]) + dp[i-1][0]

    for i in range(2, len(li)):
        for j in range(1, i):
            if j == i-1:
                m = [dp[j][0]+abs(li[1]-li[0])]
                for k in range(0, j):
                    m.append(dp[j][k] + abs(li[i]-li[k]))
                dp[i][j] = min(m)
            if j < i-1:
                dp[i][j] = dp[i-1][j] + abs(li[i]-li[i-1])
    print(min(list(dp[len(li)-1].values())))

# seven()

import math
from scipy.optimize import fsolve
# ρ=xcosθ+ysinθ


def eight():
    N = input().strip()
    X = [int(i) for i in input().strip().split()]
    Y = [int(i) for i in input().strip().split()]
    p_list = {}
    for i in range(1, len(X)):
        for j in range(0, i):
            # def func(z):
            #     rho, theta = z[0], z[1]
            #     return [
            #         X[i] * math.cos(theta) + Y[i] * math.sin(theta) - rho,
            #         X[j] * math.cos(theta) + Y[j] * math.sin(theta) - rho,
            #     ]
            # r = fsolve(func, [0, 0])
            if Y[i] == Y[j]:
                theta = math.pi/2
            else:
                theta = math.atan((X[i]-X[j])/(Y[i]-Y[j]))
            rho = X[i] * math.cos(theta) + Y[i] * math.sin(theta)

            p = []
            for num in [rho, theta]:
                if num == 0:
                    p.append(0.0)
                else:
                    p.append(round(num, 4))
            if p[0] not in p_list.keys():
                p_list[p[0]] = {}
            if p[1] not in p_list[p[0]].keys():
                p_list[p[0]][p[1]] = 0
            p_list[p[0]][p[1]] += 1
    Max = 0
    for i in p_list:
        for j in p_list[i]:
            if p_list[i][j] > Max:
                Max = p_list[i][j]
    print(int(math.sqrt(Max*2))+1)
# eight()


# 四个for循环。每个for循环选取一个点（判断该点不同于前面的点），前三个点要求不共线。
#     前两个点A,B通过第一条直线；
#         第三个点C通过另一条直线；
#             第四个for循环，对于剩下的n-3个点，判断是否落在这两条直线上。如果有AD与AB平行，则落在第一条直线上；如果有CD与AB垂直，则落在第二条直线上。
#             第四个for循环结束，可以知道这两条直线能穿过最多几个点，每次更新最大值。
# 所有循环结束，输出最终的最大值即可。
# 计算斜率来判断平行和垂直，即dx1 * dy2 == dy1 *dx2。

def eight_robot():
    N = input().strip()
    X = [int(i) for i in input().strip().split()]
    Y = [int(i) for i in input().strip().split()]
    Max = 0

    if len(X)<4:
        Max = len(X)

    for i in range(0, len(X)):
        for j in range(i+1, len(X)):
            all_slope = 2
            if X[j] == X[i]:
                slope_1 = float("inf")
            else:
                slope_1 = (Y[j]-Y[i])/(X[j]-X[i])
            for z in range(j+1, len(X)):
                if X[z] == X[i]:
                    slope_2 = float("inf")
                else:
                    slope_2 = (Y[z] - Y[i]) / (X[z] - X[i])
                if slope_2 == slope_1:
                    all_slope += 1
                    if all_slope == len(X):
                        Max = all_slope
                else:
                    count = 3
                    for k in range(z+1, len(X)):
                        if X[k] == X[z]:
                            slope_3 = float("inf")
                        else:
                            slope_3 = (Y[k] - Y[z]) / (X[k] - X[z])
                        if slope_3 * slope_1 == -1:
                            count += 1; continue;
                        if slope_3 == float('inf') and slope_1 == 0:
                            count += 1; continue;
                        if X[k] == X[i]:
                            slope_4 = float("inf")
                        else:
                            slope_4 = (Y[k] - Y[i]) / (X[k] - X[i])
                        if slope_4 == slope_1:
                            count += 1; continue;
                    if count > Max:
                        Max = count
    print(Max)

eight_robot()


