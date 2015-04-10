#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def user_item_behavior_count():
    outfile = open('../csv/user_item_behavior_count.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id','item_id','item_category', 'click', 'collect', 'cart', 'deal'])
    items = {}
    with open('../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            item_category = row[4]
            
            behavior_type = row[2]

            if user_id == 'user_id':
                continue
            
            behavior_type = int(behavior_type)
            
            key = user_id+' '+item_id+' '+item_category
            if not items.get(key):
                behaviors = [0,0,0,0]
                behaviors[behavior_type-1] += 1
                items[key] = behaviors
            else:
                items[key][behavior_type-1] += 1
            print item_id, behavior_type
    
    for key in items.keys():
        behaviors = items.get(key)
        a=key.split()
        spamwriter.writerow([a[0],a[1],a[2], behaviors[0], behaviors[1], behaviors[2], behaviors[3]])   
    
if __name__ == '__main__':
    user_item_behavior_count()


'''
#
#
#    GET FEATURE
#
#
'''
def GetItemBehaviorCount(outputTable):
    inputTable = {}
    with open('../csv/user_item_behavior_count.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            ui_id = row[0]+' '+row[1]
            click = row[2]
            collect = row[3]
            cart = row[4]
            deal = row[5]
            
            if row[0] == 'user_id':
                continue
            
            inputTable[ui_id] = [click,collect,cart,deal]
   
    for key in outputTable.keys():
        outputTable[key].extend(inputTable[key])
    

