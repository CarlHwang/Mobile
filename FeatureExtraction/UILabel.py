#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

labelTable = {}

def GetLabel():
    
    with open('../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            behavior_type = row[2]
            
            if user_id == 'user_id':
                continue
            
            key = user_id + ' ' + item_id
            if not labelTable.get(key):
                if behavior_type == '4':
                    labelTable[key] = 1
                else:
                    labelTable[key] = 0
            else:
                if behavior_type == '4':
                    labelTable[key] = 1
                
                
    # 输出的文件头
    outfile = open('../csv/label.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'label'])
                        
    for key in labelTable.keys():
        user_id, item_id = key.split()[0], key.split()[1]
        spamwriter.writerow([user_id, item_id, labelTable[key]])
        
        
GetLabel()
