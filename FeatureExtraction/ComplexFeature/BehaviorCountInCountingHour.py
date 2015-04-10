#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from Globals import SplitHour, behaviorStr

# 3. 用户对该商品 的第1、2、3、4、5、6、7、8、9、10近有访问小时是什么时候（在此之前多远）里，点击、收藏、加购、购买了多少次 乘以 距最近（分割点）时间间隔的倒数

def BehaviorCountInCountingHour(behavior):

    head = [1,2,3,4,5,6,7,8,9,10]
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
            
            key = user_id + ' ' + item_id
            
            if table.get(key):
                
                if not table[key].get(time):
                    table[key][time] = 0
            else:
                table[key] = {time: 0}
                
            table[key][time] += 1
            
    # 输出的文件头
    behavior_str = behaviorStr(behavior)
    path = '../../csv/complex/behavior_count_in_counting_hour_' + behavior_str + '.csv'
    
    outfile = open(path, 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    
    row = ['user_id', 'item_id']
    row.extend(head)
    spamwriter.writerow(row)
    
    for key in table.keys():        
        pairs = [(time, table[key][time]) for time in sorted(table[key].keys(), reverse = True)]
        
        row = []
        for pair in pairs:
            gap_reverse = 1 / float(SplitHour - pair[0] + 1)
            row.append(gap_reverse*pair[1])
        
        if len(row) >= len(head):
            row = row[:len(head)]
        else:
            row.extend([0]*(len(head) -len(row)))
            
        user_id, item_id = key.split()[0], key.split()[1]
        dummy = [user_id, item_id]
        dummy.extend(row)
        spamwriter.writerow(dummy)
    
    print "BehaviorCountInCountingHour Done!"
    
BehaviorCountInCountingHour('1')
BehaviorCountInCountingHour('2')
BehaviorCountInCountingHour('3')
BehaviorCountInCountingHour('4')

'''
#
#
#    GET FEATURE
#
#
'''
        
        
def GetBehaviorCoutingInCountingHour(outputTable, behavior):
    inputTable = {}
    behavior_str = behaviorStr(behavior)
    path = '../../csv/complex/behavior_count_in_counting_hour_' + behavior_str + '.csv'
    
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

            