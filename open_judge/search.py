#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2018/3/21 下午8:06
# @Author      : Zoe
# @File        : search.py
# @Description :
import heapq


class PriorityQueue(object):
    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        for index, (p, c, i) in enumerate(self.heap):
            if i.state == item.state:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)


class node:
    """define node"""
    def __init__(self, state, parent, path_cost):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost


class problem:
    """searching problem"""

    def __init__(self, initial_state, actions):
        self.initial_state = initial_state
        self.actions = actions
        # 可以在这里随意添加代码或者不加

    def search_actions(self, state):
        available_action = list()
        for i in self.actions:
            if state == i[0]:
                available_action.append(i)
        return available_action
        # raise Exception('获取state的所有可行的动作')

    def solution(self, node):
        position = node
        path = list()
        while position.state != self.initial_state:
            path.append(position.state)
            position = position.parent
        path.append('Start')
        return path[::-1]
        # raise Exception('获取从初始节点到node的路径')

    def goal_test(self, state):
        if state == 'Goal':
            return True
        else:
            return False
        # raise Exception('判断state是不是终止节点')

    def child_node(self, node_begin, action):
        return node(action[1], node_begin, node_begin.path_cost+int(action[2]))
        # raise Exception('获取从起始节点node_begin经过action到达的node')


def UCS(problem):
    node_test = node(problem.initial_state, '', 0)
    frontier = PriorityQueue()
    frontier.push(node_test, node_test.path_cost)
    explored = []

    while 1:
        if frontier.isEmpty():
            return 'Unreachable'
        next_node = frontier.pop()
        if problem.goal_test(next_node.state):
            return problem.solution(next_node)
        explored.append(next_node.state)
        for action in problem.search_actions(next_node.state):
            child_node = problem.child_node(next_node, action)
            if child_node.state not in explored:
                frontier.push(child_node, child_node.path_cost)
            elif child_node.state in frontier.heap:
                frontier.update(child_node, child_node.path_cost)

    # raise Exception('进行循环')


def main():
    actions = []
    while True:
        a = input().strip()
        if a != 'END':
            a = a.split()
            actions += [a]
        else:
            break
    graph_problem = problem('Start', actions)
    answer = UCS(graph_problem)
    s = "->"
    if answer == 'Unreachable':
        print(answer)
    else:
        path = s.join(answer)
        print(path)


if __name__ == '__main__':
    main()
