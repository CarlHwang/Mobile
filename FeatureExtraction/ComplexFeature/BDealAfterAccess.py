#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from Globals import behaviorStr


# 访问了多久会买

def DealAfterAccess(behavior):
    
    dealTable = {}
    accessTable = {}
    maxTime, minTime = -1, -1
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
            
            if maxTime == -1:
                maxTime, minTime = time, time
            else:
                maxTime, minTime = max(maxTime, time), min(minTime, time)
                
            if behavior_type == behavior:
                
                if accessTable.get(user_id):
                    
                    if not accessTable[user_id].get(item_id):
                        accessTable[user_id][item_id] = []
                    if time not in accessTable[user_id][item_id]:
                        accessTable[user_id][item_id].append(time)
                else:
                    accessTable[user_id] = {item_id:[time]}
                    
            elif behavior_type == '4':
                
                if dealTable.get(user_id):
                    
                    if not dealTable[user_id].get(item_id):
                        dealTable[user_id][item_id] = []
                    if time not in dealTable[user_id][item_id]:
                        dealTable[user_id][item_id].append(time)
                else:
                    dealTable[user_id] = {item_id:[time]}
                
    # 输出的文件头
    behavior_str = behaviorStr(behavior)
    path = '../../csv/complex/deal_after_' + behavior_str + '.csv'
    outfile = open(path, 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    
    head = [1,2,3,4,5,6,7,8,9,10,12,14,16,18,20,25,30,40,50,60,80,100,150]
    row = ['user_id', 'item_id']
    row.extend(head)
    
    spamwriter.writerow(row)
        
    for user_id in accessTable.keys():
 
        items = accessTable[user_id]
        for item_id in items.keys():
            
            result = []
            for gap in head:
                    
                if len(result)>0 and result[-1] == 1:
                    result.append(1)
                    continue
                
                access_times = items[item_id]
                
                
                dealed = False
                for click_time in access_times:
                    
                    time_upper_bound = click_time + gap
                    
                    if dealTable.get(user_id) and dealTable[user_id].get(item_id):
                        deal_times = dealTable[user_id][item_id]
                        
                        for deal_time in deal_times:
                            if deal_time <= time_upper_bound:
                                result.append(1)
                                dealed = True
                                break
                        if dealed == True:
                            break
                        
                if dealed == False:
                    result.append(0)    
            
            row = [user_id, item_id]
            row.extend(result)
            spamwriter.writerow(row)
            print user_id, item_id, len(row)


DealAfterAccess('1')
DealAfterAccess('2')
DealAfterAccess('3')

'''
#
#
#    GET FEATURE
#
#
'''
        
        
def GetDealAfterAccess(outputTable, behavior):
    inputTable = {}
    behavior_str = behaviorStr(behavior)
    path = '../../csv/complex/deal_after_' + behavior_str + '.csv'
    
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
