#! /usr/bin/env python
# -*- coding:utf-8 -*-
import time as t

import csv
from Globals import behaviorStr, hasGapBetween

# 8. 用户对该商品的最后一次交互的前后1/2/3/4/5（共3/5/7/9/11小时）中，一共点击、收藏、加购、购买了多少个同类的不同品牌

def ItemOfSameCategoryInRange(behavior):
    localtime = t.asctime( t.localtime(t.time()) )
    print "Start: Local current time :", localtime
    table = {}
    
    rangeBounds = [1,2,3,4,5]
        
    with open('../../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            behavior_type = row[2]
            item_category = row[4]
            time = row[5]
            
            if user_id == 'user_id':
                continue
            if not behavior_type == behavior:
                continue
            
            time = int(time)
            
            if table.get(user_id):
                
                if table[user_id].get(item_category):
                    if not table[user_id][item_category].get(item_id):
                        table[user_id][item_category][item_id] = []
                else:
                    table[user_id][item_category] = {item_id : []}
            else:
                table[user_id] = {item_category : {item_id : []}}
                
            table[user_id][item_category][item_id].append(time)
    
    
    # 输出的文件头
    behavior_str = behaviorStr(behavior)
    path = '../../csv/complex/item_of_same_category_in_range_' + behavior_str + '.csv'
    
    outfile = open(path, 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    
    row = ['user_id', 'item_id']
    row.extend(rangeBounds)
    spamwriter.writerow(row)
    
    for user_id in table.keys():
        categories = table[user_id]
        for item_category in categories.keys():
            items = categories[item_category]
            for item_id in items.keys():
                latestTime = max(items[item_id])
                result = [user_id, item_id]
                for rangebound in rangeBounds:
                    upperbound = latestTime + rangebound
                    lowerbound = latestTime - rangebound
                    num_similar_item = 0
                    for similar_item_id in items.keys():
                        if similar_item_id == item_id:
                            continue
                        similar_item_access_time = items[similar_item_id]
                        
                        if hasGapBetween(similar_item_access_time, lowerbound, upperbound, lowerinclude=True):
                            num_similar_item += 1
                    result.append(num_similar_item)
                spamwriter.writerow(result)
            
    localtime = t.asctime( t.localtime(t.time()) )
    print "End:Local current time :", localtime                       
    print 'ItemOfSameCategoryInRange Done!'


ItemOfSameCategoryInRange('1')
ItemOfSameCategoryInRange('2')
ItemOfSameCategoryInRange('3')
ItemOfSameCategoryInRange('4')





'''
#
#
#    GET FEATURE
#
#
'''
        
        
def GetItemOfSameCategoryInRange(outputTable, behavior):
    inputTable = {}
    behavior_str = behaviorStr(behavior)
    path = '../../csv/complex/item_of_same_category_in_range_' + behavior_str + '.csv'
    
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

