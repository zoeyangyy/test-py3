#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2018/3/27 上午8:38
# @Author      : Zoe
# @File        : LCP.py
# @Description :

import re


class Solution:
    def longestCommonPrefix(self, strs):
        if not strs:
            return ''
        prefix = strs[0]
        for i in range(1, len(strs)):
            match = re.match(prefix, strs[i])
            while not match:
                prefix = prefix[:-1]
                match = re.match(prefix, strs[i])
        return prefix






