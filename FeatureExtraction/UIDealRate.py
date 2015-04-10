#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def UIDealRate():
    outfile = open('../csv/ui_deal_rate.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id','item_id', 'ui_deal_rate'])
    user_deal_num = {}
    with open('../csv/user_behavior_count.csv', 'rb') as f1:
        reader_olduser = csv.reader(f1)
        for row_click in reader_olduser:
            user_id = row_click[0]
            if(user_id=='user_id'):
                    continue
            user_deal = int(row_click[4])
            if(user_deal==0):
                continue
            user_deal_num[user_id] = user_deal
      
    with open('../csv/user_item_behavior_count.csv','rb') as f2:
        reader_ui = csv.reader(f2)
        for row_ui in reader_ui:
            ui_id = row_ui[0]
            if(ui_id=='user_id'):
                continue
            item_id = row_ui[1]
            ui_deal = int(row_ui[5])
            if(ui_deal==0):
                continue
            
            if user_deal_num.get(ui_id):
                user_total_deal = user_deal_num[ui_id]
                rate = ui_deal/float(user_total_deal)
                spamwriter.writerow([ui_id,item_id,rate])
             

    
'''
#
#
#    GET FEATURE
#
#
'''
def GetUIDealRate(outputTable):
    inputTable = {}
    with open('../csv/ui_deal_rate.csv', 'rb') as reader:
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            feature = row[2]
            
            if user_id == 'user_id':
                continue
            
            key = user_id + ' ' + item_id
            inputTable[key] = float(feature)        
    
    for key in outputTable.keys():
        if not inputTable.get(key):
            outputTable[key].append(0)
        else:
            outputTable[key].append(inputTable[key])
        
        
