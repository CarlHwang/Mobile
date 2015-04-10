#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from Globals import SplitHour, behaviorStr, hasGapBetween
from __builtin__ import str

# 7. 用户24小时、48小时、72小时、96小时、120小时、144小时、168小时以前，有多少个1小时、2小时、3小时、6小时、12小时 有点击、收藏、加购、购买

def BehaviorHourCountBeforePeriod(behavior):
    
    table = {}
    
    periods = [24,48,72,96,120,144,168]
    counting = [1,2,3,6,12]
    
    maxGap = 0  #最大间隔，表示最远时间
    
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
            if gap <= min(periods):
                continue
            
            maxGap = max(maxGap, gap)
            
            if table.get(user_id):
                
                if not table[user_id].get(item_id):
                    table[user_id][item_id] = []
            else:
                table[user_id] = {item_id:[]}
                
            table[user_id][item_id].append(gap)
    
   
    
    # 输出的文件头
    behavior_str = behaviorStr(behavior)
    path = '../../csv/complex/behavior_hour_count_before_period_' + behavior_str + '.csv'
    outfile = open(path, 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    
    row = ['user_id', 'item_id']
      
    for period in periods:
        lowerbound = 0
        for grade in counting:
            if grade > period:  break
            row.append(str(period) + '_' + str(grade))
                  
    spamwriter.writerow(row)
               
    k = 0 
    for user_id in table.keys():
        items = table[user_id]
        
        for item_id in items.keys():
            result = [user_id, item_id]
            gaps = items[item_id]
            
            for period in periods:
                for grade in counting:
                    
                    if grade > period:  break
                    num = 0
                    lowerbound, upperbound = period, period
                    
                    while(upperbound < maxGap):
                        
                        lowerbound = upperbound                        
                        if upperbound + grade < maxGap:
                            upperbound += grade
                        else:
                            upperbound = maxGap
                        if hasGapBetween(gaps, lowerbound, upperbound): num += 1
                        
                    result.append(num)
                    
            spamwriter.writerow(result)
            print k, user_id, item_id
            k += 1

BehaviorHourCountBeforePeriod('1')
BehaviorHourCountBeforePeriod('2')
BehaviorHourCountBeforePeriod('3')
BehaviorHourCountBeforePeriod('4')


'''
#
#
#    GET FEATURE
#
#
'''
        
        
def GetBehaviorHourCountBeforePeriod(outputTable, behavior):
    inputTable = {}
    behavior_str = behaviorStr(behavior)
    path = '../../csv/complex/behavior_hour_count_before_period_' + behavior_str + '.csv'
    
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


