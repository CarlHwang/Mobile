#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from Globals import SplitHour, behaviorStr
from math import log

# 4. 用户 点击、收藏、加购、购买该商品的最远一个有访问小时是什么时候(取与分割点的间隔，取log)，那个时间点击、收藏、加购、购买了多少次该商品


def EarliestBehavior(behavior):
    
    table = {}
    with open('../../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            behavior_type = row[2]
            time = row[5]
            
            if user_id == 'user_id':
                continue
            if not behavior_type == behavior:
                continue
            
            time = int(time)
            gap = SplitHour - time + 1
            
            if table.get(user_id):
                
                if not table[user_id].get(item_id):
                    
                    table[user_id][item_id] = [gap, 1]
                
                else:
                        
                    if gap > table[user_id][item_id][0]:
                        
                        table[user_id][item_id] = [gap, 1]
                        
                    elif gap == table[user_id][item_id][0]:
                        
                        table[user_id][item_id][1] += 1
            else:
                table[user_id] = {item_id:[gap, 1]}
            
    # 输出的文件头
    behavior_str = behaviorStr(behavior)
    path = '../../csv/complex/earliest_behavior_' + behavior_str + '.csv'
    
    outfile = open(path, 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'num_behavior', 'time'])
    
    for user_id in table.keys():
        for item_id in table[user_id].keys():
            (gap, behavior_count) = table[user_id][item_id]
            gap = log(gap)
            spamwriter.writerow([user_id, item_id, behavior_count, gap])
            print user_id, item_id, gap, behavior_count
            
    print "EarliestBehavior Done!"
     

EarliestBehavior('1')
EarliestBehavior('2')
EarliestBehavior('3')
EarliestBehavior('4')


'''
#
#
#    GET FEATURE
#
#
'''
        
        
def GetEarliestBehavior(outputTable, behavior):
    inputTable = {}
    behavior_str = behaviorStr(behavior)
    path = '../../csv/complex/earliest_behavior_' + behavior_str + '.csv'
    
    len_head = None
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            features = row[2:]
            len_head = len(features)
            
            if user_id == 'user_id':
                continue
            
            key = user_id + ' ' + item_id
            inputTable[key] = features
 
    for key in outputTable.keys():
        user_id, item_id = key.split()[0], key.split()[1]
        
        if not inputTable.get(key):
            features = [0]*len_head
        else:
            features = inputTable[key]
        
        outputTable[key].extend(features)

    