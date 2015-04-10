#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def ICClickRate():
    itemTable = {}
    categoryTable = {}
    with open('../csv/user_item_behavior_count.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            item_category = row[2]
            
            click = row[3]
            
            if user_id == 'user_id':
                continue
            
            click = int(click)
            
            if itemTable.get(item_id):
                itemTable[item_id] += click
            else:
                itemTable[item_id] = click
                
            if categoryTable.get(item_category):
                categoryTable[item_category] += click
            else:
                categoryTable[item_category] = click
                
    # 输出的文件头
    outfile = open('../csv/ic_click_rate.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['item_id', 'click_rate'])            
    
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

    print 'ClickRate Done!'


'''
#
#
#    GET FEATURE
#
#
'''
def GetICClickRate(outputTable):
    inputTable = {}
    with open('../csv/ic_click_rate.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            item_id = row[0]
            ClickRate = row[1]
            
            if item_id == 'item_id':
                continue
            
            inputTable[item_id] = float(ClickRate)            
    
    for key in outputTable.keys():
        item_id = key.split()[1]
        if not inputTable.get(item_id):
            outputTable[key].append(0)
        else:
            outputTable[key].append(inputTable[item_id])

