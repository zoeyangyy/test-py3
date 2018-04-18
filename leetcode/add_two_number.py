#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2018/3/24 下午4:36
# @Author      : Zoe
# @File        : add_two_number.py
# @Description :

# Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
# Output: 7 -> 0 -> 8
# Explanation: 342 + 465 = 807.

# Definition for singly-linked list.

class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        # carry = 0
        # sum = ListNode(0)
        # s = sum
        # while l1 is not None or l2 is not None or carry:
        #     s.val = carry
        #     if l1:
        #         s.val += l1.val
        #         l1 = l1.next
        #     if l2:
        #         s.val += l2.val
        #         l2 = l2.next
        #     carry = int(s.val / 10)
        #     s.val = s.val % 10
        #     if l1 or l2 or carry:
        #         s.next = ListNode(0)
        #         s = s.next
        # return sum

        output = tmp = ListNode(0)
        carry = 0
        while l1 or l2:
            x = l1.val if l1 else 0
            y = l2.val if l2 else 0
            sums = x + y + carry
            carry = sums // 10
            tmp.next = ListNode(sums % 10)
            tmp = tmp.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        if carry: tmp.next = ListNode(carry)
        return output.next


l1 = ListNode(2)
l12 = ListNode(4)
l13 = ListNode(3)
l1.next = l12
l12.next = l13

l2 = ListNode(5)
l22 = ListNode(6)
l23 = ListNode(4)
l2.next = l22
l22.next = l23

s = Solution()
sum = s.addTwoNumbers(l1, l2)
while sum:
    print(sum.val)
    sum = sum.next