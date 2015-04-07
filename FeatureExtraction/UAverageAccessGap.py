#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

# 用户在数据集所包含的时间范围内，平均每两次访问的间隔，如果这段时间内只有1次访问，则以数据集的时间跨度作为间隔
def AverageAccessGap():
    table = {}
    maxTime, minTime = -1, -1
    with open('../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            time = row[5]
            
            if user_id == 'user_id':
                continue
            
            # global window time
            time = int(time)
            if maxTime < 0:
                maxTime, minTime = time, time
            else:
                maxTime, minTime = max(maxTime, time), min(minTime, time)
            
            if table.get(user_id):
                if not time in table[user_id]:
                    table[user_id].append(time)
            else:
                table[user_id] = [time]
                
    gapTable = {}
    maxGap = maxTime - minTime + 1
    for user_id in table.keys():
        maxV = max(table[user_id])
        minV = min(table[user_id])
        num = len(table[user_id])
        
        if num == 1:
            gapTable[user_id] = float(maxGap)
        else:
            gapTable[user_id] = (maxV-minV+1)/float(num-1)
            
    # 输出的文件头
    outfile = open('../csv/user_average_access_gap.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'average_gap'])
    
    for user_id in gapTable.keys():
        spamwriter.writerow([user_id, gapTable[user_id]])
        
    print 'UAverageAccessGap Over'
        
if __name__ == '__main__':
    AverageAccessGap()
    pass


'''
#
#
#    GET FEATURE
#
#
'''

def GetUserAvgAccessGap(outputTable):
    inputTable = {}
    with open('../csv/user_average_access_gap.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            access_gap = row[1]
            
            if user_id == 'user_id':
                continue
            
            inputTable[user_id] = access_gap
    
    for key in outputTable.keys():
        user_id = key.split()[0]
        outputTable[key]['user_average_access_gap'] = inputTable[user_id]

