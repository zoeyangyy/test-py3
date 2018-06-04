#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2018/6/2 下午7:03
# @Author      : Zoe
# @File        : music-recommend.py
# @Description :
import os
os.chdir('/Users/zoe/Documents/复旦课程/大数据商业分析/pj2')
import json

with open('playlists.json', 'r', encoding='utf8') as file:
    contents = [json.loads(one) for one in file.readlines()]

print(len(contents))

with open('songs.json', 'r', encoding='utf8') as file:
    songs = [json.loads(one) for one in file.readlines()]

print(len(songs))