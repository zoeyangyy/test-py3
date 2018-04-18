#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2018/4/11 下午6:59
# @Author      : Zoe
# @File        : alpha.py
# @Description :

def main():
    li = []
    while True:
        a = input().strip()
        if not a:
            break
        li.append(a)

    b = li[0].split()[0]


if __name__ == '__main__':
    main()