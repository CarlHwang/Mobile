#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def DealRate():
    itemTable = {}
    categoryTable = {}
    with open('../csv/user_item_behavior_count.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            item_category = row[2]
            
            deal = row[6]
            
            if user_id == 'user_id':
                continue
            
            deal = int(deal)
            
            if itemTable.get(item_id):
                itemTable[item_id] += deal
            else:
                itemTable[item_id] = deal
                
            if categoryTable.get(item_category):
                categoryTable[item_category] += deal
            else:
                categoryTable[item_category] = deal
                
    # 输出的文件头
    outfile = open('../csv/ic_deal_rate.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['item_id', 'deal_rate'])            
    
    with open('../csv/user_item_behavior_count.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            item_id = row[1]
            item_category = row[2]
            if item_id == 'item_id':
                continue
            if categoryTable[item_category] == 0:
                spamwriter.writerow([item_id, 0])
            else:
                spamwriter.writerow([item_id, itemTable[item_id]/float(categoryTable[item_category])])

    print 'DealRate() Done!'
    
DealRate()

'''
#
#
#    GET FEATURE
#
#
'''
def GetDealRate(outputTable):
    inputTable = {}
    with open('../csv/ic_deal_rate.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            item_id = row[0]
            DealRate = row[1]
            
            if item_id == 'item_id':
                continue
            
            inputTable[item_id] = float(DealRate)            
    
    for key in outputTable.keys():
        item_id = key.split()[1]
        outputTable[key].append(inputTable[item_id])

