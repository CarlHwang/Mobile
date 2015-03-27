#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

# 统计不重复的 商品数量, 种类数量, 地理位置
item_set = {}
category_set = {}
geohash_set = {}

def getRawData():
    data = []
    with open('train_item.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            # row[0]:item_id, row[1]:item_geohash, row[2]: item_category
            data.append([row[0], row[1], row[2]])
    return data
    
def item_amount_over_item_table():
    data = getRawData()
    num = 0
    for row in data:
        item_id = row[0]
        num += 1
        item_set[item_id] = 1
#         print num, item_id
    print num, "商品数量", len(item_set.keys())
    
def category_amount_over_item_table():
    data = getRawData()
    num = 0
    for row in data:
        category = row[2]
        num += 1
        category_set[category] = 1
#         print num, category
    print num, "种类数量", len(category_set.keys())
    
def geohash_amount_over_item_table():
    data = getRawData()
    num = 0
    for row in data:
        geohash = row[1]
        num += 1
        geohash_set[geohash] = 1
#         print num, geohash
    print num, "地理信息数量", len(geohash_set.keys())
    
if __name__ == "__main__":
    item_amount_over_item_table()
    geohash_amount_over_item_table()
    category_amount_over_item_table()

    