#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def UConversionRate():
    table = {}
    with open('../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        
        for row in reader:
            user_id = row[0]
            behavior_type = row[2]
            
            if user_id == 'user_id':
                continue
            
            behavior_type = int(behavior_type)
            
            if table.get(user_id):
                if behavior_type < 4:
                    table[user_id][0] += 1
                else:
                    table[user_id][1] += 1
            else:
                if behavior_type < 4:
                    table[user_id] = [1, 0]
                else:
                    table[user_id] = [0, 1] 
        
    # 输出的文件头
    outfile = open('../csv/user_conversion_rate.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'conversion_rate'])
    
    for key in table.keys():
        spamwriter.writerow([key,  table[key][1] / float(table[key][0])])
        
    print 'UConversionRate Done!'
        

'''
#
#
#    GET FEATURE
#
#
'''
def GetUConversionRate(outputTable):
    inputTable = {}
    with open('../csv/user_conversion_rate.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            ConversionRate = row[1]
            
            if user_id == 'user_id':
                continue
            
            inputTable[user_id] = float(ConversionRate)            
    
    for key in outputTable.keys():
        user_id = key.split()[0]
        outputTable[key].append(inputTable[user_id])
        
        
        