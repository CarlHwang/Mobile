#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def ItemRebuyRate():
    outfile = open('../csv/item_rebuy_rate.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['item_id', 'rebuy_rate'])
    user_num_per_item = {}
    with open('../csv/train_user_time_to_int_cleaned.csv', 'rb') as f1:
        reader = csv.reader(f1)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            behavior_type = row[2]
            if(user_id=='user_id'):
                    continue
            if behavior_type=='4':
                if not user_num_per_item.get(item_id):
                    user_num_per_item[item_id] = [user_id]
                else:
                    user_list = user_num_per_item[item_id]
                    if user_id not in user_list:
                        user_list.append(user_id)
                    user_num_per_item[item_id] = user_list

                
            
    with open('../csv/item_behavior_count.csv','rb') as f2:
        reader_deal = csv.reader(f2)
        for row_deal in reader_deal:
            item_id_deal = row_deal[0]
            if(item_id_deal=='item_id'):
                continue
            deal = int(row_deal[4])
            if user_num_per_item.get(item_id_deal):
                user_num = len(user_num_per_item[item_id_deal])

                rate=(deal-user_num)/float(deal)
                spamwriter.writerow([item_id_deal,rate])

                print item_id_deal,rate,deal,user_num


    '''
#
#
#    GET FEATURE
#
#
'''
def GetItemRebuyRate(outputTable):
    inputTable = {}
    with open('../csv/item_rebuy_rate.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            item_id = row[0]
            item_rebuy_rate = row[1]
            
            if item_id == 'item_id':
                continue
            
            inputTable[item_id] = float(item_rebuy_rate)            
    
    for key in outputTable.keys():
        item_id = key.split()[1]
        if not inputTable.get(item_id):
            outputTable[key].append(0)
        else:
            outputTable[key].append(inputTable[item_id])
        
        