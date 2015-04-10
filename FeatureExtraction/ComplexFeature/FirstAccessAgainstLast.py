#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from Globals import behaviorStr

# 5. 用户第一次 点击+收藏、加购、购买该商品和最后一次点击+收藏、加购、购买该商品相隔多少个小时


def FirstAccessAgainstLast(behavior):
    
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
            
            time = int(time)
            behavior_type = int(behavior_type)
            
            if behavior_type <= 2 and (behavior == '3' or behavior == '4'):
                continue
            elif behavior_type > 2 and not behavior_type == int(behavior):
                continue
                
            print behavior_type
                        
            if table.get(user_id):
                if not table[user_id].get(item_id):
                    table[user_id][item_id] = [time, time]
                else:
                    (Max, Min) = table[user_id][item_id]
                    table[user_id][item_id] = [max(time, Max), min(time, Min)]
            else:
                table[user_id] = {item_id:[time, time]}
                
    # 输出的文件头
    behavior_str = behaviorStr(behavior)
    path = '../../csv/complex/first_access_against_last_' + behavior_str + '.csv'
    
    outfile = open(path, 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'gap'])
    
    for user_id in table.keys():
        for item_id in table[user_id].keys():
            spamwriter.writerow([user_id, item_id, table[user_id][item_id][0]-table[user_id][item_id][1]])
            
    print "FirstAccessAgainstLast Done!"
                    
FirstAccessAgainstLast('1')
FirstAccessAgainstLast('3')
FirstAccessAgainstLast('4')



'''
#
#
#    GET FEATURE
#
#
'''
        
        
def GetFirstAccessAgainstLast(outputTable, behavior):
    inputTable = {}
    behavior_str = behaviorStr(behavior)
    path = '../../csv/complex/first_access_against_last_' + behavior_str + '.csv'
    
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

            