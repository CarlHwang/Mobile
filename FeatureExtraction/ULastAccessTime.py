#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from Globals import SplitHour

# 用户最后（近）一次访问距离‘分割点’（数据集最后大时刻）多远
def ULastAccessTime():
    table = {}
    with open('../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            time = row[5]
            
            if user_id == 'user_id':
                continue
            
            time = int(time)
            gap = SplitHour - time + 1
            
            if table.get(user_id):
                table[user_id] = min(table[user_id], gap)
            else:
                table[user_id] = gap
                          
    
    # 输出的文件头
    outfile = open('../csv/user_last_access_time.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'time_to_current'])
    
    for key in table.keys():
        spamwriter.writerow([key, table[key]])
        
'''
#
#
#    GET FEATURE
#
#
'''
def GetULastAccessTime(outputTable):
    inputTable = {}
    with open('../csv/user_last_access_time.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            LastAccessTime = row[1]
            
            if user_id == 'user_id':
                continue
            
            inputTable[user_id] = float(LastAccessTime)            
    
    for key in outputTable.keys():
        user_id = key.split()[0]
        outputTable[key].append(inputTable[user_id])
        
        
        
        