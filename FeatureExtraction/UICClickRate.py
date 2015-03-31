#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def ClickRate():
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
                if itemTable[item_id].get(user_id):
                    itemTable[item_id][user_id] += click # in fact, it is not possible to get here since the csv ensures that one item_id matches only one user_id
                else:
                    itemTable[item_id][user_id] = click
            else:
                itemTable[item_id] = {user_id : click}
                
            if categoryTable.get(item_category):
                if categoryTable[item_category].get(user_id):
                    categoryTable[item_category][user_id] += click
                else:
                    categoryTable[item_category][user_id] = click
            else:
                categoryTable[item_category] = {user_id : click}
                
    # 输出的文件头
    outfile = open('../csv/uic_click_rate.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'deal_rate'])            
    
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

    print 'ClickRate() Done!'
    
ClickRate()
