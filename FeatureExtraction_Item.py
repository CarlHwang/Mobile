#! /usr/bin/env python
# -*- coding:utf-8 -*-

import Globals
import csv

# 获得每个商品的购买人数
def item_buyed_count():
    data = []
    with open('train_user.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            return