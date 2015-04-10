#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def IOldCustomerProportion():
    table = {}
    with open('../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            behavior_type = row[2]
            
            if user_id == 'user_id':
                continue
            
            behavior_type = int(behavior_type)
            
            if table.get(item_id):
                if behavior_type > 3:
                    if table[item_id].get(user_id):
                        table[item_id][user_id] += 1
                    else:
                        table[item_id][user_id] = 1
            else:
                if behavior_type > 3:
                    table[item_id] = {user_id : 1}
                else:
                    table[item_id] = {}
    
    # 输出的文件头
    outfile = open('../csv/item_old_customer_proportion.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['item_id', 'proportion'])
    for item in table:
        userDict = table[item]
        num = 0
        bought = 0
        multi = 0
        for user in userDict:
            if userDict[user] > 0:
                bought += 1
                if userDict[user] > 1:
                    multi += 1
            num += 1
        if num == 0:
            spamwriter.writerow([item, 0])
        else:
            spamwriter.writerow([item, float(multi)/bought])
        
    print 'IOldCustomerProportion Done!'
        

'''
#
#
#    GET FEATURE
#
#
'''
def GetIOldCustomerProportion(outputTable):
    inputTable = {}
    with open('../csv/item_old_customer_proportion.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            item_id = row[0]
            OldCustomerProportion = row[1]
            
            if item_id == 'item_id':
                continue
            
            inputTable[item_id] = float(OldCustomerProportion)            
    
    for key in outputTable.keys():
        item_id = key.split()[1]
        outputTable[key].append(inputTable[item_id])
