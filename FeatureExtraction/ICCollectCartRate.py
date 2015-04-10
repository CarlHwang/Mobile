#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def CollectCartRate():
    itemTable = {}
    categoryTable = {}
    with open('../csv/user_item_behavior_count.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            item_category = row[2]
            collect = row[4]
            cart = row[5]
            
            if user_id == 'user_id':
                continue
            
            collect = int(collect)
            cart = int(cart)
            
            if itemTable.get(item_id):
                itemTable[item_id] += collect + cart
            else:
                itemTable[item_id] = collect + cart
                
            if categoryTable.get(item_category):
                categoryTable[item_category] += collect + cart
            else:
                categoryTable[item_category] = collect + cart
                
    # 输出的文件头
    outfile = open('../csv/ic_collect_cart_rate.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['item_id', 'collect_cart_rate'])            
    
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

    print 'CollectCartRate() Done!'
    
CollectCartRate()

'''
#
#
#    GET FEATURE
#
#
'''
def GetCollectCartRate(outputTable):
    inputTable = {}
    with open('../csv/ic_collect_cart_rate.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            item_id = row[0]
            CollectCartRate = row[1]
            
            if item_id == 'item_id':
                continue
            
            inputTable[item_id] = float(CollectCartRate)            
    
    for key in outputTable.keys():
        item_id = key.split()[1]
        outputTable[key].append(inputTable[item_id])

