#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2018/3/27 下午8:01
# @Author      : Zoe
# @File        : wangyi.py
# @Description :


def one():
    N = int(input().strip())
    X1 = [int(i) for i in input().strip().split()]
    Y1 = [int(i) for i in input().strip().split()]
    X2 = [int(i) for i in input().strip().split()]
    Y2 = [int(i) for i in input().strip().split()]

    dic = {}
    for i in range(0, N):
        X = (X1[i], Y1[i])
        Y = (X2[i], Y2[i])
        for k in range(X[0], Y[0]):
            for p in range(X[1], Y[1]):
                if k not in dic.keys():
                    dic[k] = {}
                if p not in dic[k].keys():
                    dic[k][p] = 1
                else:
                    dic[k][p] += 1
    print(dic)
    Max = 0
    for i in dic:
        for j in dic[i]:
            if dic[i][j] > Max:
                Max = dic[i][j]

    print(Max)



def three():
    N = [int(i) for i in input().strip().split()]
    dic = {}
    for i in range(0, N[0]):
        work = [int(i) for i in input().strip().split()]
        dic[work[0]] = work[1]
    li = sorted(dic.keys())
    people = [int(i) for i in input().strip().split()]
    for i in people:
        for j in range(0, len(li)):
            if j == len(li) - 1 and i >= li[j]:
                print(dic[li[j]])
            elif i >= li[j]:
                continue
            elif j == 0:
                print(0)
                break
            else:
                print(dic[li[j-1]])
                break

three()


def two():
    N = int(input().strip())
    for i in range(0, N):
        Num = int(input().strip())
        line = list(input().strip())
        li = [0]*len(line)
        for index,letter in enumerate(line):
            if letter == '.':
                li[index] = 1
        new_li = [0]*len(line)
        count = 0
        for index, letter in enumerate(li):
            if letter == 1 and new_li[index] == 0:
                new_li[index] += 1
                if index+1 < len(li):
                    new_li[index+1] += 1
                if index+2 < len(li):
                    new_li[index+2] += 1
                count += 1

        print(count)




