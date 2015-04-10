#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def UIClickXCConversionRate():
    crTable = {}
    with open('../csv/category_conversion_rate.csv', 'rb') as infile:
        reader = csv.reader(infile)
        for row in reader:
            item_category = row[0] 
            conversion_rate = row[1]
            
            if item_category == 'item_category':
                continue
            conversion_rate = float(conversion_rate)
            crTable[item_category] = conversion_rate
    
    # 输出的文件头-
    outfile = open('../csv/ui_click_x_c_conversion_rate.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'feature'])
    
    with open('../csv/user_item_behavior_count.csv', 'rb') as infile:
        reader = csv.reader(infile)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            item_category = row[2]
            click = row[3]

            if user_id == 'user_id':
                continue

            click = int(click)
            clickXcr = click * crTable[item_category]
            spamwriter.writerow([user_id, item_id, clickXcr])
            
    print 'UIClickXCConversionRate Done!'
    


'''
#
#
#    GET FEATURE
#
#
'''   
def GetUIClickXCConversionRate(outputTable):
    inputTable = {}
    with open('../csv/ui_click_x_c_conversion_rate.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            ui_id = row[0]+' '+row[1]
            conversion_rate = row[2]
            
            if row[0] == 'user_id':
                continue

            inputTable[ui_id] = float(conversion_rate)            
    
    for key in outputTable.keys():
        if not inputTable.get(key):
            outputTable[key].append(0)
        else:
            outputTable[key].append(inputTable[key])

            