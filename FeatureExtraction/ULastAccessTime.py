#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

# 用户最后（近）一次访问距离‘分割点’（数据集最后大时刻）多远
def LastAccessTime():
    table = {}
    with open('../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            time = row[5]
            
            if user_id == 'user_id':
                continue
            
            time = int(time)
            
            if table.get(user_id):
                table[user_id] = max(table[user_id], time)
            else:
                table[user_id] = time
                
    tmax = max(table.values())
    print tmax
    for key in table.keys():
        table[key] = tmax - table[key]            
    
    # 输出的文件头
    outfile = open('../csv/user_last_access_time.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'time_to_current'])
    
    for key in table.keys():
        spamwriter.writerow([key, table[key]])
        
LastAccessTime()
