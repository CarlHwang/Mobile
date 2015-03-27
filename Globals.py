#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

# 统计不重复的 商品数量, 种类数量, 地理位置
item_set = {}
category_set = {}
geohash_set = {}
with open('train_item.csv', 'rb') as f:
    reader = csv.reader(f)
    num = 1
    for row in reader:
        item_id = row[0]
        geohash = row[1]
        category = row[2]
        num += 1
        item_set[item_id] = 1
        category_set[category] = 1
        geohash_set[geohash] = 1
        print num, item_id, geohash, category
    print len(item_set.keys()), len(geohash_set.keys()), len(category_set.keys())