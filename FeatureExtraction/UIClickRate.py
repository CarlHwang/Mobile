#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def UICClickRate():
    outfile = open('../csv/ui_click_rate.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id','item_id', 'ui_click_rate'])
    user_click_num = {}
    with open('../csv/user_behavior_count.csv', 'rb') as f1:
        reader_olduser = csv.reader(f1)
        for row_click in reader_olduser:
            user_id = row_click[0]
            if(user_id=='user_id'):
                    continue
            user_click = int(row_click[1])
            if(user_click==0):
                continue
            user_click_num[user_id] = user_click
      
    with open('../csv/user_item_behavior_count.csv','rb') as f2:
        reader_ui = csv.reader(f2)
        for row_ui in reader_ui:
            ui_id = row_ui[0]
            if(ui_id=='user_id'):
                continue
            item_id = row_ui[1]
            ui_click = int(row_ui[2])
            if(ui_click==0):
                continue
            if user_click_num.get(ui_id):
                user_total_click = user_click_num[ui_id]
                rate = ui_click/float(user_total_click)
                spamwriter.writerow([ui_id,item_id,rate])

'''
#
#
#    GET FEATURE
#
#
'''   
def GetUICClickRate(outputTable):
    inputTable = {}
    #minUserDealFreq = 0
    with open('../csv/ui_click_rate.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            ui_id = row[0]+' '+row[1]
            ClickRate = row[2]
            
            if row[0] == 'user_id':
                continue
            
            inputTable[ui_id] = float(ClickRate)            
    
    for key in outputTable.keys():
        if not inputTable.get(key):
            outputTable[key].append(0)
        else:
            outputTable[key].append(inputTable[key])
        
