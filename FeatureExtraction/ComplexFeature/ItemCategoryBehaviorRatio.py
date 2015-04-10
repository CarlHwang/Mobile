#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from Globals import SplitHour, behaviorStr

# 2. 最近1/2/3/4/5/6/7/8/9/10/12/14/16/18/20/25/30/40/50/60/80/100/150用户对该商品的 点击、收藏、加购、购买 次数，占用户对该商品所属 类别 同一行为的比例

def ItemCategoryBehaviorRatio(behavior):
    
    head = [1,2,3,4,5,6,7,8,9,10,12,14,16,18,20,25,30,40,50,60,80,100,150]
    maxHead = max(head)
    table = {}
    
    with open('../../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            behavoir_type  = row[2]
            item_category = row[4]
            time = row[5]
            
            if user_id == 'user_id':
                continue
            if not behavoir_type == behavior:
                continue
            
            time = int(time)
            
            if time <= SplitHour - maxHead:
                continue
            
            gap = SplitHour - time + 1
            
            if table.get(user_id):
                
                if table[user_id].get(item_category):
                    if not table[user_id][item_category].get(item_id):
                        table[user_id][item_category][item_id] = [0]*len(head)
                else:
                    table[user_id][item_category] = {'total':[0]*len(head), item_id:[0]*len(head)}
            else:
                table[user_id] = {item_category:{'total':[0]*len(head), item_id:[0]*len(head)}}
                
            for i in range(len(head)):
                if gap <= head[i]:
                    table[user_id][item_category][item_id][i] += 1
                    table[user_id][item_category]['total'][i] += 1
            
    # 输出的文件头
    behavior_str = behaviorStr(behavior)
    path = '../../csv/complex/item_category_behavior_ratio_' + behavior_str + '.csv'
    
    outfile = open(path, 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    
    row = ['user_id', 'item_id']
    row.extend(head)
    spamwriter.writerow(row)
    
    
    for user_id in table.keys():
        
        for item_category in table[user_id].keys():
            
            denominator = table[user_id][item_category]['total']
            
            for item_id in table[user_id][item_category].keys(): 
                if item_id == 'total':
                    continue
                
                row = table[user_id][item_category][item_id]
                
                ret = []
                for i in range(len(denominator)):
                    if denominator[i] == 0:
                        ret.append(float(0))
                    else:
                        ret.append(row[i]/float(denominator[i]))
                
                dummy = [user_id, item_id]
                dummy.extend(ret)
                spamwriter.writerow(dummy)
                
                print user_id, item_id, item_category
    print 'ItemCategoryBehaviorRatio Over'
    
ItemCategoryBehaviorRatio('1')
ItemCategoryBehaviorRatio('2')
ItemCategoryBehaviorRatio('3')
ItemCategoryBehaviorRatio('4')



'''
#
#
#    GET FEATURE
#
#
'''
        
        
def GetItemCategoryBehaviorRatio(outputTable, behavior):
    inputTable = {}
    behavior_str = behaviorStr(behavior)
    path = '../../csv/complex/item_category_behavior_ratio_' + behavior_str + '.csv'
    
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

