#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

# 获得每个商品的对于 不同行为 的人数
def item_behavior_count():
    # 输出的文件头
    outfile = open('item_behavior_count.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['item_id', 'click', 'collect', 'cart', 'deal'])
    
    items = {}
    with open('train_user_time_to_int.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            item_id = row[1]
            behavior_type = row[2]

            if(len(behavior_type) > 2):
                continue
            
            behavior_type = int(behavior_type)
            
            # 如果统计集合中没有这个商品，加入，如果有，对应的行为计数+1
            if not items.get(item_id):
                behaviors = [0,0,0,0]
                behaviors[behavior_type-1] += 1
                items[item_id] = behaviors
            else:
                items[item_id][behavior_type-1] += 1
            print item_id, behavior_type
    
    for key in items.keys():
        behaviors = items.get(key)
        spamwriter.writerow([key, behaviors[0], behaviors[1], behaviors[2], behaviors[3]])

            
if __name__ == '__main__':
    item_behavior_count()
