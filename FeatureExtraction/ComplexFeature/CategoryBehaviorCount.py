#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from Globals import SplitHour, behaviorStr

# 用户最近第1、2、3、4、5、6、7、8、9、10、12、14、16、18、20、25、30、40、50、60、80、100、150、200、300、400、500、500以上时间区间内，对该商品所属类别的 点击、收藏、加购、购买次数


def CategoryBehaviorCount(behavior):
    categoryBehaviorTable = {}
    
    head = [1,2,3,4,5,6,7,8,9,10,12,14,16,18,20,25,30,40,50,60,80,100,150,200,300,400,500]
    maxHead = max(head)
    
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
            gap = SplitHour - time + 1
            
            if gap > maxHead:
                continue
            
            idx = len(head) - 1
            for i in range(len(head)):
                t = head[i]
                if gap <= t:
                    idx = i
                    break
            
            if categoryBehaviorTable.get(user_id):
                if not categoryBehaviorTable[user_id].get(item_category):
                    categoryBehaviorTable[user_id][item_category] = [0]*len(head)            
            else:
                categoryBehaviorTable[user_id] = {item_category:[0]*len(head)}
                
            categoryBehaviorTable[user_id][item_category][idx] += 1
            
            print user_id, item_id, item_category
    
    
    # 输出的文件头
    behavior_str = behaviorStr(behavior)
    path = '../../csv/complex/category_behavior_count_' + behavior_str + '.csv'
    
    outfile = open(path, 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    
    row = ['user_id', 'item_id']
    row.extend(head)
    spamwriter.writerow(row)
    
    holder = {}
            
    with open('../../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            behavior_type  = row[2]
            item_category = row[4]
            time = row[5]
                
            if user_id == 'user_id':
                continue
            if not behavior_type == behavior:
                continue
            
            time = int(time)
            gap = SplitHour - time + 1
            
            if gap > maxHead:
                continue
            
            key = user_id + ' ' + item_id
            if holder.get(key):
                continue
            
            dummy = [user_id, item_id]
            dummy.extend(categoryBehaviorTable[user_id][item_category])
            spamwriter.writerow(dummy)
            holder[key] = 1

    
    print 'CategoryBehaviorCount Over'
    
CategoryBehaviorCount('1')
CategoryBehaviorCount('2')
CategoryBehaviorCount('3')
CategoryBehaviorCount('4')




'''
#
#
#    GET FEATURE
#
#
'''
        
        
def GetCategoryBehaviorCount(outputTable, behavior):
    inputTable = {}
    behavior_str = behaviorStr(behavior)
    path = '../../csv/complex/category_behavior_count_' + behavior_str + '.csv'
    
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

    