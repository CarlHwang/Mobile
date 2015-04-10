#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def UICCollectCartRate():
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
                if itemTable[item_id].get(user_id):
                    itemTable[item_id][user_id] += collect + cart # in fact, it is not possible to get here since the csv ensures that one item_id matches only one user_id
                else:
                    itemTable[item_id][user_id] = collect + cart
            else:
                itemTable[item_id] = {user_id : collect + cart}
                
            if categoryTable.get(item_category):
                if categoryTable[item_category].get(user_id):
                    categoryTable[item_category][user_id] += collect + cart
                else:
                    categoryTable[item_category][user_id] = collect + cart
            else:
                categoryTable[item_category] = {user_id : collect + cart}
                
    # 输出的文件头
    outfile = open('../csv/uic_collect_cart_rate.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'collect_cart_rate'])            
    
    with open('../csv/user_item_behavior_count.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            item_category = row[2]
            if item_id == 'item_id':
                continue
            
            if categoryTable[item_category][user_id] == 0:
                spamwriter.writerow([user_id, item_id, 0])
            else:
                spamwriter.writerow([user_id, item_id, itemTable[item_id][user_id]/float(categoryTable[item_category][user_id])])

    print 'UICCollectCartRate() Done!'
    
'''
#
#
#    GET FEATURE
#
#
'''
def GetUICCollectCartRate(outputTable):
    inputTable = {}
    with open('../csv/uic_collect_cart_rate.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            ui_id = row[0]+' '+row[1]
            CollectCartRate = row[2]
            
            if row[0] == 'user_id':
                continue
            
            inputTable[ui_id] = float(CollectCartRate)            
    
    for key in outputTable.keys():
        if not inputTable.get(key):
            outputTable[key].append(0)
        else:
            outputTable[key].append(inputTable[key])
