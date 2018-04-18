#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2018/3/24 下午3:00
# @Author      : Zoe
# @File        : two_sum.py
# @Description :


class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        # 基础方法
        # for index,data in enumerate(nums):
        #     for index2 in range(index+1, len(nums)):
        #         if nums[index]+nums[index2] == target:
        #             return [index, index2]

        # 2222222
        # dic = dict()
        # for index,data in enumerate(nums):
        #     dic[data] = index
        # for index,data in enumerate(nums):
        #     minus = target-data
        #     if minus in dic.keys() and dic[minus] != index:
        #         return [index, dic[minus]]

        # 3333333
        dic = {}
        for index, data in enumerate(nums):
            minus = target-data
            if minus in dic.keys():
                return [dic[minus], index]
            else:
                dic[data] = index


content = [int(i) for i in input().strip().split()]
target = int(input().strip())

c = Solution()
print(c.twoSum(content, target))
