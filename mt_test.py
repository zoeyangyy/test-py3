#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2017/10/1 下午3:45
# @Author      : Zoe
# @File        : mt_test.py
# @Description : multi threading
#                https://www.bilibili.com/video/av9362115/

import threading
import time
from queue import Queue


def thread_job():
    # print("this is an added thread, number is %s" % threading.current_thread())
    print('T1 start\n')
    for i in range(10):
        time.sleep(0.1)
    print('T1 finish\n')


def job2():
    print('T2 start\n')
    print('T2 end\n')


def main():
    added_thread = threading.Thread(target=thread_job, name='T1')
    thread2 = threading.Thread(target=job2, name='T2')
    added_thread.start()
    thread2.start()
    added_thread.join()
    thread2.join()
    print('all done')
    # print(threading.active_count())
    # print(threading.enumerate())
    # print(threading.current_thread())


def job(l, q):
    for i in range(len(l)):
        l[i] = l[i]**2
    q.put(l)


def multithreading():
    q = Queue()
    threads = []
    data = [[1,2,3],[2,3,4],[4,5,6],[5,6,7]]
    for i in range(4):
        t = threading.Thread(target=job, args=(data[i], q))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    results = []
    for _ in range(4):
        results.append(q.get())
    print(results)


if __name__ == '__main__':
    multithreading()
