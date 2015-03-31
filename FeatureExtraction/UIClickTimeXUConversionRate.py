#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def clickXConversionRate():
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
    outfile = open('../csv/ui_click_x_u_conversion_rate.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'feature'])
    
    with open('../csv/user_item_behavior_count.csv', 'rb') as infile:
        reader = csv.reader(infile)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            click = row[3]
            
            if user_id == 'user_id':
                continue

            click = int(click)
            clickXcr = click * crTable[user_id]
            spamwriter.writerow([user_id, item_id, clickXcr])
            
    print 'clickXConversionRate Done!'
    
clickXConversionRate()

            