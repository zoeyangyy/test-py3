#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2017/10/1 下午3:04
# @Author      : Zoe
# @File        : mp_test.py
# @Description : multiprocessing

import multiprocessing as mp
import threading as td
import time


def job(q):
    res = 0
    for i in range(100000):
        res += i+i**2+i**3
    q.put(res)


def mulcore():
    q = mp.Queue()
    p1 = mp.Process(target=job, args=(q,))
    p2 = mp.Process(target=job, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    res1 = q.get()
    res2 = q.get()
    print("multicore:", res1 + res2)


def normal():
    res = 0
    for _ in range(2):
        for i in range(100000):
            res += i + i ** 2 + i ** 3
    print("normal:", res)


def multithread():
    q = mp.Queue()
    t1 = td.Thread(target=job, args=(q,))
    t2 = td.Thread(target=job, args=(q,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    res1 = q.get()
    res2 = q.get()
    print("multithread:", res1 + res2)


def test1():
    st = time.time()
    normal()
    st1 = time.time()
    print("normal time:", st1-st)
    multithread()
    st2 = time.time()
    print("multithread time:", st2-st1)
    mulcore()
    st3 = time.time()
    print("multicore time:", st3-st2)


def job2(x):
    return x*x


def multicore2():
    pool = mp.Pool(processes=2)
    res = pool.map(job2, range(10))
    print(res)

    # apply_async 只能传一个参数
    res = pool.apply_async(job2, (2,))
    print(res.get())
    multi_res = [pool.apply_async(job2, (i,)) for i in range(10)]
    print([res.get() for res in multi_res])


multicore2()