#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def CConversionRate():
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
        

'''
#
#
#    GET FEATURE
#
#
'''
def GetCConversionRate(outputTable):
    item_to_cate = {}
    with open('../csv/train_user_time_to_int_cleaned.csv','rb') as f1:
        reader = csv.reader(f1)
        for row in reader:
            item_id = row[1]
            cate = row[4]
            if item_id=='item_id':
                continue
            if not item_to_cate.get(item_id):
                item_to_cate[item_id] = cate
                

    inputTable = {}
    with open('../csv/category_conversion_rate.csv', 'rb') as f2:
        reader = csv.reader(f2)
        for row in reader:
            item_category = row[0]
            ConversionRate = row[1]
            
            if item_category == 'item_category':
                continue
            
            inputTable[item_id] = float(ConversionRate)            
    
    for key in outputTable.keys():
        item_id = key.split()[1]
        item_category = item_to_cate[item_id]
        if not inputTable.get(item_category):
            outputTable[key].append(0)
        else:
            outputTable[key].append(inputTable[item_category])
        
