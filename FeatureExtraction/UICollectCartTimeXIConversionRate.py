#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def collectCartXConversionRate():
    crTable = {}
    with open('../csv/item_conversion_rate.csv', 'rb') as infile:
        reader = csv.reader(infile)
        for row in reader:
            item_id = row[0] 
            conversion_rate = row[1]
            
            if item_id == 'item_id':
                continue
            conversion_rate = float(conversion_rate)
            crTable[item_id] = conversion_rate
    
    # 输出的文件头-
    outfile = open('../csv/ui_collect_cart_x_i_conversion_rate.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'feature'])
    
    with open('../csv/user_item_behavior_count.csv', 'rb') as infile:
        reader = csv.reader(infile)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            collect = row[3]
            cart = row[4]
            
            if user_id == 'user_id':
                continue

            collect = int(collect)
            cart = int(cart)
            
            collectCartXcr = (collect + cart) * crTable[item_id]
            spamwriter.writerow([user_id, item_id, collectCartXcr])
            
    print 'collectCartXConversionRate Done!'
    
collectCartXConversionRate()
