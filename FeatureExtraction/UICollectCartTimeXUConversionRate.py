#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def UICollectCartXUConversionRate():
    crTable = {}
    with open('../csv/user_conversion_rate.csv', 'rb') as infile:
        reader = csv.reader(infile)
        for row in reader:
            user_id = row[0] 
            conversion_rate = row[1]
            
            if user_id == 'user_id':
                continue
            conversion_rate = float(conversion_rate)
            crTable[user_id] = conversion_rate
    
    # 输出的文件头-
    outfile = open('../csv/ui_collect_cart_x_u_conversion_rate.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'feature'])
    
    with open('../csv/user_item_behavior_count.csv', 'rb') as infile:
        reader = csv.reader(infile)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            collect = row[4]
            cart = row[5]
            
            if user_id == 'user_id':
                continue

            collect = int(collect)
            cart = int(cart)
            
            collectCartXcr = (collect + cart) * crTable[user_id]
            spamwriter.writerow([user_id, item_id, collectCartXcr])
            
    print 'UICollectCartXUConversionRate Done!'
    
            
            
'''
#
#
#    GET FEATURE
#
#
'''
def GetUICollectCartXUConversionRate(outputTable):
    inputTable = {}
    with open('../csv/ui_collect_cart_x_u_conversion_rate.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            feature = row[2]
            
            if user_id == 'user_id':
                continue
            
            key = user_id + ' ' + item_id
            inputTable[key] = float(feature)
            
    for key in outputTable.keys():
        if not inputTable.get(key):
            outputTable[key].append(0)
        else:
            outputTable[key].append(inputTable[key])
        
        