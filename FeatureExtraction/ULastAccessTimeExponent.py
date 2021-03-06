#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import numpy as np
import math

def ULastAccessTimeExponent():
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
    sigma = np.var(table.values())
    print tmax
    for key in table.keys():
        table[key] = math.e ** (-1 * (tmax - table[key])/(2*sigma))
    
    # 输出的文件头
    outfile = open('../csv/user_last_access_time_exp.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'exp'])
    
    for key in table.keys():
        spamwriter.writerow([key, table[key]])
        
    print 'ULastAccessTimeExponent Done!'
        


'''
#
#
#    GET FEATURE
#
#
'''   
def GetULastAccessTimeExponent(outputTable):
    inputTable = {}
    with open('../csv/user_last_access_time_exp.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            LastAccessTimeExponent = row[1]
            
            if user_id == 'user_id':
                continue
            
            inputTable[user_id] = float(LastAccessTimeExponent)            
    
    for key in outputTable.keys():
        user_id = key.split()[0]
        outputTable[key].append(inputTable[user_id])

