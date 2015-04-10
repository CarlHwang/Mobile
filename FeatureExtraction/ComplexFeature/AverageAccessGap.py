#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from Globals import SplitHour, behaviorStr

# 1. 用户对该商品最近1、2、3、4、5、6、7、8、9、10、12、14、16、18、20、25、30、40、50、60、80、100、150小时内平均 点击、收藏、加购、购买 的频率（平均每小时访问几次）

def AverageAccessGap(behavior):
    table = {}
    
    head = [1,2,3,4,5,6,7,8,9,10,12,14,16,18,20,25,30,40,50,60,80,100,150]
    maxHead = max(head)
    
    with open('../../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            behavoir_type  = row[2]
            time = row[5]
            
            if user_id == 'user_id':
                continue
            if not behavoir_type == behavior:
                continue
            
            # global window time
            time = int(time)
            if time <= SplitHour - maxHead:
                continue
            
            if table.get(user_id):
                if not table[user_id].get(item_id):
                    table[user_id][item_id] = []
                table[user_id][item_id].append(time)
            else:
                table[user_id] = {item_id:[time]}
                
    # 输出的文件头
    behavior_str = behaviorStr(behavior)
    path = '../../csv/complex/average_access_gap_' + behavior_str + '.csv'
    
    outfile = open(path, 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    
    row = ['user_id', 'item_id']
    row.extend(head)
    spamwriter.writerow(row)           
    
    for user_id in table.keys():
        for item_id in table[user_id].keys():
            print user_id, item_id
            row = []
            for time in head:
                count = 0
                for access_time in table[user_id][item_id]:
                    if access_time >= SplitHour - time + 1:
                        count += 1
                row.append(float(count)/time)
            dummy = [user_id, item_id]
            dummy.extend(row)
            spamwriter.writerow(dummy)
    
    print 'AverageAccessGap Over'
    
# AverageAccessGap('1')
# AverageAccessGap('2')
# AverageAccessGap('3')
# AverageAccessGap('4')


'''
#
#
#    GET FEATURE
#
#
'''
        
        
def GetAverageAccessGap(outputTable, behavior):
    inputTable = {}
    behavior_str = behaviorStr(behavior)
    path = '../../csv/complex/average_access_gap_' + behavior_str + '.csv'
    
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
        
#         if not inputTable.get(key):
#             features = [0]*len(head)
#         else:
#             features = inputTable[key]
#             
#         for i in range(len(head)):
#             feature_name = 'AverageAccessGap_' + str(head[i])
#             outputTable[key][feature_name] = features[i]
        

    