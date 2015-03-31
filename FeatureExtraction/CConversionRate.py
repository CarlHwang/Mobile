#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def ConversionRate():
    table = {}
    with open('../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        
        for row in reader:
            item_category = row[4]
            behavior_type = row[2]
            
            if item_category == 'item_category':
                continue
            
            behavior_type = int(behavior_type)
            
            if table.get(item_category):
                if behavior_type < 4:
                    table[item_category][0] += 1
                else:
                    table[item_category][1] += 1
            else:
                if behavior_type < 4:
                    table[item_category] = [1, 0]
                else:
                    table[item_category] = [0, 1] 
        
    # 输出的文件头
    outfile = open('../csv/category_conversion_rate.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['item_category', 'conversion_rate'])
    
    for key in table.keys():
        spamwriter.writerow([key,  table[key][1] / float(table[key][0])])
        
    print 'CConversionRate Done!'
        
ConversionRate()
