#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def user_item_behavior_count():
    outfile = open('../csv/user_item_behavior_count.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id','item_id', 'click', 'collect', 'cart', 'deal'])
    a = []
    items = {}
    with open('../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            item_id = row[0]+' '+row[1]
            behavior_type = row[2]

            if(len(behavior_type) > 2):
                continue
            
            behavior_type = int(behavior_type)
            
            if not items.get(item_id):
                behaviors = [0,0,0,0]
                behaviors[behavior_type-1] += 1
                items[item_id] = behaviors
            else:
                items[item_id][behavior_type-1] += 1
            print item_id, behavior_type
    
    for key in items.keys():
        behaviors = items.get(key)
        a=key.split()
        spamwriter.writerow([a[0],a[1], behaviors[0], behaviors[1], behaviors[2], behaviors[3]])   
    
if __name__ == '__main__':
    user_item_behavior_count()
