#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def UICollectCartRate():
    outfile = open('../csv/ui_collect_cart_rate.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id','item_id', 'collect_cart_rate'])
    user_cc_num = {}
    with open('../csv/user_behavior_count.csv', 'rb') as f1:
        reader = csv.reader(f1)
        for row in reader:
            user_id = row[0]
            if(user_id=='user_id'):
                    continue
            user_cc = int(row[2])+int(row[3])
            if(user_cc==0):
                continue
            user_cc_num[user_id] = user_cc
      
    with open('../csv/user_item_behavior_count.csv','rb') as f2:
        reader_ui = csv.reader(f2)
        for row_ui in reader_ui:
            ui_id = row_ui[0]
            if(ui_id=='user_id'):
                continue
            item_id = row_ui[1]
            ui_cc = int(row_ui[3])+int(row_ui[4])
            if(ui_cc==0):
                continue
            
            if user_cc_num.get(ui_id):
                user_total_deal = user_cc_num[ui_id]
                rate = ui_cc/float(user_total_deal)
                spamwriter.writerow([ui_id,item_id,rate])
             


'''
#
#
#    GET FEATURE
#
#
'''
def GetUICollectCartRate(outputTable):
    inputTable = {}
    with open('../csv/ui_collect_cart_rate.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]+' '+row[1]
            collect_cart_rate = row[2]
            
            if row[0] == 'user_id':
                continue
            
            inputTable[user_id] = float(collect_cart_rate)            
    
    for key in outputTable.keys():
        if not inputTable.get(key):
            outputTable[key].append(0)
        else:
            outputTable[key].append(inputTable[key])
        
        
        